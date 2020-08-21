#include <Wire.h>
#include <Adafruit_ADS1015.h>
Adafruit_ADS1015 ads(0x48);



float Voltage0a = 0.0;
float Voltage1a = 0.0;
float Voltage2a = 0.0;
float Voltage3a = 0.0;
float Voltage0b = 0.0;
float Voltage1b = 0.0;
float Voltage2b = 0.0;
float Voltage3b = 0.0;
float Voltage0c = 0.0;
float Voltage1c = 0.0;
float Voltage2c = 0.0;
float Voltage3c = 0.0;
float Voltage0d = 0.0;
float Voltage1d = 0.0;
float Voltage2d = 0.0;
float Voltage3d = 0.0;
float Voltage0e = 0.0;
float Voltage1e = 0.0;
float Voltage2e = 0.0;
float Voltage3e = 0.0;

float k = 50;
float correction = 100;
float total = 0.0;

int16_t adc0a;
int16_t adc1a;
int16_t adc2a;
int16_t adc3a;
int16_t adc0b;
int16_t adc1b;
int16_t adc2b;
int16_t adc3b;
int16_t adc0c;
int16_t adc1c;
int16_t adc2c;
int16_t adc3c;
int16_t adc0d;
int16_t adc1d;
int16_t adc2d;
int16_t adc3d;
int16_t adc0e;
int16_t adc1e;
int16_t adc2e;
int16_t adc3e;

int16_t adc0aold;
int16_t adc1aold;
int16_t adc2aold;
int16_t adc3aold;
int16_t adc0bold;
int16_t adc1bold;
int16_t adc2bold;
int16_t adc3bold;
int16_t adc0cold;
int16_t adc1cold;
int16_t adc2cold;
int16_t adc3cold;
int16_t adc0dold;
int16_t adc1dold;
int16_t adc2dold;
int16_t adc3dold;
int16_t adc0eold;
int16_t adc1eold;
int16_t adc2eold;
int16_t adc3eold;

int16_t base0a;
int16_t base1a;
int16_t base2a;
int16_t base3a;
int16_t base0b;
int16_t base1b;
int16_t base2b;
int16_t base3b;
int16_t base0c;
int16_t base1c;
int16_t base2c;
int16_t base3c;
int16_t base0d;
int16_t base1d;
int16_t base2d;
int16_t base3d;
int16_t base0e;
int16_t base1e;
int16_t base2e;
int16_t base3e;

int count = 0;
float diff = 0;
int basediff = 0;
int delaytime = 1;
int state = 0;
int statecount = 0;
float diffthresh = 3;

void setup(void)
{
  Serial.begin(9600);
  ads.begin();
  ads.setGain(GAIN_TWO);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);



  digitalWrite(2, HIGH);
  delay(delaytime);

  base0a = ads.readADC_SingleEnded(0);
  base1a = ads.readADC_SingleEnded(1);
  base2a = ads.readADC_SingleEnded(2);
  base3a = ads.readADC_SingleEnded(3);


  digitalWrite(2, LOW);
  digitalWrite(3, HIGH);
  delay(delaytime);


  base0b = ads.readADC_SingleEnded(0);
  base1b = ads.readADC_SingleEnded(1);
  base2b = ads.readADC_SingleEnded(2);
  base3b = ads.readADC_SingleEnded(3);


  digitalWrite(3, LOW);
  digitalWrite(4, HIGH);
  delay(delaytime);


  base0c = ads.readADC_SingleEnded(0);
  base1c = ads.readADC_SingleEnded(1);
  base2c = ads.readADC_SingleEnded(2);
  base3c = ads.readADC_SingleEnded(3);


  digitalWrite(4, LOW);
  digitalWrite(5, HIGH);
  delay(delaytime);


  base0d = ads.readADC_SingleEnded(0);
  base1d = ads.readADC_SingleEnded(1);
  base2d = ads.readADC_SingleEnded(2);
  base3d = ads.readADC_SingleEnded(3);

  digitalWrite(5, LOW);
  digitalWrite(6, HIGH);
  delay(delaytime);


  base0e = ads.readADC_SingleEnded(0);
  base1e = ads.readADC_SingleEnded(1);
  base2e = ads.readADC_SingleEnded(2);
  base3e = ads.readADC_SingleEnded(3);



}

