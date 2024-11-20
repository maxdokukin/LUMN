from flask import Flask, render_template, request, jsonify
from flask_scss import Scss

app = Flask(__name__)
Scss(app)

# In-memory database to store device information and pending commands
devices = {}

# Route to serve JSON data
@app.route('/get_info', methods=['POST'])
def up_data():
    data = request.json  # Receive JSON data from the frontend

    # Update the devices dictionary with new values
    devices['r'] = data.get('r', devices.get('r', 255))
    devices['g'] = data.get('g', devices.get('g', 255))
    devices['b'] = data.get('b', devices.get('b', 255))
    devices['brightness'] = data.get('brightness', devices.get('brightness', 100))
    devices['state'] = 1 if data.get('state', devices.get('state', 0)) == 1 else 0
    devices['mode'] = 1 if data.get('mode', devices.get('mode', 0)) == 1 else 0

    return jsonify({"success": True, "message": "Data updated successfully"}), 200

@app.route('/get_data')
def get_data():
    return jsonify({
        "r": devices.get('r', 255),
        "g": devices.get('g', 255),
        "b": devices.get('b', 255),
        "brightness": devices.get('brightness', 100),
        "state": devices.get('state', 1),  # Serve as 0 or 1
        "mode": devices.get('mode', 1)    # Serve as 0 or 1
    })

# Route to render the index page and handle form submissions
@app.route("/", methods=['GET', 'POST'])
def index():
    color = '#ff0000'
    state = "OFF"  # Default
    brightness = 50
    mode = "Manual"

    if request.method == "POST":
        # Get the selected color and switch state from the form
        color = request.form.get("color")
        state = "ON" if request.form.get("state") == "on" else "OFF"
        brightness = int(request.form.get("brightness", 50))
        mode = "Automatic" if request.form.get("mode") == "on" else "Manual"
    
    return render_template("index.html", color=color, state=state, brightness=brightness, mode=mode)

if __name__ == "__main__":
    app.run(debug=True)
