FROM python:3.11-slim

# Install system dependencies for serial communication
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libusb-1.0-0-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY dobots_mqtt_control.py .

# Expose serial ports (actual device mapping happens at runtime)
ENV DEVICE_1=/dev/ttyACM0
ENV DEVICE_2=/dev/ttyACM1

CMD ["python", "dobots_mqtt_control.py"]
