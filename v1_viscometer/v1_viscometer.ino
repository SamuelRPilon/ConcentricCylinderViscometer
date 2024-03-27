int out1 = 10; // PWM pin for motor speed control
int ena = 10; // PWM pin for motor speed control (same as out1)
int in1 = 9; // Motor control pin 1
int in2 = 8; // Motor control pin 2

int desiredSpeed = 0; // Initialize desired speed

void setup() {
  Serial.begin(9600);
  
  pinMode(out1, OUTPUT); // Motor speed control pin
  pinMode(ena, OUTPUT); // PWM pin for motor speed control
  pinMode(in1, OUTPUT); // Motor control pin 1
  pinMode(in2, OUTPUT); // Motor control pin 2

  analogWrite(out1, 0); // Initially set speed to 0
}

void loop() {
  if (Serial.available()) {
    char val = Serial.read();
    
    switch (val) {
      case '0':
        desiredSpeed = 0;
        Serial.println("Speed is set to 0");
        break;
      case '1':
        desiredSpeed = 75;
        Serial.println("Speed is set to 1");
        break;
      case '2':
        desiredSpeed = 100;
        Serial.println("Speed is set to 2");
        break;
      case '3':
        desiredSpeed = 125;
        Serial.println("Speed is set to 3");
        break;
      case '4':
        desiredSpeed = 150;
        Serial.println("Speed is set to 4");
        break;
      case '5':
        desiredSpeed = 175;
        Serial.println("Speed is set to 5");
        break;
      case '6':
        desiredSpeed = 200;
        Serial.println("Speed is set to 6");
        break;
      case '7':
        desiredSpeed = 225;
        Serial.println("Speed is set to 7");
        break;
      case '8':
        desiredSpeed = 235;
        Serial.println("Speed is set to 8");
        break;
      case '9':
        desiredSpeed = 255;
        Serial.println("Speed is set to 9");
        Serial.println("Approximate speed is 15500 RPM");
        break;
    }
  }
  
  // Set the motor speed to the desired speed
  analogWrite(ena, desiredSpeed);

  // Set motor direction (example: forward)
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
}
