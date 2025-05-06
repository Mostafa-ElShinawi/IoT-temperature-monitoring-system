# IoT Temperature Monitoring System 🌡️

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![MicroPython](https://img.shields.io/badge/MicroPython-1.20-green)](https://micropython.org)

Real-time temperature monitoring with ESP8266 modules and Python server

![System Demo](media/Circuit_with_IoT_integration.mp4) 
[![Dashboard Preview](media/thingsboard_dashboard.png)](media/thingsboard_dashboard.png)

## Quick Start
```bash
# Clone repository
git clone https://github.com/yourusername/IoT-Temperature-System.git

# Install dependencies
pip install -r requirements.txt

# Run server
python server.py
```

## File Structure
| File/Folder       | Description                          |
|-------------------|--------------------------------------|
| `client.py`       | MicroPython code for ESP8266 modules |
| `server.py`       | Python server for data processing    |
| `media/`          | Demo video and visual assets         |

## Key Components

### 🔌 Client Code (`client.py`)
```python
# Sensor reading example
import dht
from machine import Pin

def get_readings():
    sensor = dht.DHT11(Pin(2))
    sensor.measure()
    return sensor.temperature(), sensor.humidity()
```

### 💻 Server Code (`server.py`)
```python
# Alert system example
def check_thresholds(temp):
    if temp < 15:
        return "LOW"
    elif temp > 30:
        return "HIGH"
    return "NORMAL"
```

## Demo Video
Watch the system in action: [Circuit Demo](media/Circuit_with_IoT_integration.mp4)

---

