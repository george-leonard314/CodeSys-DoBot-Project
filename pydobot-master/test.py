import time
from serial.tools import list_ports
import pydobot

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[0].device  # Corrected port selection

pickup_robot = pydobot.Dobot(port='/dev/ttyACM0', verbose=True)
last_robot = pydobot.Dobot(port='/dev/ttyACM1', verbose=True)

(x, y, z, r, j1, j2, j3, j4) = last_robot.pose()
#print(f'({x},{y},{z},{r})')

init_pos = (268.1, 0.0, 52.0, 0.0)
middle_step = (215.7, 192.1, 41.2, 0.0)
nfc_tag = (200.7, 186.4, -116.8, 0.0)
tag_on_belt = (267.6, 7.7, -17.9, 0.0)

eio = last_robot.get_eio(17)
print(f"EIO: {eio}")

last_robot.set_eio(17, 01)
#device.suck(True)
#device.move_to(init_pos[0], init_pos[1], init_pos[2], init_pos[3], wait=True)
pickup_robot.suck(False)

last_robot.close()
pickup_robot.close()