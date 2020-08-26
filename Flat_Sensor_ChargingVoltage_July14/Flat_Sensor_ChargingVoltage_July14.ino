// version Aug 14:
// Fatigue testing data recording
// record 30seconds every 30 min interval

// version July14:
// Absolute voltage reading on 8 channels
// time recording

// version July10:
// added another ADS1115 with address of 0x49

// version Jun10:
// Removed the smooth
// display bits reading
// changed Gain from one to two
// AC: 2ms on, 2ms off

#include <Wire.h>
#include <Adafruit_ADS1015.h>

Adafruit_ADS1115 ads1115_0(0x48);
Adafruit_ADS1115 ads1115_1(0x49);

double threshold0 = 0, threshold1 = 0, threshold2 = 0, threshold3 = 0,threshold4 = 0,threshold5 = 0,threshold6 = 0,threshold7 = 0;
int16_t results0, results1, results2, results3, results4, results5, results6, results7;
int16_t vdd;

unsigned long t;


void setup(void)
{
  Serial.begin(2000000);
//  Serial.println("Hello!");
//  Serial.println("Getting differential reading from AIN0 (P) and AIN1 (N)");
//  Serial.println("ADC Range: +/- 4.096V (1 bit = 125uV)");
//  Serial.println("ADC Range: +/- 2.048V (1 bit = 063uV)");

  // The ADC input range (or gain) can be changed via the following
  // functions, but be careful never to exceed VDD +0.3V max, or to
  // exceed the upper and lower limits if you adjust the input range!
  // Setting these values incorrectly may destroy your ADC!
  //                                                                ADS1015  ADS1115
  //                                                                -------  -------
  // ads.setGain(GAIN_TWOTHIRDS);  // 2/3x gain +/- 6.144V  1 bit = 3mV      0.1875mV (default)
  // ads.setGain(GAIN_ONE);        // 1x gain   +/- 4.096V  1 bit = 2mV      0.125mV
  // ads.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  // ads.setGain(GAIN_FOUR);       // 4x gain   +/- 1.024V  1 bit = 0.5mV    0.03125mV
  // ads.setGain(GAIN_EIGHT);      // 8x gain   +/- 0.512V  1 bit = 0.25mV   0.015625mV
  // ads.setGain(GAIN_SIXTEEN);    // 16x gain  +/- 0.256V  1 bit = 0.125mV  0.0078125mV

  ads1115_0.begin();
  ads1115_1.begin();
  ads1115_0.setGain(GAIN_ONE);
  ads1115_1.setGain(GAIN_ONE);
  pinMode(6, INPUT);
  pinMode(7, OUTPUT);
}

void loop(void)
{

  // record 30 seconds of data
  t = millis();
  while(millis() - t < 30000){
  digitalWrite(7, HIGH);

//t = millis();
//Serial.print(t/1000.0);
//Serial.print(' ');
  results0 = ads1115_0.readADC_SingleEnded(0);
  results1 = ads1115_0.readADC_SingleEnded(1);
  results2 = ads1115_0.readADC_SingleEnded(2);
  results3 = ads1115_0.readADC_SingleEnded(3);
  results4 = ads1115_1.readADC_SingleEnded(0);
  results5 = ads1115_1.readADC_SingleEnded(1);
  results6 = ads1115_1.readADC_SingleEnded(2);
  results7 = ads1115_1.readADC_SingleEnded(3);

//Serial.print((millis()-t)/1000);
//Serial.print(' ');
Serial.print((results0-threshold0)*0.125);
Serial.print(' ');
Serial.print((results1-threshold1)*0.125);
Serial.print(' ');
Serial.print((results2-threshold2)*0.125);
Serial.print(' ');
Serial.print((results3-threshold3)*0.125);
Serial.print(' '); 
Serial.print((results4-threshold4)*0.125);
Serial.print(' ');
Serial.print((results5-threshold5)*0.125);
Serial.print(' ');
Serial.print((results6-threshold6)*0.125);
Serial.print(' ');
Serial.println((results7-threshold7)*0.125); 
//Serial.print(' ');
//Serial.println(buttonState); 
//  Serial.println("mV)");
  delay(2);
}

Serial.println("***");

  // half hour timer
  t = millis();
  while(millis() - t < 1800000){
    
  }

}
