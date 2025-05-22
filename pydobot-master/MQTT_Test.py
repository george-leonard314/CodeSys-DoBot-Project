import paho.mqtt.client as mqtt
import time
from datetime import datetime
from serial.tools import list_ports
import pydobot
import threading

#DOBOT Configurations
available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')

def control_dobot(port):
    device = pydobot.Dobot(port=port, verbose=True)
    (x, y, z, r, j1, j2, j3, j4) = device.pose()
    print(f'{port} -> x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')
    for i in range(10):
        device.move_to(x, y - 50, z + 50, r, wait=True)
        time.sleep(0.5)

        device.move_to(x, y +75, z - 50, r, wait=True)
        time.sleep(0.5)
    device.move_to(x, y, z, r, wait=True)

    device.close()

#MQTT Configuration
BROKER_IP = "192.168.0.25"
PORT = 1883
TOPIC = "robots/start"
USERNAME = "robot"
PASSWORD = "Sarmale.1808"
CLIENT_ID = f"robot-client-{time.time()}"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[{datetime.now()}] Connected to {BROKER_IP}")
        client.subscribe(TOPIC)
        print(f"[{datetime.now()}] Subscribed to {TOPIC}")
    else:
        error_messages = {
            1: "Incorrect protocol version",
            2: "Invalid client identifier",
            3: "Server unavailable",
            4: "Bad username/password",
            5: "Not authorized"
        }
        print(f"[{datetime.now()}] Connection failed: {error_messages.get(rc, f'Unknown error {rc}')}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"\n[{datetime.now()}] Message received on {msg.topic}:")
    print(f"Payload: {payload}")
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
    # Add your robot start logic here

def main():
    client = mqtt.Client(client_id=CLIENT_ID)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"[{datetime.now()}] Connecting to {BROKER_IP}...")
    
    try:
        client.connect(BROKER_IP, PORT, 60)
        client.loop_forever()
    except Exception as e:
        print(f"[{datetime.now()}] Connection error: {str(e)}")
        print("Retrying in 5 seconds...")
        time.sleep(5)
        main()

if __name__ == "__main__":
    try:
        thread1 = threading.Thread(target=control_dobot, args=('/dev/ttyACM0',))
        thread2 = threading.Thread(target=control_dobot, args=('/dev/ttyACM1',))
        main()
    except KeyboardInterrupt:
        print("\nListener stopped")
