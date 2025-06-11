from pydobotplus import Dobot, PORT_GP4

device = Dobot(port='COM3')  # Replace with your actual port

# Enable the IR sensor on port GP4
device.set_ir(enable=True, port=PORT_GP4)

# Poll the IR sensor state in a loop
import time
while True:
    detected = device.get_ir(port=PORT_GP4)
    if detected:
        print("Object detected!")
        # You can stop the conveyor or trigger other actions here
        break
    else:
        print("No object detected.")
    time.sleep(0.1)

device.close()