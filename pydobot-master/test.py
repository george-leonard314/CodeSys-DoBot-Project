from serial.tools import list_ports
import pydobot
import threading
import time

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')

def control_dobot(port):
    device = pydobot.Dobot(port=port, verbose=True)
    
    # Get current position
    (x, y, z, r, j1, j2, j3, j4) = (186.1, 211.9, -117.2, 64.2, 48.7, 89.1, 54.2, 15.5)
    print(f'{port} -> Initial position: x:{x} y:{y} z:{z}')
    
    # Move to target position (50mm left and 50mm up from current position)
    target_x = x - 50
    target_y = y
    target_z = z + 50
    device.move_to(x, y, z, r, wait=True)
    print(f"Moved to target position: x:{target_x} y:{target_y} z:{target_z}")
    
    # Activate suction cup (enable control + enable suction)
    device.suck(True)  # Or use direct command: device.set_end_effector_suction_cup(True, True)
    print("Suction cup activated")
    
    # Hold suction for 2 seconds (adjust as needed)
    time.sleep(1)
    
    device.move_to(244.90731811523438,-29.21633529663086,-11.619270324707031,8.721089363098145, wait=True)
    device.suck(False)
    device.move_to(244.90731811523438,-29.21633529663086,26.393142700195312,8.721089363098145, wait=True)
    print("Product on the line")
    
    device.close()

# Create and start threads
thread1 = threading.Thread(target=control_dobot, args=('/dev/ttyACM0',))
thread1.start()
thread1.join()
