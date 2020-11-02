long count = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print(":3_");
  count = count + 1;
  Serial.println(count);
}
