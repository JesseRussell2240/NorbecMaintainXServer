# 🛠 MaintainX PLC Integration System

This project is a complete Raspberry Pi-based system that reads data from a Rockwell PLC and reports sensor data to MaintainX using their REST API. It is designed to run headlessly on boot, switch between isolated PLC and internet networks, and keep data in sync using Git for maintainability.

---

## 📦 Project Overview

**Goal**: Provide real-time data synchronization between a factory-floor Allen-Bradley PLC and the MaintainX cloud dashboard using the MaintainX Meter API.

### System Flow:
```
[PLC Sensors] → [Raspberry Pi] → [REST API via HTTPS] → [MaintainX Cloud]
```

---

## 🚀 Auto-Start Configuration on Boot

To configure the Raspberry Pi to pull updates and run `main.py` on boot:

```bash
# 1. Download and move the systemd service file
wget https://chat.openai.com/mnt/data/maintainx.service
sudo cp maintainx.service /etc/systemd/system/maintainx.service

# 2. Reload systemd to recognize the new service
sudo systemctl daemon-reexec
sudo systemctl daemon-reload

# 3. Set Git identity for the user
sudo -u NorbecMaintainXserver git config --global user.name "Jesse Russell"
sudo -u NorbecMaintainXserver git config --global user.email "jesserussell2240@users.noreply.github.com"

# 4. Enable credential caching and push manually to store token
git config --global credential.helper store
git push origin main

# 5. Enable and start the service
sudo systemctl enable maintainx.service
sudo systemctl start maintainx.service
```

---

## 🛠️ Initial Installation & Dependencies

```bash
# System packages
sudo apt update
sudo apt install -y python3 python3-pip git iproute2

# Python packages
pip3 install pylogix requests python-dotenv --break-system-packages
```

---

## 🔐 Environment Configuration

```bash
# Create a .env file in your project root
nano .env
```

Paste:
```env
MAINTAINX_API_KEY=your_token_here
```

In `main.py`, replace any hardcoded key with:

```python
from dotenv import load_dotenv
load_dotenv()
BEARER_TOKEN = os.getenv("MAINTAINX_API_KEY")
```

Also add `.env` to `.gitignore` and untrack it:
```bash
echo ".env" >> .gitignore
git rm --cached .env
git commit -m "Remove .env from version control"
git push origin main
```

---

## 🧩 Updating the Sensor Database

To add new sensors to `Database.py`, you need:

- **Meter ID** from the MaintainX web app:
  - Go to `Meters > [Your Meter]`
  - Copy the ID from the URL: `.../meters/123456`
- **PLC Tag Name** from wiring diagrams or RSLogix (e.g., `PT_PNT_9F_005`)

Each entry should look like:

```python
{
  "category": "Pressure Monitor before Pump",
  "location": "Poly_2_Transfer",
  "parameter": "pressure",
  "data": {
    "meter_id": 435418,
    "tag_name": "PT_POL_7D_505",
    "last_sent_reading": None,
    "current_reading": None
  }
}
```

Append new entries to the `sensors` list in `Database.py`.

---

## 🧪 Testing & Debugging Tools

### Run data loop manually:
```bash
python3 main.py
```

### Monitor tag changes:
```bash
python3 genericTagMonitor.py
```

### Verify leak detector sensors:
```bash
python3 leakDetectUnitTest.py
```

---

## 🧠 Architecture Notes

- `main.py`: Full loop to read → compare → POST updated sensor values.
- `Database.py`: Sensor definition (all meters).
- `TankDatabase.py`: Reference metadata (limits, names).
- `genericTagMonitor.py`: Watch live PLC tag changes.
- `leakDetectUnitTest.py`: Display leak states from the database.
- `.env`: Keeps secrets out of version control.
- `maintainx.service`: systemd boot hook.

---

## 🔄 Git Sync Instructions

Use Git to manage this repo on the Pi:

```bash
git pull origin main  # to get latest
git add .
git commit -m "Update"
git push origin main
```

Ensure `.env` is excluded from pushes and protected from pulls:
```bash
git update-index --assume-unchanged .env
```

---

## ✅ Final Notes

- PLC IP is assumed to be `10.10.0.10` via `eth0`
- Internet is accessed via `eth1` or a USB-Ethernet adapter
- Network interface switching is done automatically via `ip link set`
- MaintainX API key must be valid and unexpired
- Token rate limits are handled via retry logic in `main.py`

For more, consult the [MaintainX API docs](https://api.getmaintainx.com/v1/docs/)

