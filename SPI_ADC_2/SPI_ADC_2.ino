
#include <SPI.h>

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
byte transmission2;
byte data1;
byte data2;
byte expectedResp;
double readings[8];
unsigned long reading = 0;
unsigned long tempdata1 = 0;
unsigned long tempdata2 = 0;
unsigned long tempdata3 = 0;
byte res = 0;

void setup()
{
  
  //Set Pin Direction
  //Again, the other SPI pins are configured automatically
  delay(1000);
  pinMode(SSpot, OUTPUT);
  pinMode(RESET, OUTPUT);
  pinMode(SSadc, OUTPUT);
  
  pinMode(DATA_READY, INPUT);
  digitalWrite(RESET, HIGH);
  digitalWrite(SSpot, HIGH);
  Serial.begin(2000000);

  
  //Initialize SPI
  SPI.begin();
  //SPI.setDataMode(SPI_MODE1);
  SPI.setBitOrder(MSBFIRST);
  SPI.setClockDivider(2);
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
  
  //Serial.println("Begin Reset Attempt");
  byte packet = 0;
  while(packet != 0b11111111){
    bytecount = bytecount + 1;
    packet = SPI.transfer(0);
    }
  if (SPI.transfer(0) == 0b00101000) {
    Serial.print("Reset successful in ");
    Serial.print(bytecount);
    Serial.println(" cycles");
  }
  else{
    Serial.println("Reset Failed");    
  }
  digitalWrite(SSadc, HIGH);
  //writeRegister(0x2C, 0b1111111100000010);



  delay(10);
  setPot(1,0);

  digitalWrite(SSadc, LOW);
  writeDummyWord(10);
  digitalWrite(SSadc, HIGH);

  digitalWrite(SSadc, LOW);
  writeDummyWord(10);
  digitalWrite(SSadc, HIGH);
}

void loop()
{
  digitalWrite(SSadc, HIGH);
//  setPot(1,res);
//  if(readings[0] < 150000){
//    if(res < 255)
//    res = res + 1;
//  }
//  else if(readings[0] > 220000)
//    if(res > 0)
//    res = res - 1;
//    
  digitalWrite(SSadc, LOW);
  writeDummyWord(10);
  digitalWrite(SSadc, HIGH);

  digitalWrite(SSadc, LOW);
  writeDummyWord(10);
  digitalWrite(SSadc, HIGH);

 
  gatherData();
  Serial.println(readings[0]);
  //Serial.println(res);
  

//  counter = 0;
//  Serial.println(dataindex);
//  while(counter < dataindex){
//    Serial.print(out[counter],BIN);
//    Serial.print("  "); 
//    Serial.println(data[counter],BIN);
//    counter = counter + 1;
//  }
  dataindex = 0;
  
}



void writeDummyWord(int numBytes){
  for(int i = 0; i < numBytes; i++){
    transferSPI(0b0000000);
    transferSPI(0b0000000);
    transferSPI(0b0000000);
  }
}

void gatherData(){

    digitalWrite(SSadc, LOW);
    
    transferSPI(0b0000000);
    transferSPI(0b0000000);
    transferSPI(0b0000000);
   
  for(int i = 0; i < 8; i++){
    
    unsigned long tempdata1 = transferSPI(0b0000000);
    unsigned long tempdata2 = transferSPI(0b0000000);
    unsigned long tempdata3 = transferSPI(0b0000000);
    reading = (tempdata1 << 16) | (tempdata2 << 8) | tempdata3;
    readings[i] = readings[i]*0.99 + reading*(0.01);
  }
   
    transferSPI(0b0000000);
    transferSPI(0b0000000);
    transferSPI(0b0000000);

    digitalWrite(SSadc, HIGH);
}

    
int transferSPI(byte datain){
    out[dataindex]= datain;
    data[dataindex] = SPI.transfer(datain);
    byte result =  data[dataindex];
    dataindex = dataindex + 1;
    if(dataindex >= 400){
      Serial.println("Fail");
    }
    return result;
    
}

void writeRegister(byte thisRegister, int thisValue) {

  transmission1 = 0b011 << 5 | (thisRegister >> 1); // Write command in first 3 bit
  transmission2 = (thisRegister | 0b1) << 7;

  data1 = thisValue & 0b0000000011111111;
  data2 = (thisValue & 0b1111111100000000) >> 8;
  
  digitalWrite(SSadc, LOW);
  transferSPI(transmission1); //Send register location
  transferSPI(transmission2); //Send register location
  transferSPI(0);

  transferSPI(data2); //Send register location
  transferSPI(data1); //Send register location
  transferSPI(0);

  expectedResp =  0b010 << 5 | (thisRegister >> 1);
  
  while(data[dataindex-1] != expectedResp) {
    transferSPI(0b00000000);
  } 
  digitalWrite(SSadc, HIGH);
  unsigned int result  = readRegister(thisRegister,0);
  Serial.println(result,BIN);
 
}

unsigned int readRegister(byte thisRegister, byte thisLen) {

  transmission1 = 0b101 << 5 | (thisRegister >> 1); // Write command in first 3 bit
  transmission2 = (thisRegister | 0b1) << 7;
 
  digitalWrite(SSadc, LOW);
  transferSPI(transmission1); //Send register location
  transferSPI(transmission2); //Send register location
  transferSPI(0);
  writeDummyWord(9);
  digitalWrite(SSadc, HIGH);
  while(digitalRead(DATA_READY) == 0);
  digitalWrite(SSadc, LOW);
  unsigned int firstbit = transferSPI(0b00000000);
  int secondbit = transferSPI(0b00000000);
  digitalWrite(SSadc, HIGH);
  
  unsigned int result = ((firstbit *256) | secondbit);
  return result;

  

}

void setPot(int reg, int level)
{
  digitalWrite(SSpot, LOW);
  SPI.transfer(reg);
  SPI.transfer(level);
  digitalWrite(SSpot, HIGH);
}
