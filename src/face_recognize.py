import cv2 as cv
import numpy as np
import os
import time
from csv import writer
from datetime import datetime

def recognize()->None:
    # recognizes person based on the data
    
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

    startTime = time.time()
    while int(time.time()-startTime) <= 12:
        isCaptured,img=cap.read()
        if not isCaptured:
            break

        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces_detect = cascade.detectMultiScale(
            gray_img, scaleFactor=1.1, minNeighbors=3)

        # detects the face
        for(x, y, z, w) in faces_detect:
            face_region = gray_img[y:y+w, x:x+z]
            label, confidence = recognizer.predict(face_region)
            if(confidence>=45):
                cv.putText(img, str(persons[label]), (500, 500), cv.FONT_HERSHEY_COMPLEX,
                        3.0, (0, 255, 0), thickness=5)

                with open("../users.csv","w") as csvFile:
                    # writes the details of the user logged in, to maintain data
                    ww=writer(csvFile)
                    ww.writerow([str(persons[label]),datetime.now().strftime("%d/%b/%Y %H:%M:%S")])
            cv.rectangle(img, (x, y), (x+z, y+w), (0, 255, 0), thickness=8)

        # recognizes with help of model
        cv.imshow("unknown person", img)
        if(cv.waitKey(1)==ord("q")):
            break
    cap.release()
    cv.destroyAllWindows()