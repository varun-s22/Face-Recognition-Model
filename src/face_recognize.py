import cv2 as cv
import numpy as np
import os

celebs = []

for folder in os.listdir("../training_images"):
    if(folder[0] == "."):
        continue
    celebs.append(folder)

# loads up the trained data
cascade = cv.CascadeClassifier("../haarcascade_face.xml")
faces = np.load("../faces.npy", allow_pickle=True)
labels = np.load("../labels.npy")

# loads the trained .yml file
recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read("../trainer.yml")

# gets the image from the dir
img = cv.imread("../untrained_images/taytay2.jpeg")
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
faces_detect = cascade.detectMultiScale(
    gray_img, scaleFactor=1.1, minNeighbors=4)

# detects the face
for(x, y, z, w) in faces_detect:
    face_region = gray_img[y:y+w, x:x+z]
    label, confidence = recognizer.predict(face_region)
    cv.putText(img, str(celebs[label]), (500, 500), cv.FONT_HERSHEY_COMPLEX,
               3.0, (0, 255, 0), thickness=5)
    cv.rectangle(img, (x, y), (x+z, y+w), (0, 255, 0), thickness=8)

# recognizes with help of model
cv.imshow("unknown person", img)
cv.waitKey(0)
