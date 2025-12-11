#include <Adafruit_GFX.h>
#include <Adafruit_PCD8544.h>

// Nokia 5110 LCD pins (adjust if wired differently)
Adafruit_PCD8544 display = Adafruit_PCD8544(8, 7, 6, 5, 4);

// Analog pins
const int voltagePin = A0;   // voltage sensor/divider output
const int currentPin = A1;   // ACS712 output (Raw1)
const int refPin     = A2;   // 2.5 V reference from resistor divider (Raw2)

// Scaling/config
const float ADC_LSB     = 5.0 / 1023.0; // UNO default analog reference
const float voltageScale = 5.0;         // adjust to your divider ratio (e.g., 5 or 25)
const float sensitivity  = 0.100;       // ACS712-20A; use 0.185 for 5A, 0.066 for 30A

void setup() {
  Serial.begin(115200);
  display.begin();
  display.setContrast(50);

  // Optional: small settling delay
  delay(100);
}

void loop() {
  // Read voltage (scaled by your divider)
  int rawV = analogRead(voltagePin);
  float voltage = rawV * ADC_LSB * voltageScale;

  // Read current with Raw1 - Raw2 to remove offset
  int rawI   = analogRead(currentPin);  // ACS712 output
  int rawRef = analogRead(refPin);      // 2.5 V reference
  int rawDiff = rawI - rawRef;

  // Convert to volts difference, then to amps
  float deltaV  = rawDiff * ADC_LSB;    // volts around mid-rail
  float current = deltaV / sensitivity; // signed current (A)

  // Power (signed). If you expect only consumption, you can show abs(power).
  float power = voltage * current;

  // LCD output
  display.clearDisplay();
  display.setCursor(0, 0);
  display.print("V: "); display.println(voltage, 2);
  display.print("I: "); display.println(current, 2);
  display.print("P: "); display.println(power, 2);
  display.display();

  // JSON over Serial
  Serial.print("{\"device_id\":\"uno1\"");
  Serial.print(",\"voltage\":"); Serial.print(voltage, 2);
  Serial.print(",\"current\":"); Serial.print(current, 2);
  Serial.print(",\"power\":");   Serial.print(power, 2);
  Serial.println("}");

  delay(500);
}
