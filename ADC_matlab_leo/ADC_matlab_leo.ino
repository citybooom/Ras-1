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
float k = 100;

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

int count = 0;
int diff = 0;
int basediff = 0;

void setup(void) 
{
  Serial.begin(9600);  
  ads.begin();
  pinMode(1, OUTPUT); 
  pinMode(9, OUTPUT); 
  pinMode(10, OUTPUT); 
  pinMode(11, OUTPUT);

  digitalWrite(11, LOW);
  digitalWrite(1, HIGH);
  delay(1);
  
  base0a = ads.readADC_SingleEnded(0);
  base1a = ads.readADC_SingleEnded(1);
  base2a = ads.readADC_SingleEnded(2);
  base3a = ads.readADC_SingleEnded(3);
    

  digitalWrite(1, LOW);
  digitalWrite(9, HIGH);
  delay(1);

  
  base0b = ads.readADC_SingleEnded(0);
  base1b = ads.readADC_SingleEnded(1);
  base2b = ads.readADC_SingleEnded(2);
  base3b = ads.readADC_SingleEnded(3);
  
   
  digitalWrite(9, LOW);
  digitalWrite(10, HIGH);
  delay(1);

  
  base0c = ads.readADC_SingleEnded(0);
  base1c = ads.readADC_SingleEnded(1);
  base2c = ads.readADC_SingleEnded(2);
  base3c = ads.readADC_SingleEnded(3);
  
  
  digitalWrite(10, LOW);
  digitalWrite(11, HIGH);
  delay(1);


  base0d = ads.readADC_SingleEnded(0);
  base1d = ads.readADC_SingleEnded(1);
  base2d = ads.readADC_SingleEnded(2);
  base3d = ads.readADC_SingleEnded(3);
  
  
}

void loop(void) 
{
  digitalWrite(11, LOW);
  digitalWrite(1, HIGH);
  delay(1);

  adc0aold = adc0a;
  adc1aold = adc1a;
  adc2aold = adc2a;
  adc3aold = adc3a;
  
  adc0a = ads.readADC_SingleEnded(0);
  adc1a = ads.readADC_SingleEnded(1);
  adc2a = ads.readADC_SingleEnded(2);
  adc3a = ads.readADC_SingleEnded(3);
  Voltage0a = ((base0a-adc0a) * 0.1875)/1000;
  Voltage1a = ((base1a-adc1a) * 0.1875)/1000;
  Voltage2a = ((base2a-adc2a) * 0.1875)/1000;
  Voltage3a = ((base3a-adc3a) * 0.1875)/1000;
  if (count < 20) {
    base0a = adc0a;
    base1a = adc1a;
    base2a = adc2a;
    base3a = adc3a;
  }
  
  digitalWrite(1, LOW);
  digitalWrite(9, HIGH);
  delay(1);

  adc0bold = adc0b;
  adc1bold = adc1b;
  adc2bold = adc2b;
  adc3bold = adc3b;
  
  adc0b = ads.readADC_SingleEnded(0);
  adc1b = ads.readADC_SingleEnded(1);
  adc2b = ads.readADC_SingleEnded(2);
  adc3b = ads.readADC_SingleEnded(3);
  Voltage0b = ((base0b-adc0b) * 0.1875)/1000;
  Voltage1b = ((base1b-adc1b) * 0.1875)/1000;
  Voltage2b = ((base2b-adc2b) * 0.1875)/1000;
  Voltage3b = ((base3b-adc3b) * 0.1875)/1000;
  if (count < 20) {
    base0b = adc0b;
    base1b = adc1b;
    base2b = adc2b;
    base3b = adc3b;
  }

  digitalWrite(9, LOW);
  digitalWrite(10, HIGH);
  delay(1);

  adc0cold = adc0c;
  adc1cold = adc1c;
  adc2cold = adc2c;
  adc3cold = adc3c;
  
  
  adc0c = ads.readADC_SingleEnded(0);
  adc1c = ads.readADC_SingleEnded(1);
  adc2c = ads.readADC_SingleEnded(2);
  adc3c = ads.readADC_SingleEnded(3);
  Voltage0c = ((base0c-adc0c) * 0.1875)/1000;
  Voltage1c = ((base1c-adc1c) * 0.1875)/1000;
  Voltage2c = ((base2c-adc2c) * 0.1875)/1000;
  Voltage3c = ((base3c-adc3c) * 0.1875)/1000;
  if (count < 20) {
    base0c = adc0c;
    base1c = adc1c;
    base2c = adc2c;
    base3c = adc3c;
  }


  digitalWrite(10, LOW);
  digitalWrite(11, HIGH);
  delay(1);

  adc0dold = adc0d;
  adc1dold = adc1d;
  adc2dold = adc2d;
  adc3dold = adc3d;
  
  adc0d = ads.readADC_SingleEnded(0);
  adc1d = ads.readADC_SingleEnded(1);
  adc2d = ads.readADC_SingleEnded(2);
  adc3d = ads.readADC_SingleEnded(3);
  Voltage0d = ((base0d-adc0d) * 0.1875)/1000;
  Voltage1d = ((base1d-adc1d) * 0.1875)/1000;
  Voltage2d = ((base2d-adc2d) * 0.1875)/1000;
  Voltage3d = ((base3d-adc3d) * 0.1875)/1000;

  diff = abs(adc0a - adc0aold) +  abs(adc1a - adc1aold) +  abs(adc2a - adc2aold) +  abs(adc3a - adc3aold) +
         abs(adc0b - adc0bold) +  abs(adc1b - adc1bold) +  abs(adc2b - adc2bold) +  abs(adc3b - adc3bold) + 
         abs(adc0c - adc0dold) +  abs(adc1c - adc1cold) +  abs(adc2c - adc2cold) +  abs(adc3c - adc3cold) +
         abs(adc0d - adc0dold) +  abs(adc1d - adc1dold) +  abs(adc2d - adc3dold) +  abs(adc3d - adc3dold);
  
  if (count < 20) {
    base0d = adc0d;
    base1d = adc1d;
    base2d = adc2d;
    base3d = adc3d;
    basediff = diff;
  }


  Serial.print(Voltage0a*k, 5); 
  Serial.print(" ");
  Serial.print(Voltage1a*k, 5);
  Serial.print(" ");
  Serial.print(Voltage2a*k, 5);
  Serial.print(" ");
  Serial.print(Voltage3a*k, 5);
  Serial.print("  ");
        
     
  Serial.print(Voltage0b*k, 5); 
  Serial.print(" ");
  Serial.print(Voltage1b*k, 5);
  Serial.print(" ");
  Serial.print(Voltage2b*k, 5);
  Serial.print(" ");
  Serial.print(Voltage3b*k, 5);
  Serial.print("  ");  
  
  Serial.print(Voltage0c*k, 5); 
  Serial.print(" ");
  Serial.print(Voltage1c*k, 5);
  Serial.print(" ");
  Serial.print(Voltage2c*k, 5);
  Serial.print(" ");
  Serial.print(Voltage3c*k, 5);
  Serial.print("  ");  
 
       
  Serial.print(Voltage0d*k, 5); 
  Serial.print(" ");
  Serial.print(Voltage1d*k, 5);
  Serial.print(" ");
  Serial.print(Voltage2d*k, 5);
  Serial.print(" ");
  Serial.println(Voltage3d*k, 5);

  count = count + 1;  

}
