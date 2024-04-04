#include <stddef.h>

// Pin definitions
constexpr uint8_t MOTOR_PWM_PIN = 10;
constexpr uint8_t MOTOR_CONTROL_PIN_1 = 9;
constexpr uint8_t MOTOR_CONTROL_PIN_2 = 8;

// Helpful constants

// Minimum required PWM value to start the motor spinning
constexpr uint8_t MINIMUM_MOTOR_PWM = 90;

// Motor class for controlling current ramping
class Motor {
  public:
    Motor() : m_desiredPWM(0), m_currentPWM(0) {}

    // Sets the desired PWM for the motor to be set to, which will eventually
    // be reached.
    void setDesiredPWM(uint8_t pwm) {
      this->m_desiredPWM = pwm;
    }

    // Gets the actual current PWM setting for the motor
    uint8_t getCurrentPWM() {
      return this->m_currentPWM;
    }

    // Should be called as close to every 15 milliseconds as you can manage
    // DEFINITELY not more often
    void update() {
      // Get the difference between the desired PWM and the current PWM as a signed integer
      const int16_t settingDelta = (int16_t)(static_cast<int16_t>(this->m_desiredPWM) - static_cast<int16_t>(this->m_currentPWM));

      if (settingDelta > 0) {
        // Calculate our little limit function
        // This limits the maximum derivative of our PWM signal over time
        // This will keep the instantaneous current in check (below 2 amps)
        if ((this->m_desiredPWM > this->m_currentPWM) && (this->m_currentPWM < MINIMUM_MOTOR_PWM)) {
          // We're currently under the minimum motor speed (which would be possible after the motor has started)
          // So we can just jump to the minimum motor speed and be safe
          this->m_currentPWM = MINIMUM_MOTOR_PWM + 1;
        } else {
          // We derived a little exponential curve that allows us to control the PWM signal derivative
          
          // A 32-bit version of our current setting for the intermediate math
          // This is offset as part of our mathematical function
          const int32_t offsetSetting = ((int32_t) this->m_currentPWM - 50);
          const uint8_t maximumDelta = (uint8_t)(((offsetSetting * offsetSetting) / 9000) + 1);

          // Change by either the limited max delta or the setting delta
          this->m_currentPWM += min(maximumDelta, (uint8_t)(settingDelta));
        }
      } else {
        // Our derivative is negative (we're trying to command the motor to slow down)
        // So directly slowing down is fine
        this->m_currentPWM = this->m_desiredPWM;
      }
    }

  private:
    uint8_t m_desiredPWM;
    uint8_t m_currentPWM;
};

Motor motor = Motor();

void setup() {
  Serial.begin(115200);e
  
  pinMode(MOTOR_PWM_PIN, OUTPUT); // Motor speed control pin
  pinMode(MOTOR_CONTROL_PIN_1, OUTPUT); // Motor control pin 1
  pinMode(MOTOR_CONTROL_PIN_2, OUTPUT); // Motor control pin 2
  
  analogWrite(MOTOR_PWM_PIN, 0); // Initially set speed to 0

    // Set motor direction (example: forward)
  digitalWrite(MOTOR_CONTROL_PIN_1, HIGH);
  digitalWrite(MOTOR_CONTROL_PIN_2, LOW);
}

void loop() {
  if (Serial.available()) {
    const uint8_t inputPWMValue = Serial.read();
    motor.setDesiredPWM(inputPWMValue);
  }

  delay(15);

  motor.update();
  
  // Set the motor speed to the desired speed
  analogWrite(MOTOR_PWM_PIN, motor.getCurrentPWM());
}
