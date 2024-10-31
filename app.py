#imports
from flask import Flask, render_template, request
from flask_scss import Scss
#from flask_sqlalchemy import SQLAlchemy

 #my app
app = Flask(__name__)
Scss(app)

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


if __name__ in "__main__":
    app.run(debug=True)