import cv2 as cv
import numpy as np
import os

persons = []
parent="../photos"

# loads up the trained data
for folder in os.listdir(parent):
    if(folder[0]=="."):
        continue
    persons.append(folder)
cascade = cv.CascadeClassifier("../haarcascade_face.xml")
faces = np.load("../faces2.npy", allow_pickle=True)
labels = np.load("../labels2.npy")

# loads the trained .yml file
recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read("../trainerFaces.yml")

# gets the image from the dir
cap=cv.VideoCapture(0)
while True:
    isCaptured,img=cap.read()
    if not isCaptured:
        break
    # img = cv.imread("../photos/45.jpg")
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces_detect = cascade.detectMultiScale(
        gray_img, scaleFactor=1.1, minNeighbors=4)

    # detects the face
    for(x, y, z, w) in faces_detect:
        face_region = gray_img[y:y+w, x:x+z]
        label, confidence = recognizer.predict(face_region)
        if(confidence>=45):
            cv.putText(img, str(persons[label]), (500, 500), cv.FONT_HERSHEY_COMPLEX,
                    3.0, (0, 255, 0), thickness=5)
        cv.rectangle(img, (x, y), (x+z, y+w), (0, 255, 0), thickness=8)

    # recognizes with help of model
    cv.imshow("unknown person", img)
    if(cv.waitKey(1)==ord("q")):
        break
cap.release()
cv.destroyAllWindows()