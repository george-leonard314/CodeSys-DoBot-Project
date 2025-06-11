# Dobot Magician Python Automation Project

This project demonstrates how to control a Dobot Magician robotic arm using Python, including moving the arm, operating a conveyor belt, and using the IR sensor for object detection. The code is organized into several scripts for different tasks.

---

## Table of Contents
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Setup](#setup)
- [How It Works](#how-it-works)
  - [1. Dobot Control (`nfc_pickup.py`)](#1-dobot-control-nfc_pickuppy)
  - [2. Conveyor Belt and IR Sensor (`belt.py`)](#2-conveyor-belt-and-ir-sensor-beltpy)
  - [3. Dobot Library (`pydobotplus/dobotplus.py`)](#3-dobot-library-pydobotplusdobotpluspy)
- [Running the Project](#running-the-project)
- [Troubleshooting](#troubleshooting)
- [Notes](#notes)

---

## Project Structure

```
CodeSys-DoBot-Project/
├── pydobotplus/
│   └── dobotplus.py      # Main Dobot control library
├── pydobot-master/
│   ├── nfc_pickup.py     # Example: pick and place with Dobot
│   ├── belt.py           # Example: conveyor belt with IR sensor
│   └── test.py           # Example: basic Dobot test
└── .venv/                # Python virtual environment (recommended)
```

---

## Requirements

- **Hardware:**
  - Dobot Magician robotic arm
  - Conveyor belt accessory
  - IR sensor (connected to GP4 port)
- **Software:**
  - Python 3.7+
  - `pyserial` library
  - Dobot connected via USB (e.g., `/dev/ttyACM0` or `/dev/ttyACM1`)

---

## Setup

1. **Clone or copy the project files to your Raspberry Pi or Linux machine.**

2. **(Recommended) Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install pyserial pydobotplus
   ```

4. **Connect your Dobot Magician and accessories (conveyor, IR sensor) as per the hardware manual.**

---

## How It Works

### 1. Dobot Control (`nfc_pickup.py`)

- **Purpose:**
  Moves the Dobot arm through a sequence of positions to pick up an NFC tag and place it on the conveyor belt. - The main program that all the parts should be merged into
- **Key Steps:**
  - Connects to the Dobot on `/dev/ttyACM0`.
  - Moves to initial, middle, and tag positions.
  - Activates the suction cup to pick up the tag.
  - Moves to the belt and releases the tag.
- **Usage:**
  The main function is `move_nfc_on_belt()`. It is run in a thread at the end of the script.

### 2. Conveyor Belt and IR Sensor (`belt.py`)

- **Purpose:**
  Controls the conveyor belt and uses the IR sensor to detect objects. - DEVELOPMENT
- **Key Steps:**
  - Connects to the Dobot on `/dev/ttyACM1`.
  - Enables the IR sensor on GP4.
  - Starts the conveyor belt.
  - Reads the IR sensor state.
- **Usage:**
  Run `python3 pydobot-master/belt.py` to execute. The script logs available ports, sensor state, and other info.

### 3. Dobot Library (`pydobotplus/dobotplus.py`)

- **Purpose:**
  Provides all the low-level functions to control the Dobot, including movement, IO, conveyor, and sensors.
- **Key Features:**
  - Serial communication with Dobot.
  - Functions for moving the arm, controlling the end effector, and reading sensors.
  - IR sensor support via `set_ir()` and `get_ir()`.

---

## Running the Project

1. **Connect the Dobot and accessories.**
2. **Check which serial ports your Dobot appears on:**
   ```bash
   python3 -c "from serial.tools import list_ports; print([p.device for p in list_ports.comports()])"
   ```
   Update the `PORT` variable in the scripts if needed.

3. **Run the Dobot pick-and-place script:**
   ```bash
   python3 pydobot-master/nfc_pickup.py
   ```
   This will move the arm and operate the suction cup as described.

4. **Run the conveyor and IR sensor script:**
   ```bash
   python3 pydobot-master/belt.py
   ```
   This will start the conveyor and print the IR sensor state.

---

## Troubleshooting

- **IR sensor always returns `True`:**
  - The sensor reading may need adjustment in `pydobotplus/dobotplus.py`. Print the raw sensor value and check your wiring.
  - Try changing the unpacking in `get_ir()` from `'?'` to `'B'` and see what value is returned.

- **Serial port not found:**
  - Make sure the Dobot is connected and powered on.
  - Use `ls /dev/ttyACM*` to see available ports.

- **Permission denied on serial port:**
  - Add your user to the `dialout` group or run with `sudo`.

---

## Notes

- **Threading:**
  The scripts use Python threads to allow for multiple operations or multiple Dobots. Adjust as needed for your setup.
- **Safety:**
  Always ensure the Dobot's workspace is clear before running scripts.
- **Customization:**
  You can modify the positions and sequences in the scripts to fit your application.

---

**Enjoy automating with Dobot Magician!**
For further customization, refer to the code and comments in `pydobotplus/dobotplus.py`.
