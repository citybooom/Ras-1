// Update: Oct26
// Added the second linear stage

// Update: Oct29
// Added the DC motor control
// Switched to Arduino Due

// Include the AccelStepper library:
#include <AccelStepper.h>
#include <VNH3SP30.h>
#include <LiquidCrystal.h>
LiquidCrystal lcd(12, 11, A0, A1, A2, A3);


int StepperWaitCycles = 1;
int StepperMoveSteps_Y = 32;
int StepperMoveSteps_X = 12;
int StepperPos_Y;
int StepperPos_X;
int StepTime = 1000;


// Define stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver:
#define Low_dirPin 9
#define Low_stepPin 10
#define motorInterfaceType 1

#define High_dirPin 6
#define High_stepPin 7

#define switchPin 8

#define IRPin 13

#define DC_Motor_Pot A5

VNH3SP30 Motor1;    // define control object for 1 motor

// motor pins
#define M1_PWM 3    // pwm pin motor (digital output)
#define M1_INA 2    // control pin INA (digital output)
#define M1_INB 4    // control pin INB (digital output)

// Create a new instance of the AccelStepper class:
AccelStepper Low_stepper = AccelStepper(motorInterfaceType, Low_stepPin, Low_dirPin);
AccelStepper High_stepper = AccelStepper(motorInterfaceType, High_stepPin, High_dirPin);

void setup() {
  Serial.begin(115200);
  // Set the maximum speed and acceleration:
  Low_stepper.setMaxSpeed(1500);
  Low_stepper.setAcceleration(4000);
  High_stepper.setMaxSpeed(1500);
  High_stepper.setAcceleration(4000);
  pinMode(13, INPUT);
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("X       Y");
  pinMode(switchPin, INPUT);
  pinMode(DC_Motor_Pot, INPUT);

  Motor1.begin(M1_PWM, M1_INA, M1_INB);
  
}

void loop(){
  while(digitalRead(switchPin) == 0){}


  lcd.clear();
  lcd.print("X       Y");  
  
  for(StepperPos_Y = 1; StepperPos_Y<=StepperMoveSteps_Y; StepperPos_Y++){
    
    if (StepperPos_Y%2 == 1){
      for(StepperPos_X = 1; StepperPos_X<=StepperMoveSteps_X; StepperPos_X++){
        High_stepper.moveTo(400*StepperPos_X);
        High_stepper.runToPosition();
        Serial.print(':');
        Serial.print(StepperPos_X);
        Serial.print('_');
        Serial.print(StepperPos_Y);
        if(StepperPos_X < 10){
          Serial.print('_');
          }
        if(StepperPos_Y < 10){
          Serial.print('_');
          }
        Serial.println("");
        LCD_print(StepperPos_X, StepperPos_Y);
        DCMotorMove();        
        delay(StepTime);
      }
    }

    if (StepperPos_Y%2 == 0){
      for(StepperPos_X = StepperMoveSteps_X; StepperPos_X>=1; StepperPos_X--){
        High_stepper.moveTo(400*StepperPos_X);
        High_stepper.runToPosition();
        Serial.print(':');
        Serial.print(StepperPos_X);
        Serial.print('_');
        Serial.print(StepperPos_Y);
        if(StepperPos_X < 10){
          Serial.print('_');
        }
        if(StepperPos_Y < 10){
          Serial.print('_');
        }
        Serial.println("");
        LCD_print(StepperPos_X, StepperPos_Y);
        DCMotorMove();
        delay(StepTime);
      }
    }
    Low_stepper.moveTo(320*StepperPos_Y);
    Low_stepper.runToPosition();
  }
  
  High_stepper.moveTo(0);
  High_stepper.runToPosition();
  Low_stepper.moveTo(0);
  Low_stepper.runToPosition();
}

void LCD_print(int x, int y){
        lcd.clear();
        lcd.print("X       Y");
        lcd.setCursor(0, 1);
        lcd.print(x);
        lcd.setCursor(8, 1);
        lcd.print(y);
}

void DCMotorMove(){
  int pastState = LOW;
  int counter = 0;
  int MotorSpeed;
  MotorSpeed = analogRead(DC_Motor_Pot)/3;
  while(counter < 6){
    int currentState = digitalRead(IRPin);
    if (currentState == HIGH && pastState == LOW){      
      Motor1.setSpeed(MotorSpeed);
      counter++;
    }
    pastState = currentState;
    delay(10);
  }
  delay(400-MotorSpeed);
  Motor1.setSpeed(0);
  
}
