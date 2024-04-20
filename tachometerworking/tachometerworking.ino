// Define the pins
const int irPin = 2; // IR sensor pin
const int ledPin = 13; // On-board LED pin

volatile unsigned long lastTime;
volatile unsigned long interruptCount; // Count of interrupts within one second
volatile boolean flag;

void setup() {
  Serial.begin(9600); // Start serial communication
  pinMode(irPin, INPUT); // Initialize IR sensor pin as input
  pinMode(ledPin, OUTPUT); // Initialize LED pin as output
  
  attachInterrupt(digitalPinToInterrupt(irPin), countInterrupt, FALLING); // Attach interrupt to the IR sensor pin
  lastTime = millis(); // Initialize the last time
  interruptCount = 0; // Initialize interrupt count
}

void loop() {
  if (millis() - lastTime >= 1000) { // Check if one second has passed
    noInterrupts(); // Disable interrupts to ensure atomicity
    unsigned long count = interruptCount; // Store interrupt count
    interruptCount = 0; // Reset interrupt count
    interrupts(); // Enable interrupts
    
    // Calculate RPM
    unsigned long rpm = (count * 60)/3; // Multiply interrupt count by 60 to get RPM
    
    // Send RPM value to serial port
    Serial.println(rpm);
    
    lastTime = millis(); // Update last time
  }
}

void countInterrupt() {
  interruptCount++; // Increment interrupt count
}
