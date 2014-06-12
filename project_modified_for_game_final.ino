#include <Servo.h>

Servo myservo;
//int loadSensorValue = 0;
int loadSensorValue1 = 0;
int loadSensorValue2 = 0;
int newServoPosition = 1450;
int servoPosition = 1450; //platform is flat

const int ledPinUp = 8;
const int ledPinStop = 9;
const int ledPinDown = 7;

void setup() {
  Serial.begin(115200);
  myservo.attach(10);
  pinMode(ledPinUp, OUTPUT);
  pinMode(ledPinStop, OUTPUT);
  pinMode(ledPinDown, OUTPUT);
  moveArm();
}

void loop(){
  readLoadSensors();
  if(Serial.available() == 4){
    recieveSerialInput();
  }
  else {
    sendSerialOutput();
  }
  //delay(100);
}

void readLoadSensors(){
  //int tempSensVal1 = analogRead(A0);
  //delay(100);
  int tempSensVal2 = analogRead(A2);
  delay(10);
  //loadSensorValue1 = (tempSensVal1 + tempSensVal2)/2;
  //loadSensorValue1 = tempSensVal1;
  loadSensorValue2 = tempSensVal2;
}

void recieveSerialInput(){
  unsigned long serialValue = readLongFromBytes();
  if(serialValue <= 2150 & serialValue >= 950) { //max and min, reject all outside values to prevent damage
    newServoPosition = (int)serialValue;
    moveArm();
  }
  //Serial.print(serialValue, DEC); //for testing
  //Serial.print('\n');
}

void sendSerialOutput(){
  //Serial.print(loadSensorValue1, DEC);
  //Serial.print(' ');
  Serial.print(loadSensorValue2, DEC);
  Serial.print(' ');
  Serial.print(servoPosition, DEC);
  Serial.print('\n'); //NEEDED FOR READLINE TO WORK IN PYTHON, WILL HANG OTHERWISE
}

unsigned long readLongFromBytes() {
  union u_tag {
    byte b[4];
    unsigned long lval;
  } u;
  Serial.flush();
  u.b[0] = Serial.read();
  u.b[1] = Serial.read();
  u.b[2] = Serial.read();
  u.b[3] = Serial.read();
  return u.lval;
}

void moveArm() {
  int servoDelay = 1; //approximately how long it will take to finish the movement
  //.00135 seconds/microsecond input, use 1.5 just to be sure it finishes motion and to convert to ms
  if(newServoPosition > servoPosition) {
    servoDelay = (newServoPosition - servoPosition) * 1.5;
    digitalWrite(ledPinUp, HIGH);
    digitalWrite(ledPinStop, LOW);
  }
  else if(newServoPosition < servoPosition) {
    servoDelay = (servoPosition - newServoPosition) * 1.5;
    digitalWrite(ledPinDown, HIGH);
    digitalWrite(ledPinStop, LOW);
  }
  servoPosition = newServoPosition;
  myservo.writeMicroseconds(servoPosition);
  delay(servoDelay);
  //delay(1);
  digitalWrite(ledPinUp, LOW);
  digitalWrite(ledPinStop, HIGH);
  digitalWrite(ledPinDown, LOW);
}
