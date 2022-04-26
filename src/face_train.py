import os
import cv2 as cv
import time
import numpy as np

def takePicture(folder_name):
    # takes picture from the webcam
    cap = cv.VideoCapture(0)
    startTime = time.time()
    ctr = 0
    while int(time.time()-startTime) <= 6:
        isCaptured, frame = cap.read()
        if not isCaptured:
            print("Can't receive frame ")
            break
        gray_img_obj = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imwrite(f"../photos/{folder_name}/{ctr}.jpg", gray_img_obj)
        ctr += 1
        cv.imshow("frame", frame)
        if(cv.waitKey(1) == ord("q")):
            break
    cap.release()
    cv.destroyAllWindows()

# getting data
labels = []
persons = []
faces = []
# loads a haarcascade.xml file (avaiable at opencv repo)
cascade = cv.CascadeClassifier("../haarcascade_face.xml")
folder_name=input("Enter folder name: ")
parent="../photos"
pathToFolder=os.path.join(parent,folder_name)
os.mkdir(pathToFolder)
takePicture(folder_name)

for folder in os.listdir(parent):
    if(folder[0]=="."):
        continue
    persons.append(folder)
# detects faces on the data
for folder in os.listdir(parent):
    if(folder[0] == "."):
        continue
    label=persons.index(folder)
    folder_path = os.path.join(parent, folder)
    for img in os.listdir(folder_path):
        img_path=os.path.join(folder_path,img)
        img_obj=cv.imread(img_path)
        gray_img_obj=cv.cvtColor(img_obj,cv.COLOR_BGR2GRAY)
        faces_detect = cascade.detectMultiScale(gray_img_obj, scaleFactor=1.1, minNeighbors=4)
        for(x, y, z, w) in faces_detect:
            face_region = gray_img_obj[y:y+w, x:x+z]
            # adds data to the list
            labels.append(label)
            faces.append(face_region)  

labels22 = np.array(labels)
faces22 = np.array(faces, dtype="object")

# trains the model from the data
recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.train(faces22, labels22)

# saves the trained model in .yml file
recognizer.save("../trainerFaces.yml")
np.save("../faces2.npy", faces22)
np.save("../labels2.npy", labels22)