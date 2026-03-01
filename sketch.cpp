#include <Servo.h>

#define TRIG_PIN 9
#define ECHO_PIN 10
#define SERVO_PIN 6

Servo servo;

int angle = 30;
bool forward = true;

void setup() {

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  servo.attach(SERVO_PIN);

  Serial.begin(115200);
}

void loop() {

  // Move servo
  servo.write(angle);

  if (forward) angle++;
  else angle--;

  if (angle >= 150) forward = false;
  if (angle <= 30) forward = true;

  delay(20);

  float distance = measureDistance();

  // Send to PC
  Serial.print(angle);
  Serial.print(",");
  Serial.println(distance);
}

float measureDistance() {

  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG_PIN, LOW);

  unsigned long duration = pulseIn(ECHO_PIN, HIGH, 30000);

  if (duration == 0)
    return -1;

  float distance = duration * 0.0343 / 2;

  return distance;
}