void loop(void)
{
  digitalWrite(2, HIGH);
  digitalWrite(6, LOW);
  delay(delaytime);

  adc0aold = adc0a;
  adc1aold = adc1a;
  adc2aold = adc2a;
  adc3aold = adc3a;

  adc0a = ads.readADC_SingleEnded(0);
  adc1a = ads.readADC_SingleEnded(1);
  adc2a = ads.readADC_SingleEnded(2);
  adc3a = ads.readADC_SingleEnded(3);

  Voltage0a = ((base0a - adc0a) * 0.1875) * 0.001;
  Voltage1a = ((base1a - adc1a) * 0.1875) * 0.001;
  Voltage2a = ((base2a - adc2a) * 0.1875) * 0.001;
  Voltage3a = ((base3a - adc3a) * 0.1875) * 0.001;
  if (count < 20) {
    base0a = adc0a;
    base1a = adc1a;
    base2a = adc2a;
    base3a = adc3a;
  }

  digitalWrite(2, LOW);
  digitalWrite(3, HIGH);
  delay(delaytime);

  adc0bold = adc0b;
  adc1bold = adc1b;
  adc2bold = adc2b;
  adc3bold = adc3b;

  adc0b = ads.readADC_SingleEnded(0);
  adc1b = ads.readADC_SingleEnded(1);
  adc2b = ads.readADC_SingleEnded(2);
  adc3b = ads.readADC_SingleEnded(3);
  Voltage0b = ((base0b - adc0b) * 0.1875) / 1000;
  Voltage1b = ((base1b - adc1b) * 0.1875) / 1000;
  Voltage2b = ((base2b - adc2b) * 0.1875) / 1000;
  Voltage3b = ((base3b - adc3b) * 0.1875) / 1000;
  if (count < 20) {
    base0b = adc0b;
    base1b = adc1b;
    base2b = adc2b;
    base3b = adc3b;
  }

  digitalWrite(3, LOW);
  digitalWrite(4, HIGH);
  delay(delaytime);

  adc0cold = adc0c;
  adc1cold = adc1c;
  adc2cold = adc2c;
  adc3cold = adc3c;


  adc0c = ads.readADC_SingleEnded(0);
  adc1c = ads.readADC_SingleEnded(1);
  adc2c = ads.readADC_SingleEnded(2);
  adc3c = ads.readADC_SingleEnded(3);
  Voltage0c = ((base0c - adc0c) * 0.1875) / 1000;
  Voltage1c = ((base1c - adc1c) * 0.1875) / 1000;
  Voltage2c = ((base2c - adc2c) * 0.1875) / 1000;
  Voltage3c = ((base3c - adc3c) * 0.1875) / 1000;
  if (count < 20) {
    base0c = adc0c;
    base1c = adc1c;
    base2c = adc2c;
    base3c = adc3c;
  }


  digitalWrite(4, LOW);
  digitalWrite(5, HIGH);
  delay(delaytime);

  adc0dold = adc0d;
  adc1dold = adc1d;
  adc2dold = adc2d;
  adc3dold = adc3d;

  adc0d = ads.readADC_SingleEnded(0);
  adc1d = ads.readADC_SingleEnded(1);
  adc2d = ads.readADC_SingleEnded(2);
  adc3d = ads.readADC_SingleEnded(3);
  Voltage0d = ((base0d - adc0d) * 0.1875) / 1000;
  Voltage1d = ((base1d - adc1d) * 0.1875) / 1000;
  Voltage2d = ((base2d - adc2d) * 0.1875) / 1000;
  Voltage3d = ((base3d - adc3d) * 0.1875) / 1000;
  
  if (count < 20) {
    base0d = adc0d;
    base1d = adc1d;
    base2d = adc2d;
    base3d = adc3d;
    basediff = diff;
  }

  digitalWrite(5, LOW);
  digitalWrite(6, HIGH);
  delay(delaytime);

  adc0eold = adc0e;
  adc1eold = adc1e;
  adc2eold = adc2e;
  adc3eold = adc3e;

  adc0e = ads.readADC_SingleEnded(0);
  adc1e = ads.readADC_SingleEnded(1);
  adc2e = ads.readADC_SingleEnded(2);
  adc3e = ads.readADC_SingleEnded(3);
  Voltage0e = ((base0e - adc0e) * 0.1875) / 1000;
  Voltage1e = ((base1e - adc1e) * 0.1875) / 1000;
  Voltage2e = ((base2e - adc2e) * 0.1875) / 1000;
  Voltage3e = ((base3e - adc3e) * 0.1875) / 1000;
  
  if (count < 20) {
    base0e = adc0e;
    base1e = adc1e;
    base2e = adc2e;
    base3e = adc3e;
    basediff = diff;
  }

  diff = (abs(adc0a) - abs(adc0aold) +  abs(adc1a) - abs(adc1aold) +  abs(adc2a) - abs(adc2aold) +  abs(adc3a) - abs(adc3aold) +
          abs(adc0b) - abs(adc0bold) +  abs(adc1b) - abs(adc1bold) +  abs(adc2b) - abs(adc2bold) +  abs(adc3b) - abs(adc3bold) +
          abs(adc0c) - abs(adc0cold) +  abs(adc1c) - abs(adc1cold) +  abs(adc2c) - abs(adc2cold) +  abs(adc3c) - abs(adc3cold) +
          abs(adc0d) - abs(adc0dold) +  abs(adc1d) - abs(adc1dold) +  abs(adc2d) - abs(adc2dold) +  abs(adc3d) - abs(adc3dold)) * 0.1875 / 10;

  total = abs(Voltage0a) + abs(Voltage1a) + abs(Voltage2a) + abs(Voltage3a) + abs(Voltage0b) + abs(Voltage1b) + abs(Voltage2b) + abs(Voltage3b)
          + abs(Voltage0c) + abs(Voltage1c) + abs(Voltage2c) + abs(Voltage3c) + abs(Voltage0d) + abs(Voltage1d) + abs(Voltage2d) + abs(Voltage3d);


//  if (abs(diff - basediff) < diffthresh && total < 0.04 && total > 0.005) {
//    base0a = base0a + (adc0a - base0a) / abs(adc0a - base0a);
//    base0b = base0b + (adc0b - base0b) / abs(adc0b - base0b);
//    base0c = base0c + (adc0c - base0c) / abs(adc0c - base0c);
//    base0d = base0d + (adc0d - base0d) / abs(adc0d - base0d);
//    base0e = base0e + (adc0e - base0e) / abs(adc0e - base0e);
//    base1a = base1a + (adc1a - base1a) / abs(adc1a - base1a);
//    base1b = base1b + (adc1b - base1b) / abs(adc1b - base1b);
//    base1c = base1c + (adc1c - base1c) / abs(adc1c - base1c);
//    base1d = base1d + (adc1d - base1d) / abs(adc1d - base1d);
//    base1e = base1e + (adc1e - base1e) / abs(adc1e - base1e);
//    base2a = base2a + (adc2a - base2a) / abs(adc2a - base2a);
//    base2b = base2b + (adc2b - base2b) / abs(adc2b - base2b);
//    base2c = base2c + (adc2c - base2c) / abs(adc2c - base2c);
//    base2d = base2d + (adc2d - base2d) / abs(adc2d - base2d);
//    base2e = base2e + (adc2e - base2e) / abs(adc2e - base2e);
//    base3a = base3a + (adc3a - base3a) / abs(adc3a - base3a);
//    base3b = base3b + (adc3b - base3b) / abs(adc3b - base3b);
//    base3c = base3c + (adc3c - base3c) / abs(adc3c - base3c);
//    base3d = base3d + (adc3d - base3d) / abs(adc3d - base3d);
//    base3e = base3e + (adc3e - base3e) / abs(adc3e - base3e);
//  }


  if (count > 10) {
    Serial.print(Voltage0a * k, 5);
    Serial.print(" ");
    Serial.print(Voltage1a * k, 5);
    Serial.print(" ");
    Serial.print(Voltage2a * k, 5);
    Serial.print(" ");
    Serial.print(Voltage3a * k, 5);
    Serial.print("  ");


    Serial.print(Voltage0b * k, 5);
    Serial.print(" ");
    Serial.print(Voltage1b * k, 5);
    Serial.print(" ");
    Serial.print(Voltage2b * k, 5);
    Serial.print(" ");
    Serial.print(Voltage3b * k, 5);
    Serial.print("  ");

    Serial.print(Voltage0c * k, 5);
    Serial.print(" ");
    Serial.print(Voltage1c * k, 5);
    Serial.print(" ");
    Serial.print(Voltage2c * k, 5);
    Serial.print(" ");
    Serial.print(Voltage3c * k, 5);
    Serial.print("  ");


    Serial.print(Voltage0d * k, 5);
    Serial.print(" ");
    Serial.print(Voltage1d * k, 5);
    Serial.print(" ");
    Serial.print(Voltage2d * k, 5);
    Serial.print(" ");
    Serial.print(Voltage3d * k, 5);


    Serial.print(Voltage0e * k, 5);
    Serial.print(" ");
    Serial.print(Voltage1e * k, 5);
    Serial.print(" ");
    Serial.print(Voltage2e * k, 5);
    Serial.print(" ");
    Serial.println(Voltage3e * k, 5);
  }
  count = count + 1;

}
