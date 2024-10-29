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

    # Update or register device info
    devices[device_id] = {
        "ip": device_ip,
        "pending_command": None
    }

    return jsonify({"status": "Heartbeat received", "device_id": device_id})

# Endpoint to poll for commands
@app.route('/esp_commands', methods=['GET'])
def esp_commands():
    device_id = request.args.get("device_id")

    if not device_id or device_id not in devices:
        return jsonify({"error": "Unknown or missing device ID"}), 400

    command = devices[device_id].get("pending_command")
    if command:
        # Clear command after sending it to device
        devices[device_id]["pending_command"] = None
        return jsonify({"command": command})
    else:
        return jsonify({"command": None})

# Admin endpoint to set a command for a specific device (for testing purposes)
@app.route('/set_command', methods=['POST'])
def set_command():
    data = request.get_json()
    device_id = data.get("device_id")
    command = data.get("command")

    if device_id not in devices:
        return jsonify({"error": "Device not registered"}), 400

    # Set pending command for device
    devices[device_id]["pending_command"] = command
    return jsonify({"status": "Command set", "device_id": device_id, "command": command})

# Run Flask server
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
