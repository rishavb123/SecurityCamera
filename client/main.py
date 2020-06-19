import numpy as np
import cv2
import base64
import socketio
import time

from drawing import draw_border
from colors import GREEN, BLUE, ORANGE, to_bgr_from_rgb
from config import MOTION_THRESHOLDS, RUNNING_AVERAGE_LENGTH

classifier = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

sio.connect('http://localhost:3000')

old, frame = cap.read()

motion_levels = []

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = classifier.detectMultiScale(gray)

    img = cv2.absdiff(old, gray)
    old = gray
    img = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)[1]
    img = cv2.dilate(img, None, iterations=2)

    cnts, hierarchy = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, cnts, -1, to_bgr_from_rgb(ORANGE))

    img2 = frame.copy()

    diff = np.linalg.norm(img)

    motion_level = 0

    for threshold in MOTION_THRESHOLDS:
        if diff > threshold: 
            motion_level += 1
        else:
            break

    motion_levels.append(motion_level)

    print('Motion Level:', '[' + '+' * motion_level + ' ' * (len(MOTION_THRESHOLDS) - motion_level) + ']', motion_level, '/',  len(MOTION_THRESHOLDS), '\tRunning Average: ', sum(motion_levels[-RUNNING_AVERAGE_LENGTH:]) / min(len(motion_levels), RUNNING_AVERAGE_LENGTH))

    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    if len(faces) > 0:
        faces = sorted(faces, key=lambda face: -face[2] * face[3])

        x, y, w, h = faces[0]
        draw_border(img, (x, y), (x + w, y + h), to_bgr_from_rgb(GREEN), 3, 10, 20)
        draw_border(img2, (x, y), (x + w, y + h), to_bgr_from_rgb(BLUE), 3, 10, 20)

    final = np.concatenate((img, img2), axis=1)

    encoded_final = str(base64.b64encode(cv2.imencode('.jpg', final)[1].tobytes()))[2:-1]
    sio.emit('frame', encoded_final)

    # cv2.imshow('frame', final)

    if cv2.waitKey(1) & 0xFF in [ord('q'), 27]:
        break

cap.release()
cv2.destroyAllWindows()
