import json
import time
import serial
import ssl
import paho.mqtt.client as mqtt

# ---------------- AWS IoT CONFIG ----------------
AWS_ENDPOINT = "a2gb9g0qvftyyt-ats.iot.us-east-2.amazonaws.com"
CA_CERT = "AmazonRootCA1.pem"
CERTFILE = "bdafed31a3f4086a76ad7a934fbfb95f74cccb81c623ae47229eef5dcc492ee5-certificate.pem.crt"
KEYFILE = "bdafed31a3f4086a76ad7a934fbfb95f74cccb81c623ae47229eef5dcc492ee5-private.pem.key"

TOPIC = "smart/energy/data"

# ---------------- SERIAL CONFIG ----------------
SERIAL_PORT = "COM4"
BAUD = 115200

# ---------------- MQTT CALLBACKS ----------------
def on_connect(client, userdata, flags, rc, properties=None):
    print("✔ AWS IoT Connected with result code:", rc)

def on_publish(client, userdata, mid, properties=None):
    print("✔ Message published with ID:", mid)

def on_log(client, userdata, level, buf):
    print("LOG:", buf)

# ---------------- MQTT SETUP ----------------
client = mqtt.Client(protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_publish = on_publish
client.on_log = on_log

client.tls_set(
    ca_certs=CA_CERT,
    certfile=CERTFILE,
    keyfile=KEYFILE,
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLSv1_2
)

print("Connecting to:", AWS_ENDPOINT)
client.connect(AWS_ENDPOINT, 8883, 60)
client.loop_start()

# ---------------- SERIAL SETUP ----------------
try:
    ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)
    print("✔ Connected to Arduino on", SERIAL_PORT)
except Exception as e:
    print("❌ ERROR: Cannot open serial port", SERIAL_PORT, e)
    exit()

print("⌛ Waiting for Arduino to reboot...")
time.sleep(2)
print("Entering main loop...")

# ---------------- MAIN LOOP ----------------
while True:
    try:
        raw = ser.readline().decode(errors="ignore").strip()

        if not raw:
            print("… waiting for data")
            time.sleep(0.3)
            continue

        print("Arduino sent:", raw)

        # Parse JSON from Arduino
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            print("❌ Bad JSON, skipping")
            continue

        # Add timestamp
        data["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        payload = json.dumps(data)

        print("→ Publishing:", payload)
        client.publish(TOPIC, payload)

    except Exception as e:
        print("❌ MAIN LOOP ERROR:", e)
        time.sleep(1)
