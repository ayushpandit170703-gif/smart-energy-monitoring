import boto3
import matplotlib.pyplot as plt
import json

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('EnergyReadings')

# Scan table
response = table.scan()
items = response['Items']

# Sort by timestamp
items.sort(key=lambda x: x['timestamp'])
items = items[-30:]

timestamps = []
voltages = []
currents = []
powers = []

for item in items:
    payload = item['payload']
    
    # If payload is a string, parse it as JSON
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except Exception:
            continue
    
    # Now extract values if they exist
    timestamps.append(item['timestamp'])
    voltages.append(float(payload.get('voltage', 0)))
    currents.append(float(payload.get('current', 0)))
    powers.append(float(payload.get('power', 0)))

# Plot
plt.figure(figsize=(10,6))
plt.plot(timestamps, voltages, label="Voltage (V)", marker='o')
plt.plot(timestamps, currents, label="Current (A)", marker='x')
plt.plot(timestamps, powers, label="Power (W)", marker='s')
plt.legend()
plt.xticks(rotation=45)
plt.title("Smart Energy Monitoring Readings")
plt.xlabel("Timestamp")
plt.ylabel("Values")
plt.tight_layout()
plt.show()
