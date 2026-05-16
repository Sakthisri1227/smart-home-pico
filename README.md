# ⚡ Smart Energy-Efficient Home Automation System
### Using Raspberry Pi Pico | MicroPython

> **Upgraded from**: 1st Year Basic Home Automation Project  
> **Upgraded to**: Smart Energy Monitoring + Automation System

---

## 📸 Project Demo

> *(Add your project photos/video here)*

---

## 🔹 Problem Statement

Traditional home automation systems allow users to control appliances remotely, but they do **not monitor energy usage or optimize power consumption**. This leads to unnecessary energy wastage and higher electricity costs.

This project builds a smart home system that not only **automates appliances** but also **monitors and reduces energy consumption** efficiently.

---

## ✅ What's NEW compared to the Old Project?

| Feature | Old Project (Year 1) | New Project (Enhanced) |
|---|---|---|
| Control | Manual ON/OFF | Auto + Manual |
| Intelligence | Basic | Smart decision logic |
| Energy Monitoring | ❌ None | ✅ Real-time |
| Power Analysis | ❌ None | ✅ Daily calculation |
| Sensors | Basic | PIR + LDR + Current |
| Display | LED only | Serial + Web Dashboard |

---

## 🎯 Objectives

1. Design a smart home automation system using **Raspberry Pi Pico**
2. Monitor **real-time energy consumption** of home appliances
3. Reduce power wastage using **automatic control logic**
4. Display energy usage data to the user
5. Improve overall **energy efficiency** in homes

---

## 🔧 Hardware Components

| Component | Purpose |
|---|---|
| Raspberry Pi Pico | Main microcontroller |
| ACS712 Current Sensor | Measures current consumption |
| PIR Motion Sensor | Detects room occupancy |
| LDR (Light Sensor) | Detects ambient light level |
| Relay Module | Controls appliance ON/OFF |
| Bulb / Fan (Load) | Simulated home appliances |
| Power Supply | 5V for Pico, 230V AC for load |
| Jumper Wires | Connections |

---

## 💻 Software Requirements

- [Arduino IDE](https://www.arduino.cc/en/software) / [Thonny IDE](https://thonny.org/)
- MicroPython firmware for Raspberry Pi Pico
- HTML, CSS, JavaScript (Web Dashboard – optional)
- Serial Monitor

---

## 🗂️ Project Structure

```
smart-home-pico/
│
├── src/
│   ├── main.py              # Main MicroPython code
│   ├── energy_monitor.py    # Energy calculation module
│   └── web_server.py        # Optional: Web dashboard server
│
├── dashboard/
│   └── index.html           # Web-based energy dashboard
│
├── docs/
│   ├── circuit_diagram.md   # Wiring and connections guide
│   └── working_principle.md # Detailed explanation
│
├── diagrams/
│   └── block_diagram.png    # System block diagram
│
└── README.md
```

---

## 🔌 Block Diagram

```
┌──────────────────────────────────┐
│         INPUT SENSORS            │
│  ACS712  │  PIR Sensor  │  LDR  │
└────────────────┬─────────────────┘
                 │
                 ▼
┌──────────────────────────────────┐
│       Raspberry Pi Pico          │
│   (Processing & Decision Logic)  │
└────────────┬─────────────────────┘
             │
      ┌──────┴──────┐
      ▼             ▼
┌──────────┐  ┌──────────────────┐
│  Relay   │  │  Energy Display  │
│  Module  │  │ Serial / Web UI  │
└────┬─────┘  └──────────────────┘
     │
     ▼
┌──────────────┐
│  Appliances  │
│ (Bulb / Fan) │
└──────────────┘
```

---

## ⚙️ Working Principle

1. **Current Sensor (ACS712)** continuously reads the current drawn by connected appliances
2. **PIR Sensor** detects whether a person is present in the room
3. **LDR** detects ambient light to decide if lights are needed
4. **Raspberry Pi Pico** processes all sensor data and applies decision logic:
   - If room is **empty (no PIR)** → Switch OFF appliances automatically
   - If **bright daylight (LDR high)** → Switch OFF lights
   - Calculates **energy consumed = Power × Time**
5. **Energy data** is displayed via Serial Monitor and optional Web Dashboard

---

## 📐 Pin Configuration

| Component | Pico Pin |
|---|---|
| ACS712 (Analog Out) | GP26 (ADC0) |
| PIR Sensor (Digital) | GP15 |
| LDR (Analog) | GP27 (ADC1) |
| Relay 1 (Light) | GP14 |
| Relay 2 (Fan) | GP13 |

---

## 🚀 Getting Started

### 1. Flash MicroPython on Pico
- Download MicroPython `.uf2` from [micropython.org](https://micropython.org/download/rp2-pico/)
- Hold BOOTSEL button → Connect USB → Drag `.uf2` to drive

### 2. Upload Code
```bash
# Using Thonny IDE:
# Open src/main.py → Click Run (F5)
```

### 3. Open Serial Monitor
- Baud Rate: `115200`
- View real-time energy readings

### 4. (Optional) Web Dashboard
- Run `src/web_server.py` on Pico W
- Open browser → `http://<pico-ip>/`

---

## 📊 Energy Monitoring Logic

```python
# Power (Watts) = Voltage × Current
power = 230 * current_amps

# Energy (Wh) = Power × Time (hours)
energy_wh = power * (elapsed_seconds / 3600)

# Daily cost estimation
cost = (energy_wh / 1000) * electricity_rate  # per kWh
```

---

## 👨‍💻 Team / Author

> SAKTHISRI S |
> PRIYANGA B |
> NEGHASHREE S |
> RUVETHA S P |
> POOJA M

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).

---

## 🔗 References

- [MicroPython Docs](https://docs.micropython.org/)
- [ACS712 Datasheet](https://www.sparkfun.com/datasheets/BreakoutBoards/0712.pdf)
- [Raspberry Pi Pico Pinout](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html)
- Base project inspiration: [YouTube Reference](https://youtu.be/l04FsFVuaGs)
