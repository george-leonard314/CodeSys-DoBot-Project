from serial.tools import list_ports
from pydobotplus import Dobot
import threading
import time

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[0].device  # Corrected port selection

device = Dobot(port='/dev/ttyACM0')

#(x, y, z, r, j1, j2, j3, j4) = device.pose()
#print(f'({x},{y},{z},{r})')

init_pos = (268.1, 0.0, 52.0, 0.0)
middle_step = (215.7, 192.1, 41.2, 0.0)
nfc_tag = (176.0, 224.3, -115.6, 0.0)
tag_on_belt = (267.6, 7.7, -17.0, 0.0)


def move_nfc_on_belt():
    device.move_to(init_pos[0], init_pos[1], init_pos[2], init_pos[3], wait=True)
    device.move_to(middle_step[0], middle_step[1], middle_step[2], middle_step[3], wait=True)
    device.move_to(nfc_tag[0], nfc_tag[1], nfc_tag[2], nfc_tag[3], wait=True)
    device.suck(True)  # Or use direct command: device.set_end_effector_suction_cup(True, True)
    device.move_to(middle_step[0], middle_step[1], middle_step[2], middle_step[3], wait=True)
    device.move_to(init_pos[0], init_pos[1], init_pos[2], init_pos[3], wait=True)
    device.move_to(tag_on_belt[0], tag_on_belt[1], tag_on_belt[2], tag_on_belt[3], wait=True)
    device.suck(False)
    device.move_to(init_pos[0], init_pos[1], init_pos[2], init_pos[3], wait=True)
    device.suck(False)
    device.close()

def bring_nfc_to_senzor():
    pass

def move_nfc_from_belt():
    pass

thread1 = threading.Thread(target=move_nfc_on_belt, args=('/dev/ttyACM0',))
thread2 = threading.Thread(target=bring_nfc_to_senzor, args=('/dev/ttyACM1',))
thread3 = threading.Thread(target=move_nfc_from_belt, args=('/dev/ttyACM1',))

thread1.start()