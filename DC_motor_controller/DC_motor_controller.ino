void setup() {
  // put your setup code here, to run once:
  pinMode(8,OUTPUT);
  pinMode(9,OUTPUT);
  pinMode(10,OUTPUT);

  digitalWrite(8,HIGH);
  digitalWrite(10,LOW);

  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  analogWrite(9,analogRead(A0)/4);
  
}
