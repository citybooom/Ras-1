
#include <SPI.h>
#include <math.h>


//When Using the SPI library, you only have to worry
//about picking your slave select
//By Default, 11 = MOSI, 12 = MISO, 13 = CLK
byte SSpot = 10;   //Pot Slave Select
byte SSadc = 7;   //ADC Slave Select
byte RESET = 5;
byte DATA_READY = 8;
byte out[400];
byte data[400];
int dataindex = 1;
int counter = 0;
int bytecount = 0;
byte transmission1;
long tempdata;
byte transmission2;
byte data1;
byte data2;
byte expectedResp;
long firstreadings[8];
long readings[8];
long dataout[8];
long dataprefilt[8];
long datafilt[8];
long dataave = 0;
long reading = 0;
long tempdata1 = 0;
long tempdata2 = 0;
long tempdata3 = 0;
double j;
unsigned long timer = 0;
int buffercounter = 0;
long chargingtimer = 0;


byte res = 0;
int first = 1;
double EMA_a = 0.00005;    //initialization of EMA alpha
long EMA_S = 0;        //initialization of EMA S
long highpass = 0;

void setup()
{
  // set up Timer 1
  pinMode (9, OUTPUT);
  pinMode (19, OUTPUT);
  pinMode (6, OUTPUT);
  digitalWrite(19, HIGH);
  digitalWrite(6, HIGH);
  TCCR1A = bit (COM1A0);  // toggle OC1A on Compare Match
  TCCR1B = bit (WGM12) | bit (CS10);   // CTC, no prescaling
  OCR1A =  0;       // output every cycle


  delay(10);
  pinMode(SSpot, OUTPUT);
  pinMode(RESET, OUTPUT);
  pinMode(SSadc, OUTPUT);

  pinMode(DATA_READY, INPUT);
  digitalWrite(RESET, HIGH);
  digitalWrite(SSpot, HIGH);
  Serial.begin(9600);


  //Initialize SPI
  SPI.begin();
  SPI.setDataMode(SPI_MODE1);
  SPI.setBitOrder(MSBFIRST);
  SPI.setClockDivider(SPI_CLOCK_DIV2);
  digitalWrite(SSadc, HIGH);
  digitalWrite(RESET, LOW);
  delay(10);
  digitalWrite(RESET, HIGH);

  // while(digitalRead(DATA_READY) == LOW){}

  // Reset
  digitalWrite(SSadc, LOW);

  SPI.transfer(0b00000000);
  SPI.transfer(0b00010001);
  SPI.transfer(0b00000000);

  byte packet = 0;

  if (SPI.transfer(0) == 0b00101000) {
    Serial.print("Reset successful in ");
    Serial.print(bytecount, BIN);
    Serial.println(" cycles");
  }
  else {
  }
  digitalWrite(SSadc, HIGH);

  delay(10);

  digitalWrite(SSadc, LOW);
  writeDummyWord(10);
  digitalWrite(SSadc, HIGH);

  digitalWrite(SSadc, LOW);
  writeDummyWord(10);
  digitalWrite(SSadc, HIGH);
  timer = micros();
}

void loop()
{
  digitalWrite(SSadc, HIGH);

  if(first) {
    digitalWrite(SSadc, LOW);
    writeDummyWord(10);
    digitalWrite(SSadc, HIGH);
  
    digitalWrite(SSadc, LOW);
    writeDummyWord(10);
    digitalWrite(SSadc, HIGH);
  }
  
  gatherData();
  
  if (chargingtimer > 0) {
    for (int i = 0; i < 8; i++) {
      firstreadings[i] = readings[i];
    }
    chargingtimer = chargingtimer - 1;
  }

  first = 0;
 
  for (int i = 0; i < 8; i++) {
    dataprefilt[i] = readings[i] - firstreadings[i];
    datafilt[i] =  dataprefilt[i];
    if(buffercounter == 0) {
      dataout[i] = datafilt[i];
    }
    else{
      dataout[i] = dataout[i] + datafilt[i];
    }
  }
  buffercounter = buffercounter + 1;

  
//  while(millis() > 30000){} 
  if(micros() - 500 > timer){
    timer = micros();
    

    for (int i = 0; i < 8; i++){
      dataout[i] = readings[i];
      //dataout[i] = readings[i];
    }
//    delay(1000);
//    Serial.print(millis()/1000.0);
//    Serial.print("  ");
    Serial.print(": ");
    for (int i = 0; i < 8; i++) {
      if(i!= 9){
        tempdata = dataout[i];
        if (tempdata > 0) {
          Serial.print(" ");
        }
        j = log10(abs(tempdata));
        if (tempdata == 0)
          j = 1;
        while (j < 8) {
          Serial.print(" ");
          j = j + 1;
        }
        if(1){
          Serial.print(tempdata);
        }
      }
    }
    Serial.println("  ");
    buffercounter = 0;
  }
  dataindex = 0;
}


void writeDummyWord(int numBytes) {
  for (int i = 0; i < numBytes; i++) {
    transferSPI(0b0000000);
    transferSPI(0b0000000);
    transferSPI(0b0000000);
  }
}

void gatherData() {

  digitalWrite(SSadc, LOW);

  transferSPI(0b0000000);
  transferSPI(0b0000000);
  transferSPI(0b0000000);

  for (int i = 0; i < 8; i++) {

    unsigned long tempdata1 = transferSPI(0b0000000);
    unsigned long tempdata2 = transferSPI(0b0000000);
    unsigned long tempdata3 = transferSPI(0b0000000);
    reading = (tempdata1 << 16) | (tempdata2 << 8) | tempdata3;
    if (first) {
      readings[i] = reading;
    }
    else {
      readings[i] = reading;
      //readings[i] = readings[i]*0.95 + reading*0.05;
    }
  }

  transferSPI(0b0000000);
  transferSPI(0b0000000);
  transferSPI(0b0000000);
  digitalWrite(SSadc, HIGH);

}


int transferSPI(byte datain) {
  out[dataindex] = datain;
  data[dataindex] = SPI.transfer(datain);
  byte result =  data[dataindex];
  dataindex = dataindex + 1;
  if (dataindex >= 400) {
    Serial.println("Fail");
  }
  return result;

}
