# Intelligent Driver Monitoring System 🚗

A real-time driver safety system that detects driver drowsiness and distraction using facial landmark detection and provides hardware alerts through Arduino.


# Features

* Drowsiness detection using Eye Aspect Ratio (EAR)
* Driver distraction detection
* Real-time webcam monitoring
* OLED display alerts
* Buzzer warning system
* Servo motor alert action
* Relay-based control
* Voice alerts
* Python and Arduino integration



# Technologies Used

## Software

* Python
* OpenCV
* MediaPipe
* PySerial
* pyttsx3

## Hardware

* Arduino UNO
* OLED Display
* Servo Motor
* Relay Module
* Buzzer
* LED
* Webcam



# Working

1. Webcam captures live video
2. Face landmarks are detected using MediaPipe
3. EAR is calculated to monitor eye closure
4. Driver distraction is detected using face orientation
5. Driver state is classified as:

   * NORMAL
   * WARNING
   * DROWSY
   * DISTRACTED
6. Python sends state data to Arduino
7. Arduino activates buzzer, OLED, relay, and servo alerts



# Hardware Connections

## OLED

* VCC → 5V
* GND → GND
* SDA → A4
* SCL → A5

## Relay

* IN → D8
* VCC → 5V
* GND → GND

## Servo

* Signal → D9
* VCC → External 5V
* GND → Common GND

---

# How to Run

**##Upload the sketch file to Arduino**

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

```bash 
source venv/bin/activate
```

## Install Requirements

```bash 
pip install opencv-python mediapipe pyserial pyttsx3 numpy
```

## Run Project

```bash 
python detect.py
```



# Applications

* Driver safety systems
* Smart vehicle monitoring
* Accident prevention
* Fleet monitoring



# Future Improvements

* Raspberry Pi integration
* Infrared camera support
* Yawning detection
* Mobile app integration



# Author

Utkarsh
