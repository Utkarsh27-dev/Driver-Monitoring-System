#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Servo.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

Servo steeringServo;

// ---------------- PINS ----------------
const int buzzerPin = 7;
const int relayPin = 8;
const int servoPin = 9;

// ---------------- VARIABLES ----------------
String state = "NORMAL";

// =====================================================
// SETUP
// =====================================================

void setup() {

  Serial.begin(9600);

  pinMode(buzzerPin, OUTPUT);
  pinMode(relayPin, OUTPUT);

  digitalWrite(relayPin, LOW);

  steeringServo.attach(servoPin);
  steeringServo.write(90);

  // OLED INIT
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    while (true);
  }

  display.clearDisplay();
  display.setTextColor(WHITE);

  display.setTextSize(2);
  display.setCursor(10, 20);
  display.println("SYSTEM");
  display.setCursor(20, 45);
  display.println("READY");

  display.display();

  delay(2000);
}

// =====================================================
// LOOP
// =====================================================

void loop() {

  // SERIAL READ
  if (Serial.available()) {

    state = Serial.readStringUntil('\n');
    state.trim();
  }

  // STATE HANDLING
  if (state == "NORMAL") {
    handleNormal();
  }

  else if (state == "WARNING") {
    handleWarning();
  }

  else if (state == "DROWSY") {
    handleDrowsy();
  }

  else if (state == "DISTRACTED") {
    handleDistracted();
  }
}

// =====================================================
// NORMAL
// =====================================================

void handleNormal() {

  digitalWrite(relayPin, LOW);

  noTone(buzzerPin);

  steeringServo.write(90);

  display.clearDisplay();

  display.setTextSize(2);
  display.setCursor(15, 15);
  display.println("NORMAL");

  display.setTextSize(1);
  display.setCursor(25, 45);
  display.println("DRIVE SAFE");

  display.display();

  delay(100);
}

// =====================================================
// WARNING
// =====================================================

void handleWarning() {

  digitalWrite(relayPin, LOW);

  display.clearDisplay();

  display.setTextSize(2);
  display.setCursor(8, 15);
  display.println("WARNING");

  display.setTextSize(1);
  display.setCursor(25, 45);
  display.println("BE ALERT");

  display.display();

  // buzzer
  tone(buzzerPin, 1500);
  delay(300);

  noTone(buzzerPin);
  delay(200);

  tone(buzzerPin, 1500);
  delay(300);

  noTone(buzzerPin);

  // servo jitter
  for (int i = 0; i < 3; i++) {

    steeringServo.write(80);
    delay(120);

    steeringServo.write(100);
    delay(120);
  }

  steeringServo.write(90);
}

// =====================================================
// DROWSY
// =====================================================

void handleDrowsy() {

  digitalWrite(relayPin, HIGH);

  display.clearDisplay();

  display.setTextSize(2);
  display.setCursor(10, 15);
  display.println("DROWSY");

  display.setTextSize(1);
  display.setCursor(5, 45);
  display.println("STOP VEHICLE");

  display.display();

  // alarm
  for (int i = 0; i < 10; i++) {

    tone(buzzerPin, 2000);
    delay(100);

    noTone(buzzerPin);
    delay(100);
  }

  // strong turn
  steeringServo.write(20);
  delay(700);

  steeringServo.write(160);
  delay(700);

  steeringServo.write(90);
}

// =====================================================
// DISTRACTED
// =====================================================

void handleDistracted() {

  digitalWrite(relayPin, HIGH);

  display.clearDisplay();

  display.setTextSize(2);
  display.setCursor(0, 15);
  display.println("DISTRACT");

  display.setTextSize(1);
  display.setCursor(10, 45);
  display.println("FOCUS ROAD");

  display.display();

  // buzzer
  for (int i = 0; i < 3; i++) {

    tone(buzzerPin, 1700);
    delay(500);

    noTone(buzzerPin);
    delay(250);
  }

  // servo shake
  for (int i = 0; i < 5; i++) {

    steeringServo.write(70);
    delay(120);

    steeringServo.write(110);
    delay(120);
  }

  steeringServo.write(90);
}