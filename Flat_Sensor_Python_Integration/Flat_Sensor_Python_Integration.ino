#include <Arduino.h>
#include <Wire.h>
#include <ADS1115.h>

// Auto scale conversion
// Manual for library: http://lygte-info.dk/project/ADS1115Library%20UK.html
// By HKJ from lygte-info.dk


ADS1115 adc0;
ADS1115 adc1(ADS1115ADDRESS+1);

void setup() {
  Serial.begin(115200);
  Wire.begin();
  adc0.setSpeed(ADS1115_SPEED_860SPS);
  adc1.setSpeed(ADS1115_SPEED_860SPS);
}

void loop() {
  double c0 = adc0.convert(ADS1115_CHANNEL0, ADS1115_RANGE_4096);
  double c1 = adc0.convert(ADS1115_CHANNEL1, ADS1115_RANGE_4096);
  double c2 = adc0.convert(ADS1115_CHANNEL2, ADS1115_RANGE_4096);
  double c3 = adc0.convert(ADS1115_CHANNEL3, ADS1115_RANGE_4096);
  double c4 = adc1.convert(ADS1115_CHANNEL0, ADS1115_RANGE_4096);
  double c5 = adc1.convert(ADS1115_CHANNEL1, ADS1115_RANGE_4096);
  double c6 = adc1.convert(ADS1115_CHANNEL2, ADS1115_RANGE_4096);
  double c7 = adc1.convert(ADS1115_CHANNEL3, ADS1115_RANGE_4096); 
//  Serial.print(millis());
//  Serial.print(" ");
  Serial.print('s');
  Serial.print(c0*0.125);
  Serial.print(" ");
  Serial.print(c1*0.125);
  Serial.print(" ");
  Serial.print(c2*0.125);
  Serial.print(" ");
  Serial.print(c3*0.125);
  Serial.print(" ");
  Serial.print(c4*0.125);
  Serial.print(" ");
  Serial.print(c5*0.125);
  Serial.print(" ");
  Serial.print(c6*0.125);
  Serial.print(" ");
  Serial.println(c7*0.125);
}
