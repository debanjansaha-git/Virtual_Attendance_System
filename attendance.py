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
import os
from datetime import datetime

cap = cv2.VideoCapture(0)
scaleFactor = 4

path = "KnownDB"
images = []
classnames = []
myList = os.listdir(path)

for cl in myList:
    curImg = cv2.imread(f"{path}/{cl}")
    images.append(curImg)
    classnames.append(os.path.splitext(cl)[0].upper())


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


knownFaces = findEncodings(images)

# Dictionary to keep track of the status of each person
attendance_status = {name: "OUT" for name in classnames}


def markAttendance(name, status):
    with open("attendance.csv", "a") as f:
        now = datetime.now()
        dateStr = now.strftime("%Y-%m-%d %H:%M:%S")
        f.writelines(f"\n{name},{status},{dateStr}")


while True:
    _, img = cap.read()
    imgC = cv2.resize(img, (0, 0), None, (1 / scaleFactor), (1 / scaleFactor))
    imgC = cv2.cvtColor(imgC, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgC)
    encodeCurFrame = face_recognition.face_encodings(imgC, facesCurFrame)

    current_frame_names = []

    for faceEnc, faceLoc in zip(encodeCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(knownFaces, faceEnc)
        faceDist = face_recognition.face_distance(knownFaces, faceEnc)
        matchIndex = np.argmin(faceDist)

        if matches[matchIndex]:
            name = classnames[matchIndex].upper()
            current_frame_names.append(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = (
                y1 * scaleFactor,
                x2 * scaleFactor,
                y2 * scaleFactor,
                x1 * scaleFactor,
            )
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 0, 255), cv2.FILLED)
            cv2.putText(
                img,
                name,
                (x1 + 6, y2 - 6),
                cv2.FONT_HERSHEY_COMPLEX_SMALL,
                1,
                (255, 255, 255),
                2,
            )

            if attendance_status[name] == "OUT":
                markAttendance(name, "IN")
                attendance_status[name] = "IN"

    # Check for people who have left the frame
    for name in attendance_status.keys():
        if name not in current_frame_names and attendance_status[name] == "IN":
            markAttendance(name, "OUT")
            attendance_status[name] = "OUT"

    cv2.imshow("Result", img)
    # press keyboard 'q' to quit()
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
