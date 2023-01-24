# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 04:39:47 2021
@description: This module detects faces from live webcam and performs face recognition
              If a known face is found, then the attendance is recorded in a csv file
@author :     Debanjan Saha
@licence:     MIT License
"""

import numpy as np
import cv2
import face_recognition
from face_recognition.api import face_locations
import os
from datetime import datetime

cap = cv2.VideoCapture(0)
scaleFactor = 4

path = 'KnownDB'
images = []
classnames = []
myList = os.listdir(path)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classnames.append(os.path.splitext(cl)[0])



def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

knownFaces = findEncodings(images)

def markAttendance(name):
    with open('attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dateStr = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dateStr}')



while True:
    _, img = cap.read()
    imgC = cv2.resize(img, (0,0), None, (1/scaleFactor), (1/scaleFactor))
    imgC = cv2.cvtColor(imgC, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgC)
    encodeCurFrame = face_recognition.face_encodings(imgC, facesCurFrame)

    for faceEnc, faceLoc in zip(encodeCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(knownFaces, faceEnc)
        faceDist = face_recognition.face_distance(knownFaces, faceEnc)
        matchIndex = np.argmin(faceDist)

        if matches[matchIndex]:
            name = classnames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*scaleFactor, x2*scaleFactor, y2*scaleFactor, x1*scaleFactor
            cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,255), 2)
            cv2.rectangle(img, (x1,y2-35), (x2, y2), (255,0,255), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 2)
            markAttendance(name)

    cv2.imshow("Result", img)
    # press keyboard 'q' to quit()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break