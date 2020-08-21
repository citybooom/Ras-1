
#include <SPI.h>

//When Using the SPI library, you only have to worry
//about picking your slave select
//By Default, 11 = MOSI, 12 = MISO, 13 = CLK
int SSpin = 10;   //SPI Slave Select
byte SSadc = 7;

void setup()
{
  
  //Set Pin Direction
  //Again, the other SPI pins are configured automatically
  pinMode(SSpin, OUTPUT);
  pinMode(SSadc, OUTPUT);
  Serial.begin(9600);
  
  //Initialize SPI
  SPI.begin();
  SPI.setClockDivider(2);
  SPI.setDataMode(SPI_MODE1);
  SPI.setBitOrder(MSBFIRST);

  digitalWrite(SSadc, HIGH);
}

//This will set 1 LED to the specififed level
void setLed(int reg, int level)
{
  digitalWrite(SSpin, LOW);
  SPI.transfer(reg);
  SPI.transfer(level);
  digitalWrite(SSpin, HIGH);
}

void loop()
{
  setLed(1,0);

//  for (int j = 50; j<=220; j++)
//  {
//      setLed(0,j);
//      setLed(1,j);
//      setLed(2,j);
//      setLed(4,j);
//      setLed(4,j);
//      delay(10);
//      Serial.println(analogRead(A0));
//  }
//    for (int j = 220; j>=50; j--)
//  {
//            setLed(0,j);
//      setLed(1,j);
//      setLed(2,j);
//      setLed(4,j);
//      setLed(4,j);
//      delay(10);
//      Serial.println(analogRead(A0));
//  }
}
