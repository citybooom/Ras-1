#include <Arduino.h>
#include <Wire.h>
#include <ADS1115.h>

// Auto scale conversion
// Manual for library: http://lygte-info.dk/project/ADS1115Library%20UK.html
// By HKJ from lygte-info.dk


ADS1115 adc0;
ADS1115 adc1(ADS1115ADDRESS+1);

double c0base = 0;
double c1base = 0;
double c2base = 0;
double c3base = 0;
double c4base = 0;
double c5base = 0;
double c6base = 0;
double c7base = 0;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  adc0.setSpeed(ADS1115_SPEED_860SPS);
  adc1.setSpeed(ADS1115_SPEED_860SPS);

  c0base = adc0.convert(ADS1115_CHANNEL0, ADS1115_RANGE_4096);
  c1base = adc0.convert(ADS1115_CHANNEL1, ADS1115_RANGE_4096);
  c2base = adc0.convert(ADS1115_CHANNEL2, ADS1115_RANGE_4096);
  c3base = adc0.convert(ADS1115_CHANNEL3, ADS1115_RANGE_4096);
  c4base = adc1.convert(ADS1115_CHANNEL0, ADS1115_RANGE_4096);
  c5base = adc1.convert(ADS1115_CHANNEL1, ADS1115_RANGE_4096);
  c6base = adc1.convert(ADS1115_CHANNEL2, ADS1115_RANGE_4096);
  c7base = adc1.convert(ADS1115_CHANNEL3, ADS1115_RANGE_4096); 
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
  
  Serial.print((c0-c0base)*0.125);
  Serial.print(" ");
  Serial.print((c1-c1base)*0.125);
  Serial.print(" ");
  Serial.print((c2-c2base)*0.125);
  Serial.print(" ");
  Serial.print((c3-c3base)*0.125);
  Serial.print(" ");
  Serial.print((c4-c4base)*0.125);
  Serial.print(" ");
  Serial.print((c5-c5base)*0.125);
  Serial.print(" ");
  Serial.print((c6-c6base)*0.125);
  Serial.print(" ");
  Serial.println((c7-c7base)*0.125);
}
