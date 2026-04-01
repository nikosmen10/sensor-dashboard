from flask import Flask, render_template, jsonify, send_file
import csv
import time
import random

app = Flask(__name__)

DATA_FILE = "data.csv"
THRESHOLD = 80

# Create CSV file if not exists
def init_file():
    try:
        with open(DATA_FILE, "x", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["time", "temperature", "pressure", "vibration"])
    except:
        pass

init_file()

# Generate sensor data (demo or replace with real sensors)
def generate_data():
    sensors = {
        "temperature": round(random.uniform(20, 100), 2),
        "pressure": round(random.uniform(1, 10), 2),
        "vibration": round(random.uniform(0, 5), 2)
    }

    timestamp = time.strftime("%H:%M:%S")

    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp,
            sensors["temperature"],
            sensors["pressure"],
            sensors["vibration"]
        ])

    alert = sensors["temperature"] > THRESHOLD

    return {
        "time": timestamp,
        "sensors": sensors,
        "alert": alert
    }

# MAIN PAGE (NO LOGIN)
@app.route("/")
def index():
    return render_template("index.html")

# DATA API
@app.route("/data")
def data():
    return jsonify(generate_data())

# EXPORT CSV
@app.route("/export")
def export():
    return send_file(DATA_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)