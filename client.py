import dht
import machine
import time
import network
import urequests  # To make HTTP requests

# Setup DHT sensor on GPIO pin (D2)
sensor = dht.DHT11(machine.Pin(2))  # D2 = GPIO4
print("DHT11 Sensor initialized.")

# ThingsBoard Device Token
THINGSBOARD_TOKEN = "CDc55T7WKYLu0AHqs0wI"  # Replace with your ThingsBoard Access Token
THINGSBOARD_URL = "http://demo.thingsboard.io/api/v1/" + THINGSBOARD_TOKEN + "/telemetry"

# Wi-Fi credentials
SSID = ""
PASSWORD = ""

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Connecting to Wi-Fi network '{SSID}'...")
        wlan.connect(SSID, PASSWORD)

        attempt = 0
        while not wlan.isconnected():
            time.sleep(2)
            attempt += 1
            print(f"Connecting to Wi-Fi... Attempt {attempt}")
            if attempt > 10:  # Stop trying after 10 attempts
                print("Failed to connect to Wi-Fi. Check credentials and signal.")
                return False

    print("Connected to Wi-Fi!")
    print(f"Device IP Address: {wlan.ifconfig()[0]}")
    return True

def read_sensor():
    try:
        sensor.measure()
        temp = sensor.temperature()  # in Celsius
        humidity = sensor.humidity()  # in %
        print(f"Sensor Readings - Temp: {temp}°C, Humidity: {humidity}%")
        return temp, humidity
    except OSError as e:
        print(f"Sensor read error: {e}")
        return None, None

def send_to_thingsboard(temp, humidity):
    data = {"temperature": temp, "humidity": humidity}
    try:
        print(f"Sending data to ThingsBoard: {data}")
        response = urequests.post(THINGSBOARD_URL, json=data)
        print(f"Response: {response.status_code}, {response.text}")
        response.close()
    except Exception as e:
        print(f"Failed to send data to ThingsBoard: {e}")

def start_client():
    if not connect_wifi():
        print("Failed to connect to Wi-Fi. Exiting.")
        return

    while True:
        temp, humidity = read_sensor()
        if temp is not None and humidity is not None:
            send_to_thingsboard(temp, humidity)
        time.sleep(10)  # Adjust as needed for your update frequency

start_client()


