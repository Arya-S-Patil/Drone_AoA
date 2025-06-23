print("Starting main.py", flush=True)

import socket
import os
import threading
import time
from flask import Flask, request, send_from_directory
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision

# Load .env variables
load_dotenv()
token = os.getenv("INFLUXDB_TOKEN")
org = os.getenv("INFLUXDB_ORG")
bucket = os.getenv("BUCKET_UUDP")
url = os.getenv("INFLUXDB_HOST")

print("Loaded env variables", flush=True)

# InfluxDB Client
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api()
print("[+] InfluxDB client ready", flush=True)

# Global drone state
drone_position = {"active": False, "x": 0, "y": 0, "z": 0}

# Flask setup
app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/position', methods=['POST'])
def update_position():
    global drone_position
    data = request.json
    if data.get("active"):
        drone_position.update({
            "x": float(data["x"]),
            "y": float(data["y"]),
            "z": float(data["z"]),
            "active": True
        })
        print(f"[UI] Activated logging at X={data['x']}, Y={data['y']}, Z={data['z']}", flush=True)
    else:
        drone_position["active"] = False
        print("[UI] Logging stopped by user", flush=True)
    return {"status": "ok"}

# UDP Listener
def listen_udp():
    UDP_IP = "0.0.0.0"
    UDP_PORT = 5333
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print(f"[+] Listening for UDP packets on port {UDP_PORT}...", flush=True)

    while True:
        data, addr = sock.recvfrom(2048)
        message = data.decode().strip()
        print(f"[UDP] {addr}: {message}", flush=True)

        if message.startswith("+UUDF:") and drone_position["active"]:
            try:
                parts = message.split(":")[1].split(",")
                mac = parts[0]
                rssi = int(parts[1])
                azimuth = int(parts[2])
                elevation = int(parts[3])
                antenna = int(parts[4])
                channel = int(parts[5])
                peer_mac = parts[6].replace('"', '')

                point = (
                    Point("uudp_packet")
                    .tag("mac", mac)
                    .tag("peer_mac", peer_mac)
                    .field("rssi", rssi)
                    .field("azimuth", azimuth)
                    .field("elevation", elevation)
                    .field("antenna", antenna)
                    .field("channel", channel)
                    .field("drone_x", drone_position["x"])
                    .field("drone_y", drone_position["y"])
                    .field("drone_z", drone_position["z"])
                    .time(time.time_ns(), WritePrecision.NS)
                )

                write_api.write(bucket=bucket, org=org, record=point)
                print("[+] Data written with drone position", flush=True)

            except Exception as e:
                print("[!] Error parsing UDP message:", e, flush=True)
        else:
            print("[-] Ignored packet (inactive or invalid format)", flush=True)

# Start UDP listener
threading.Thread(target=listen_udp, daemon=True).start()

# Start Flask server
if __name__ == '__main__':
    print("[+] Starting Flask server on http://localhost:5000", flush=True)
    app.run(port=5000)
