import socket
import time

# UDP configuration from the uploaded image
ROBOT_IP = "192.168.0.20"  # From Socka Server Address
UDP_PORT = 8899          # From Socka Port
PROTOCOL = "UDP"         # Using UDP-Server as shown

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)  # Set timeout for receive operations

# Function to send commands
def send_command(cmd):
    sock.sendto(cmd.encode(), (ROBOT_IP, UDP_PORT))
    try:
        response, _ = sock.recvfrom(1024)
        return response.decode().strip()
    except socket.timeout:
        print("No response received")
        return None

# Connect and enable robot
send_command("ConnectRobot()")
send_command("EnableRobot()")
time.sleep(1)

# Get current position
pose_data = send_command("GetPose()")
if pose_data:
    x, y, z, r = map(float, pose_data.split(',')[:4])
    print(f"Current position: X:{x} Y:{y} Z:{z} R:{r}")

    # Movement sequence
    send_command(f"MovJ({x},{y-50},{z},{r})")
    time.sleep(2)  # Wait for movement completion

    # Return to original position
    send_command(f"MovJ({x},{y},{z},{r})")
    time.sleep(1)

# Cleanup
send_command("DisconnectRobot()")
sock.close()
