from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

# In-memory database to store device information and pending commands
devices = {}

# Endpoint to receive heartbeat and store the device IP
@app.route('/esp_heartbeat', methods=['POST'])
def esp_heartbeat():
    data = request.get_json()
    device_id = data.get("device_id")
    device_ip = data.get("ip")

    if not device_id or not device_ip:
        return jsonify({"error": "Device ID and IP required"}), 400

    # Update or register device info with default properties
    if device_id not in devices:
        devices[device_id] = {
            "ip": device_ip,
            "pending_command": None,
            "rgb": [255, 255, 255],  # Default white color
            "brightness": 255,       # Default brightness 100%
            "mode": 1,        # Default mode
            "state": 1            # Default state
        }
    else:
        devices[device_id]["ip"] = device_ip

    return jsonify({"status": "Heartbeat received", "device_id": device_id})

# Endpoint to poll for commands and device state
@app.route('/esp_commands', methods=['GET'])
def esp_commands():
    device_id = request.args.get("device_id")

    if not device_id or device_id not in devices:
        return jsonify({"error": "Unknown or missing device ID"}), 400

    device = devices[device_id]
    response = {
        "command": device.get("pending_command"),
        "rgb": device["rgb"],
        "brightness": device["brightness"],
        "mode": device["mode"],
        "state": device["state"]
    }

    # Clear command after sending it to device
    device["pending_command"] = None
    return jsonify(response)

# Admin endpoint to set a command or update properties for a specific device
@app.route('/set_command', methods=['POST'])
def set_command():
    data = request.get_json()
    device_id = data.get("device_id")
    command = data.get("command")
    rgb = data.get("rgb")
    brightness = data.get("brightness")
    mode = data.get("mode")
    state = data.get("state")

    if device_id not in devices:
        return jsonify({"error": "Device not registered"}), 400

    # Update device command and properties
    if command:
        devices[device_id]["pending_command"] = command
    if rgb:
        devices[device_id]["rgb"] = rgb
    if brightness is not None:
        devices[device_id]["brightness"] = brightness
    if mode:
        devices[device_id]["mode"] = mode
    if state:
        devices[device_id]["state"] = state

    return jsonify({"status": "Command and properties set", "device_id": device_id})

@app.route('/')
def main():
    return "Hi"

# Run Flask server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

