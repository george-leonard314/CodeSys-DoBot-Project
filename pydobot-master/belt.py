#!/usr/bin/env python3
"""
run_conveyor.py

Continuously run the Dobot Magician's conveyor belt until the IR sensor on GP4
detects an object, then stop, pause, and repeat.
"""

import time
import logging
from serial.tools import list_ports
from pydobotplus import Dobot

# -- USER CONFIGURATION -------------------------------------------------------
PORT            = '/dev/ttyACM1'  # Adjust to your Dobot's port
BELT_SPEED      = 1.0             # 0.0–1.0 (fraction of max speed)
PAUSE_AFTER_STOP= 0.5             # Seconds to wait after stopping
POLL_INTERVAL   = 0.05            # Sensor poll interval (s)
PORT_GP4        = "GP4"           # Add this line if not already defined

# -- LOGGING SETUP ------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)5s: %(message)s',
    datefmt='%H:%M:%S'
)

def main():
    # 1. Verify port exists
    available = [p.device for p in list_ports.comports()]
    logging.info(f"Available serial ports: {available}")
    if PORT not in available:
        logging.error(f"Port {PORT} not found. Update PORT variable.")
        return

    # 2. Connect
    try:
        device = Dobot(port=PORT)
    except Exception as e:
        logging.error(f"Failed to open {PORT}: {e}")
        return

    logging.info("Connected to Dobot Magician")

    # 3. Enable the IR sensor on GP4
    sensor = device.set_ir(enable=True, port=4)
    logging.info(f"sensor: {sensor}")
    #device.move_to(268.1, 0.0, 52.0, 0.0, wait=True)  # Move to home position

    try:
        while True:
            # Start the conveyor belt
            device.conveyor_belt(speed=BELT_SPEED, direction=1)
            logging.info("Conveyor belt running...")

            # Poll IR sensor until object detected
            while True:
                state = device.get_ir()
                # If object detected (assuming state==1 means detected; adjust if needed)
                if state == True:
                    logging.info("Object detected by IR sensor! Stopping belt.")
                    print(state)
                    device.conveyor_belt(speed=0.0, direction=1)
                    break
                time.sleep(POLL_INTERVAL)

            # Pause after stopping
            time.sleep(PAUSE_AFTER_STOP)
    except KeyboardInterrupt:
        logging.info("Interrupted by user. Stopping belt and exiting.")
        device.conveyor_belt(speed=0.0, direction=1)
    finally:
        device.close()

if __name__ == "__main__":
    main()