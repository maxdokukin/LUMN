![logo](https://github.com/user-attachments/assets/db8cac1d-6cd5-49cf-8b4a-c0d7abeebb8f)

# ESP LED Web Server README

## Overview
This project is a Flask-based web server designed to control LED lights via an ESP32-C3 microcontroller. The server communicates with the ESP32 device through JSON APIs and provides a user-friendly interface for managing LED colors, brightness, state, and operating modes. It also generates a QR code linking to the server for easy access.

The project is deployed using Docker and Google Cloud Run, ensuring scalability and reliability.

---

## Features
- **Web Interface**: Control LED lights through an interactive web UI.
- **API Integration**:
  - `POST /get_info`: Update device state with JSON data.
  - `GET /get_data`: Retrieve current LED settings.
- **QR Code Generation**: Generates a QR code linking to the server's URL.
- **LED Control**: Supports RGB values, brightness adjustment, state toggling (ON/OFF), and mode switching (Manual/Automatic).
- **ESP32-C3 Integration**: The microcontroller pulls data from the server every 2 seconds and adjusts LEDs accordingly.

---

## Prerequisites
- Python 3.7+
- Flask and Flask-Scss libraries
- Docker
- Google Cloud SDK
- ESP32-C3 microcontroller with the appropriate firmware
- Hardware setup for LED installation (available on request)

---

## Local Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Server**:
   ```bash
   python app.py
   ```

3. **Access the Web Interface**:
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## Deployment

### Google Cloud Deployment
1. **Set Google Cloud Project**:
   ```bash
   gcloud config set project esp-led-server
   ```

2. **Build Docker Image**:
   ```bash
   docker buildx build --platform linux/amd64 -t us-west1-docker.pkg.dev/esp-led-server/esp-led-server/esp-led-server:latest .
   ```

3. **Push Docker Image**:
   ```bash
   docker push us-west1-docker.pkg.dev/esp-led-server/esp-led-server/esp-led-server:latest
   ```

4. **Deploy with Google Cloud Run**:
   ```bash
   gcloud beta run deploy esp-web-server        --image us-west1-docker.pkg.dev/esp-led-server/esp-led-server/esp-led-server:latest        --region us-west1
   ```

### Stop Deployment
To stop traffic:
```bash
gcloud run services update esp-web-server --region us-west1 --no-traffic
```

---

## API Endpoints

### 1. `POST /get_info`
- **Description**: Updates the LED configuration.
- **Input**: JSON payload with the following fields:
  - `r` (int): Red intensity (0-255).
  - `g` (int): Green intensity (0-255).
  - `b` (int): Blue intensity (0-255).
  - `brightness` (int): Brightness level (0-100).
  - `state` (int): LED state (1 for ON, 0 for OFF).
  - `mode` (int): Operating mode (1 for Automatic, 0 for Manual).
- **Response**:
  ```json
  {
    "success": true,
    "message": "Data updated successfully"
  }
  ```

### 2. `GET /get_data`
- **Description**: Retrieves the current LED settings.
- **Response**:
  ```json
  {
    "r": 255,
    "g": 255,
    "b": 255,
    "brightness": 100,
    "state": 1,
    "mode": 0
  }
  ```

### 3. `GET /qr_code`
- **Description**: Generates and serves a QR code linking to the web server.

---

## ESP32-C3 Integration
The ESP32-C3 pulls data from the `GET /get_data` endpoint every 2 seconds and adjusts the LED lights based on the received configuration.

- **Firmware**: Custom firmware compatible with the server (available upon request).
- **Hardware Installation**: Schematic available upon request.

---

## Key Files
- **`app.py`**: Flask application logic.
- **`templates/index.html`**: Web interface template.
- **`Dockerfile`**: Docker container setup.
- **`requirements.txt`**: Python dependencies.

---

## Notes
- Ensure that the ESP32-C3 device has stable Wi-Fi connectivity to reach the server.
- Configure Google Cloud permissions for successful deployment.

For firmware or hardware support, contact the project maintainer.
