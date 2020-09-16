  #include <Arduino.h>
#include <Wire.h>
#include <ADS1115.h>

// Auto scale conversion
// Manual for library: http://lygte-info.dk/project/ADS1115Library%20UK.html
// By HKJ from lygte-info.dk
double c0 = 0;
double c1 = 0;
double c2 = 0;
double c3 = 0;
double c4 = 0;
double c5 = 0;
double c6 = 0;
double c7 = 0;

double c0out = 0;
double c1out = 0;
double c2out = 0;
double c3out = 0;
double c4out = 0;
double c5out = 0;
double c6out = 0;
double c7out = 0;

double const1 = 0.0;
double const2 = 1 - const1;
int first = 1;

ADS1115 adc0;
ADS1115 adc1(ADS1115ADDRESS + 1);

void setup() {
  Serial.begin(2000000);
  Wire.begin();
  adc0.setSpeed(ADS1115_SPEED_860SPS);
  adc1.setSpeed(ADS1115_SPEED_860SPS);
  delay(50);
}

void loop() {
  c0 = adc0.convert(ADS1115_CHANNEL0, ADS1115_RANGE_4096);
  c1 = adc0.convert(ADS1115_CHANNEL1, ADS1115_RANGE_4096);
  c2 = adc0.convert(ADS1115_CHANNEL2, ADS1115_RANGE_4096);
  c3 = adc0.convert(ADS1115_CHANNEL3, ADS1115_RANGE_4096);
  c4 = adc1.convert(ADS1115_CHANNEL0, ADS1115_RANGE_4096);
  c5 = adc1.convert(ADS1115_CHANNEL1, ADS1115_RANGE_4096);
  c6 = adc1.convert(ADS1115_CHANNEL2, ADS1115_RANGE_4096);
  c7 = adc1.convert(ADS1115_CHANNEL3, ADS1115_RANGE_4096);
  //  Serial.print(millis());
  //  Serial.print(" ");

  if (first) {
    c0out = c0;
    c1out = c1;
    c2out = c2;
    c3out = c3;
    c4out = c4;
    c5out = c5;
    c6out = c6;
    c7out = c7;
    first = 0;
  }
  else {
    c0out = c0out * const1 + c0 * const2;
    c1out = c1out * const1 + c1 * const2;
    c2out = c2out * const1 + c2 * const2;
    c3out = c3out * const1 + c3 * const2;
    c4out = c4out * const1 + c4 * const2;
    c5out = c5out * const1 + c5 * const2;
    c6out = c6out * const1 + c6 * const2;
    c7out = c7out * const1 + c7 * const2;
  }



  Serial.print("k ");
  Serial.print(c0out * 0.125);
  Serial.print(" ");
  Serial.print(c1out * 0.125);
  Serial.print(" ");
  Serial.print(c2out * 0.125);
  Serial.print(" ");
  Serial.print(c3out * 0.125);
  Serial.print(" ");
  Serial.print(c4out * 0.125);
  Serial.print(" ");
  Serial.print(c5out * 0.125);
  Serial.print(" ");
  Serial.print(c6out * 0.125);
  Serial.print(" ");
  Serial.print(c7out * 0.125);
  Serial.println(" ");
  Serial.print("-----------");
}
