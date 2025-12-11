# smart-energy-monitoring
Smart Energy Monitoring System using Arduino, ACS712, Python MQTT, AWS IoT, and DynamoDB

## 📖 Overview
This project implements a Smart Energy Monitoring System that measures voltage, current, and power in real time. It uses an Arduino UNO with an ACS712 current sensor and a voltage divider, displays readings locally on a Nokia 5110 LCD, and publishes data to AWS IoT Core via a Python MQTT gateway. Data is stored in DynamoDB and visualized using Python plots.

---

**Workflow:**
1. **Sensor** → ACS712 current sensor + voltage divider  
2. **Arduino** → Reads values, applies Raw1 − Raw2 calibration, outputs JSON  
3. **Python Gateway** → Publishes MQTT messages to AWS IoT Core  
4. **AWS IoT Core** → Routes messages to DynamoDB  
5. **DynamoDB** → Stores readings securely with timestamps  
6. **Plotting** → Python script queries DynamoDB and visualizes last 30 readings  
7. **User** → Views LCD output locally and graphs remotely  

---

## Features
- Real-time measurement of voltage, current, and power  
- Raw1 − Raw2 calibration to correct sensor offset and polarity  
- MQTT publishing with retry logic for reliability  
- Cloud storage in DynamoDB  
- Visualization of last 30 readings using Python plots  
- Local LCD display and LED status indicator  

---

## Setup Instructions

### Hardware
- Arduino UNO  
- ACS712 current sensor (5A/20A/30A variant)  
- Voltage divider circuit  
- Nokia 5110 LCD  
- Breadboard + jumper wires  

### Software
- Arduino IDE  
- Python 3.x  
- Libraries: `paho-mqtt`, `boto3`, `matplotlib`  

### Steps
1. Upload `energy_monitor.ino` to Arduino.  
2. Run `mqtt_gateway.py` to publish data to AWS IoT Core.  
3. Verify DynamoDB entries.  
4. Run `plot_dynamodb.py` to visualize readings.  

---


