
#include <SPI.h>

//When Using the SPI library, you only have to worry
//about picking your slave select
//By Default, 11 = MOSI, 12 = MISO, 13 = CLK
byte SSpot = 10;   //Pot Slave Select
byte SSadc = 7;   //ADC Slave Select
byte RESET = 5;
byte DATA_READY = 2;
byte DATA_READY2 = 3;
byte response18 = 0;
byte out[800];
byte data[800];
int dataindex = 0;
int counter = 0;
int bytecount = 0;
byte dataReady = 0;

void setup()
{
  
  //Set Pin Direction
  //Again, the other SPI pins are configured automatically
  delay(1000);
  pinMode(SSpot, OUTPUT);
  pinMode(RESET, OUTPUT);
  pinMode(SSadc, OUTPUT);
  //pinMode(DATA_READY, INPUT);
  pinMode(DATA_READY, INPUT_PULLUP);
  pinMode(DATA_READY2, INPUT_PULLUP);
  
  attachInterrupt(digitalPinToInterrupt(DATA_READY), DataNotReady, RISING);
  attachInterrupt(digitalPinToInterrupt(DATA_READY2), DataReady, FALLING);
  Serial.begin(250000);
  digitalWrite(RESET, HIGH);
  
  //Initialize SPI
  SPI.begin();
  SPI.setDataMode(SPI_MODE1);
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
}

void loop()
{
  //Serial.println("Frame Start");
  digitalWrite(SSadc, LOW);
  writeDummyWord(10);
  digitalWrite(SSadc, HIGH);
  delay(1);
  digitalWrite(SSadc, LOW);
  writeDummyWord(10);
  digitalWrite(SSadc, HIGH);
  delay(1);
  
  digitalWrite(SSadc, LOW);
  // Write to Register CH7_CFG Register (Address = 2Ch): 3 Registers
  transferSPI(0b01110110);
  transferSPI(0b00000010);
  transferSPI(0b00000000);

  transferSPI(0b10111101);
  transferSPI(0b01000010);
  transferSPI(0b00000000);

  transferSPI(0b10101101);
  transferSPI(0b01000011);
  transferSPI(0b00000000);

  transferSPI(0b10111001);
  transferSPI(0b01000110);
  transferSPI(0b00000000);

  writeDummyWord(6);
  
  while(dataReady == 1){transferSPI(0b00000000);} 
 
    // //digitalWrite(SSadc, HIGH);digitalWrite(SSadc, LOW);
    
  // Read Command

  transferSPI(0b10110110); 
  transferSPI(0b00000010);
  transferSPI(0b00000000);


  writeDummyWord(9);
 
  while(dataReady == 1){transferSPI(0b00000000);} 
  //digitalWrite(SSadc, HIGH);

  digitalWrite(SSadc, LOW);
  writeDummyWord(10);
  digitalWrite(SSadc, HIGH);
  counter = 0;
  Serial.println(dataindex);
  while(counter < dataindex){
    Serial.print(out[counter],BIN);
    Serial.print("    "); 
    Serial.println(data[counter],BIN);
    counter = counter + 1;
  }
  dataindex = 0;
  
}
void writeRegister(byte thisRegister, byte thisValue) {

  uint16_t transmission = 0b011 << 13; // Write command in first 3 bit
  transmission = transmission | thisRegister << 7 | thisValue;
  
  digitalWrite(SSadc, LOW);
  SPI.transfer(transmission); //Send register location
  digitalWrite(SSadc, HIGH);
  Serial.print("transmitted: ");
  Serial.println(transmission);
}


void writeDummyWord(int numBytes){
  for(int i = 0; i < numBytes; i++){
    transferSPI(0b0000000);
    transferSPI(0b0000000);
    transferSPI(0b0000000);
  }
}

void transferSPI(byte datain){
    out[dataindex]= datain;
    data[dataindex] = SPI.transfer(datain);
    dataindex = dataindex + 1;
    if(dataindex >= 800){
      Serial.println("Fail");
    }
}


int readRegister(byte thisRegister, byte thisLen) {

  byte bytesToRead = thisLen;
  uint16_t transmission = 0b101 << 13; // Write command in first 3 bit
  transmission = transmission | thisRegister << 7 | thisLen;
  
  digitalWrite(SSadc, LOW);
  SPI.transfer(transmission); //Send register location
  
  byte result = SPI.transfer(0);

  digitalWrite(SSadc, HIGH);
  Serial.print("Read Register: ");
  Serial.print(result);
  

}

void DataNotReady() {
  dataReady = 0;
  data[dataindex] = 0xFF;
  out[dataindex] = 0xFF;
  dataindex = dataindex + 1;
  //Serial.println("bar");
}

void DataReady() {
  dataReady = 1;
  data[dataindex] = 0xCC;
  out[dataindex] = 0xCC;
  dataindex = dataindex + 1;
  //Serial.println("foo");
}
