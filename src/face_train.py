import os
import cv2 as cv
import numpy as np

# getting data
labels = []
celebs = []
faces = []
# loads a haarcascade.xml file (avaiable at opencv repo)
cascade = cv.CascadeClassifier("../haarcascade_face.xml")

for folder in os.listdir("../training_images"):
    # gets all the data
    if(folder[0] == "."):
        continue
    celebs.append(folder)

# detects faces on the data
for folder in os.listdir("../training_images"):
    if(folder[0] == "."):
        continue
    label = celebs.index(folder)
    dir_path = os.path.join("../training_images", folder)
    for imgs in os.listdir(dir_path):
        if(imgs[0] == "."):
            continue
        img_path = os.path.join(dir_path, imgs)
        img_obj = cv.imread(img_path)
        gray_img_obj = cv.cvtColor(img_obj, cv.COLOR_BGR2GRAY)
        faces_detect = cascade.detectMultiScale(
            gray_img_obj, scaleFactor=1.1, minNeighbors=4)

        for(x, y, z, w) in faces_detect:
            face_region = gray_img_obj[y:y+w, x:x+z]
            # adds data to the list
            labels.append(label)
            faces.append(face_region)

labels = np.array(labels)
faces = np.array(faces, dtype="object")

# trains the model from the data
recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.train(faces, labels)

# saves the trained model in .yml file
recognizer.save("../trainer.yml")
np.save("../faces.npy", faces)
np.save("../labels.npy", labels)
