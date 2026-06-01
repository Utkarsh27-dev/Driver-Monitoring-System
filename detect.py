import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import pyttsx3
import threading
import time
import serial
import serial.tools.list_ports

# -------------------- SERIAL (auto-detect) --------------------
def find_arduino():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if "usb" in p.device.lower():
            return p.device
    return None

PORT = find_arduino()
arduino = None

if PORT:
    try:
        arduino = serial.Serial(PORT, 9600, timeout=1)
        time.sleep(2)
        print(f"Connected to {PORT}")
    except:
        print("Arduino connection failed")
else:
    print("No Arduino found")

# -------------------- VOICE (single worker) --------------------
engine = pyttsx3.init()
engine.setProperty('rate', 170)

speak_queue = deque()
speaking = False

def voice_worker():
    global speaking
    while True:
        if speak_queue and not speaking:
            speaking = True
            text = speak_queue.popleft()
            engine.say(text)
            engine.runAndWait()
            speaking = False
        time.sleep(0.1)

threading.Thread(target=voice_worker, daemon=True).start()

def speak(text):
    if not speak_queue or speak_queue[-1] != text:
        speak_queue.append(text)

# -------------------- MEDIAPIPE --------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def ear(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

# -------------------- CAMERA --------------------
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

# -------------------- STATE MACHINE --------------------
state = "NORMAL"
last_sent = ""
ear_hist = deque(maxlen=10)

closed_frames = 0
no_face_start = None
last_alert = 0

EAR_TH = 0.23
WARN_F = 15
DROW_F = 35
ALERT_INTERVAL = 3

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = face_mesh.process(rgb)

    new_state = "NORMAL"

    if res.multi_face_landmarks:
        no_face_start = None

        pts = np.array([(int(p.x*w), int(p.y*h)) for p in res.multi_face_landmarks[0].landmark])

        # EAR
        e = (ear(pts[LEFT_EYE]) + ear(pts[RIGHT_EYE])) / 2
        ear_hist.append(e)
        smooth = np.mean(ear_hist)

        if smooth < EAR_TH:
            closed_frames += 1
        else:
            closed_frames = 0

        # Distraction (nose deviation)
        nose = pts[1]
        if abs(nose[0] - w//2) > w*0.15:
            new_state = "DISTRACTED"
        elif closed_frames > DROW_F:
            new_state = "DROWSY"
        elif closed_frames > WARN_F:
            new_state = "WARNING"

        cv2.putText(frame, f"EAR:{round(smooth,3)}", (20,100), 0, 0.7, (255,255,255),2)

    else:
        if not no_face_start:
            no_face_start = time.time()
        elif time.time() - no_face_start > 2:
            new_state = "DISTRACTED"

    # -------------------- STATE CHANGE --------------------
    if new_state != state:
        state = new_state
        print("STATE:", state)

        # Send to Arduino
        if arduino:
            try:
                arduino.write((state + "\n").encode())
            except:
                pass

    # -------------------- VOICE --------------------
    now = time.time()
    if now - last_alert > ALERT_INTERVAL:
        if state == "WARNING":
            speak("Stay alert")
        elif state == "DROWSY":
            speak("Wake up immediately")
        elif state == "DISTRACTED":
            speak("Keep your eyes on the road")
        last_alert = now

    # -------------------- DISPLAY --------------------
    color = {
        "NORMAL": (0,255,0),
        "WARNING": (0,165,255),
        "DROWSY": (0,0,255),
        "DISTRACTED": (255,0,0)
    }.get(state, (255,255,255))

    cv2.putText(frame, f"STATE: {state}", (20,50), 0, 1, color, 3)

    cv2.imshow("Driver Monitor", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()