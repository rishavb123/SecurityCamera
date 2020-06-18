import numpy as np
import cv2

from drawing import draw_border
from colors import GREEN, BLUE, to_bgr_from_rgb
from config import MOTION_THRESHOLD

classifier = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

old, frame = cap.read()

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = classifier.detectMultiScale(gray)

    img = cv2.subtract(old, frame)
    _, img = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)
    img2 = frame.copy()

    diff = np.linalg.norm(img)

    if diff > MOTION_THRESHOLD:
        print("Motion Number: ", diff)

    if len(faces) > 0:
        faces = sorted(faces, key=lambda face: -face[2] * face[3])

        x, y, w, h = faces[0]
        draw_border(img, (x, y), (x + w, y + h), to_bgr_from_rgb(GREEN), 3, 10, 20)
        draw_border(img2, (x, y), (x + w, y + h), to_bgr_from_rgb(BLUE), 3, 10, 20)

    cv2.imshow('frame', np.concatenate((img, img2), axis=1))

    old = frame

    if cv2.waitKey(1) & 0xFF in [ord('q'), 27]:
        break

cap.release()
cv2.destroyAllWindows()
