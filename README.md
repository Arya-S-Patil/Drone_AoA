

## 📡 Drone AoA UDP Logger with InfluxDB & Flask

A lightweight system to log BLE AoA (`+UUDF:`) packets from a drone **only when stationary**, using a web UI to **start/stop logging** and tag each packet with drone `x, y, z` coordinates.
Data is streamed over UDP and stored in **InfluxDB Cloud** for further analysis.

---

## 🚀 Features

* ✅ UDP listener for BLE AoA data (`+UUDF:` packets)
* ✅ Start/stop logging with a browser interface
* ✅ Custom `x`, `y`, `z` drone coordinates tagged in InfluxDB
* ✅ Uses InfluxDB Cloud v2+ with token-based auth
* ✅ Logging ignored when drone is moving (i.e., STOP pressed)
* ✅ Fully modular Python + Flask backend

---

## 🗂️ Folder Structure

```
Influx_db/
├── .env                # Your InfluxDB credentials (ignored in Git)
├── index.html          # Simple web UI (runs on http://localhost:5000)
├── main.py             # Flask server + UDP listener
└── requirements.txt    # Python dependencies
```

---

## 🧠 Logging Logic

| Button Pressed | Behavior                       | What Happens                          |
| -------------- | ------------------------------ | ------------------------------------- |
| **SEND**       | Start logging with given X/Y/Z | Incoming UDP data is logged to Influx |
| **STOP**       | Stop logging                   | UDP data is ignored                   |
| No Press       | Nothing logged                 | No data is written                    |

> Logging resumes only after **SEND** is pressed again.

---

## ☁️ InfluxDB Cloud Setup 

### 1️⃣ Sign up at Cloud 3 version

### 2️⃣ Create:

* An **organization** name 
* A **bucket** 
* A **token** 
### 3️⃣ Copy the **cloud URL**
`https://us-east-1-1.aws.cloud2.influxdata.com`

---

## 🔐 .env File 

Create a file `.env` inside your project root with the following:

```env
INFLUXDB_TOKEN=your-token-here
INFLUXDB_ORG=your-org-name
INFLUXDB_HOST=XYZ
BUCKET_UUDP=X
```


---

## ✅ How to Run

```bash
cd Influx_db
pip install -r requirements.txt
python main.py
```

Then open:
🌐 [http://localhost:5000](http://localhost:5000)
and use the web UI to send/stop logging.

---

## 💾 Sample Data Format in InfluxDB

Each data point is stored like this:

| Field        | Value        |
| ------------ | ------------ |
| mac          | BLE tag MAC  |
| rssi         | -55          |
| azimuth      | 33           |
| elevation    | 12           |
| antenna      | 3            |
| channel      | 37           |
| peer\_mac    | anchor MAC   |
| drone\_x/y/z | from user UI |

---

## 🛠 Requirements

* Python 3.8+
* A valid InfluxDB Cloud account

Install dependencies:

```bash
pip install -r requirements.txt
```


