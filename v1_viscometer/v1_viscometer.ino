// Define the pins
const int irPin = 2; // IR sensor pin
const int ledPin = 13; // On-board LED pin
const int out1 = 10; // PWM pin for motor speed control
const int ena = 10; // PWM pin for motor speed control (same as out1)
const int in1 = 9; // Motor control pin 1
const int in2 = 8; // Motor control pin 2

volatile unsigned long lastTime;
volatile unsigned long interruptCount; // Count of interrupts within one second
volatile boolean flag;

int desiredSpeed = 0; // Initialize desired speed
int currentSpeed = 0; // Current motor speed
int rampSpeedIncrement = 5; // Increment for ramping speed change
unsigned long rampInterval = 100; // Interval between ramp steps in milliseconds
unsigned long previousMillis = 0; // Variable to store the previous time

void setup() {
  Serial.begin(9600); // Start serial communication
  pinMode(irPin, INPUT); // Initialize IR sensor pin as input
  pinMode(ledPin, OUTPUT); // Initialize LED pin as output
  pinMode(out1, OUTPUT); // Motor speed control pin
  pinMode(ena, OUTPUT); // PWM pin for motor speed control
  pinMode(in1, OUTPUT); // Motor control pin 1
  pinMode(in2, OUTPUT); // Motor control pin 2

  attachInterrupt(digitalPinToInterrupt(irPin), countInterrupt, FALLING); // Attach interrupt to the IR sensor pin
  lastTime = millis(); // Initialize the last time
  interruptCount = 0; // Initialize interrupt count
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
        desiredSpeed = 80;
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

  // Ramping up or down the speed gradually
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= rampInterval) {
    previousMillis = currentMillis;
    if (currentSpeed < desiredSpeed) {
      currentSpeed = min(currentSpeed + rampSpeedIncrement, desiredSpeed);
    } else if (currentSpeed > desiredSpeed) {
      currentSpeed = max(currentSpeed - rampSpeedIncrement, desiredSpeed);
    }
    analogWrite(ena, currentSpeed);
  }

  // RPM measurement
  if (millis() - lastTime >= 1000) { // Check if one second has passed
    noInterrupts(); // Disable interrupts to ensure atomicity
    unsigned long count = interruptCount; // Store interrupt count
    interruptCount = 0; // Reset interrupt count
    interrupts(); // Enable interrupts
    
    // Calculate RPM
    unsigned long rpm = (count * 60)*10; // Multiply interrupt count by 60 to get RPM
    
    // Send RPM value to serial port
    Serial.println(rpm);
    
    lastTime = millis(); // Update last time
  }

  // Set motor direction (example: forward)
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
}

void countInterrupt() {
  interruptCount++; // Increment interrupt count
}