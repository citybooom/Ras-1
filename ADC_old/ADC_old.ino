#include <Wire.h>
#include <Adafruit_ADS1015.h>
Adafruit_ADS1115 ads(0x48);


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

void setup(void) 
{
  Serial.begin(500000);  
  ads.begin();
  pinMode(2, OUTPUT); 
  pinMode(3, OUTPUT); 
  pinMode(4, OUTPUT); 
  pinMode(5, OUTPUT);

  digitalWrite(2, HIGH);
  delay(1);

  base0a = ads.readADC_SingleEnded(0);
  base1a = ads.readADC_SingleEnded(1);
  base2a = ads.readADC_SingleEnded(2);
  base3a = ads.readADC_SingleEnded(3);

  digitalWrite(2, LOW);
  digitalWrite(3, HIGH);
  delay(1);

  base0b = ads.readADC_SingleEnded(0);
  base1b = ads.readADC_SingleEnded(1);
  base2b = ads.readADC_SingleEnded(2);
  base3b = ads.readADC_SingleEnded(3);
   
  digitalWrite(3, LOW);
  digitalWrite(4, HIGH);
  delay(1);

  base0c = ads.readADC_SingleEnded(0);
  base1c = ads.readADC_SingleEnded(1);
  base2c = ads.readADC_SingleEnded(2);
  base3c = ads.readADC_SingleEnded(3);
  
  digitalWrite(4, LOW);
  digitalWrite(5, HIGH);
  delay(1);

  base0d = ads.readADC_SingleEnded(0);
  base1d = ads.readADC_SingleEnded(1);
  base2d = ads.readADC_SingleEnded(2);
  base3d = ads.readADC_SingleEnded(3);
  Serial.print('a'); 
}

void loop(void) 
{
  digitalWrite(5, LOW);
  digitalWrite(2, HIGH);
  delay(1);
  adc0a = ads.readADC_SingleEnded(0);
  adc1a = ads.readADC_SingleEnded(1);
  adc2a = ads.readADC_SingleEnded(2);
  adc3a = ads.readADC_SingleEnded(3);
  Voltage0a = ((base0a-adc0a) * 0.1875)/1000;
  Voltage1a = ((base1a-adc1a) * 0.1875)/1000;
  Voltage2a = ((base2a-adc2a) * 0.1875)/1000;
  Voltage3a = ((base3a-adc3a) * 0.1875)/1000;
  
  digitalWrite(2, LOW);
  digitalWrite(3, HIGH);
  delay(1);
  adc0b = ads.readADC_SingleEnded(0);
  adc1b = ads.readADC_SingleEnded(1);
  adc2b = ads.readADC_SingleEnded(2);
  adc3b = ads.readADC_SingleEnded(3);
  Voltage0b = ((base0b-adc0b) * 0.1875)/1000;
  Voltage1b = ((base1b-adc1b) * 0.1875)/1000;
  Voltage2b = ((base2b-adc2b) * 0.1875)/1000;
  Voltage3b = ((base3b-adc3b) * 0.1875)/1000;

  digitalWrite(3, LOW);
  digitalWrite(4, HIGH);
  delay(1);
  adc0c = ads.readADC_SingleEnded(0);
  adc1c = ads.readADC_SingleEnded(1);
  adc2c = ads.readADC_SingleEnded(2);
  adc3c = ads.readADC_SingleEnded(3);
  Voltage0c = ((base0c-adc0c) * 0.1875)/1000;
  Voltage1c = ((base1c-adc1c) * 0.1875)/1000;
  Voltage2c = ((base2c-adc2c) * 0.1875)/1000;
  Voltage3c = ((base3c-adc3c) * 0.1875)/1000;

  digitalWrite(4, LOW);
  digitalWrite(5, HIGH);
  delay(1);
  adc0d = ads.readADC_SingleEnded(0);
  adc1d = ads.readADC_SingleEnded(1);
  adc2d = ads.readADC_SingleEnded(2);
  adc3d = ads.readADC_SingleEnded(3);
  Voltage0d = ((base0d-adc0d) * 0.1875)/1000;
  Voltage1d = ((base1d-adc1d) * 0.1875)/1000;
  Voltage2d = ((base2d-adc2d) * 0.1875)/1000;
  Voltage3d = ((base3d-adc3d) * 0.1875)/1000;

  
  Serial.print(Voltage0a*100, 5); 
  Serial.print(" ");
  Serial.print(Voltage1a*100, 5);
  Serial.print(" ");
  Serial.print(Voltage2a*100, 5);
  Serial.print(" ");
  Serial.print(Voltage3a*100, 5);
  Serial.print("  ");  
     
  Serial.print(Voltage0b*100, 5); 
  Serial.print(" ");
  Serial.print(Voltage1b*100, 5);
  Serial.print(" ");
  Serial.print(Voltage2b*100, 5);
  Serial.print(" ");
  Serial.print(Voltage3b*100, 5);
  Serial.print("  ");  
       
  Serial.print(Voltage0c*100, 5); 
  Serial.print(" ");
  Serial.print(Voltage1c*100, 5);
  Serial.print(" ");
  Serial.print(Voltage2c*100, 5);
  Serial.print(" ");
  Serial.print(Voltage3c*100, 5);
  Serial.print("  "); 

       
  Serial.print(Voltage0d*100, 5); 
  Serial.print(" ");
  Serial.print(Voltage1d*100, 5);
  Serial.print(" ");
  Serial.print(Voltage2d*100, 5);
  Serial.print(" ");
  Serial.print(Voltage3d*100, 5);
  Serial.println(" "); 

}
