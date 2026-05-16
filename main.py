# ============================================================
# Smart Energy-Efficient Home Automation System
# Raspberry Pi Pico - MicroPython
# ============================================================

from machine import ADC, Pin
import utime

# ── Pin Setup ────────────────────────────────────────────────
pir     = Pin(15, Pin.IN)          # PIR Motion Sensor
relay1  = Pin(14, Pin.OUT)         # Relay 1 → Light
relay2  = Pin(13, Pin.OUT)         # Relay 2 → Fan
adc_cs  = ADC(Pin(26))             # ACS712 Current Sensor → ADC0
adc_ldr = ADC(Pin(27))             # LDR → ADC1

# ── Constants ────────────────────────────────────────────────
VOLTAGE         = 230.0            # AC Mains Voltage (India)
ELECTRICITY_RATE = 6.5             # ₹ per kWh (adjust per your bill)
ADC_REF         = 3.3
ADC_MAX         = 65535
ACS712_ZERO     = 0.5 * ADC_MAX   # Zero-current midpoint
ACS712_SENS     = 0.185            # 5A module: 185 mV/A
LDR_THRESHOLD   = 30000           # Below = dark, Above = bright
NO_MOTION_LIMIT = 30              # Seconds before auto switch-off

# ── State Variables ─────────────────────────────────────────
total_energy_wh = 0.0
last_motion_time = utime.time()
start_time = utime.time()

print("=" * 45)
print("  Smart Energy Home Automation System")
print("  Raspberry Pi Pico | MicroPython")
print("=" * 45)

# ── Helper: Read Current (Amps) ──────────────────────────────
def read_current():
    samples = [adc_cs.read_u16() for _ in range(50)]
    avg = sum(samples) / len(samples)
    voltage_out = (avg / ADC_MAX) * ADC_REF
    zero_v = (ACS712_ZERO / ADC_MAX) * ADC_REF
    current = abs(voltage_out - zero_v) / ACS712_SENS
    return round(current, 3)

# ── Helper: Read LDR (Light Level 0–100%) ───────────────────
def read_ldr_percent():
    raw = adc_ldr.read_u16()
    # Higher raw = more resistance = darker room
    brightness = 100 - int((raw / ADC_MAX) * 100)
    return brightness

# ── Helper: Format time ─────────────────────────────────────
def elapsed_str():
    secs = utime.time() - start_time
    h, m, s = secs // 3600, (secs % 3600) // 60, secs % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

# ── Main Loop ────────────────────────────────────────────────
prev_time = utime.time()

while True:
    now = utime.time()
    dt_seconds = now - prev_time   # Time since last loop
    prev_time = now

    # ── Read Sensors ─────────────────────────────────────────
    motion      = pir.value()          # 1 = motion detected
    brightness  = read_ldr_percent()   # 0 = pitch dark, 100 = bright
    current_A   = read_current()

    # ── Update last motion time ──────────────────────────────
    if motion:
        last_motion_time = now

    time_since_motion = now - last_motion_time

    # ── Decision Logic ───────────────────────────────────────

    # LIGHT CONTROL
    # ON: room is occupied AND dark enough to need light
    if motion and brightness < 50:
        relay1.value(1)   # Light ON
        light_status = "ON"
    elif not motion and time_since_motion > NO_MOTION_LIMIT:
        relay1.value(0)   # Auto OFF (no motion for 30s)
        light_status = "AUTO-OFF"
    else:
        light_status = "ON" if relay1.value() else "OFF"

    # FAN CONTROL (purely motion-based in this example)
    if motion:
        relay2.value(1)
        fan_status = "ON"
    elif time_since_motion > NO_MOTION_LIMIT:
        relay2.value(0)
        fan_status = "AUTO-OFF"
    else:
        fan_status = "ON" if relay2.value() else "OFF"

    # ── Energy Calculation ───────────────────────────────────
    power_W = VOLTAGE * current_A                        # Watts
    energy_wh_now = power_W * (dt_seconds / 3600)        # Wh this cycle
    total_energy_wh += energy_wh_now                     # Accumulate
    total_energy_kwh = total_energy_wh / 1000
    cost_rs = total_energy_kwh * ELECTRICITY_RATE

    # ── Serial Output (every 2 seconds) ─────────────────────
    print(f"\n[{elapsed_str()}] ── Sensor Readings ──────────────────")
    print(f"  Motion Detected : {'YES ✔' if motion else 'NO'}")
    print(f"  Brightness      : {brightness}%  {'(Dark)' if brightness < 50 else '(Bright)'}")
    print(f"  Current         : {current_A:.3f} A")
    print(f"  Power           : {power_W:.2f} W")
    print(f"── Appliance Status ──────────────────────────────────")
    print(f"  Light (Relay 1) : {light_status}")
    print(f"  Fan   (Relay 2) : {fan_status}")
    print(f"── Energy Summary ────────────────────────────────────")
    print(f"  Total Energy    : {total_energy_wh:.4f} Wh  ({total_energy_kwh:.6f} kWh)")
    print(f"  Estimated Cost  : ₹ {cost_rs:.4f}")

    utime.sleep(2)
