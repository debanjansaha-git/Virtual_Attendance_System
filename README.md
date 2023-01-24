# Virtual Attendance System using Face Recognition
![Python](https://img.shields.io/badge/Python-3.x-python)
![NumPy](https://img.shields.io/badge/NumPy-1.19.3-orange)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5.1-blue)
![face_recognition](https://img.shields.io/badge/face--recognition-1.4.0-brown)


## Introduction

This module is a face recognition and attendance tracking tool that detects faces from live webcam and records attendance in a csv file if a known face is found, which can be used to load the data into a database. 
The module uses the `face_recognition` library to perform face detection and recognition. The webcam input is captured using the cv2 library.


## Getting Started

The following dependencies need to be installed before running the code:

`numpy`
`cv2`
`face_recognition`
`os`
`datetime`

## Execute Program

To run the code, simply execute the script in a Python environment. The script will open a window showing the webcam feed and will begin detecting and recognizing faces.

## Database

The script uses a directory called 'KnownDB' to store images of known faces for comparison. The name of the image files are used as the name of the person for attendance tracking. The script reads all images from this directory and encodes them for comparison with webcam feed.

## Attendance Tracking

The script records attendance in a csv file called 'attendance.csv'. Each row of the file contains the name of the person and the time of attendance. If a known face is detected, the script checks if the person's name is already in the attendance file. If not, the script adds a new row to the file with the person's name and the current time.
This csv file is then used to load the records into any cloud database table which can be used to create a view to display the results in a dashboard.

## Functionality

The code uses the `cv2` library to capture video frames from the computer's webcam, and the `face_recognition` library to detect faces within these frames. The `face_locations` function from the `face_recognition.api` module is used to detect the coordinates of the bounding boxes around faces within an image, and the `face_encodings` function is used to generate a 128-dimensional encoding for each face. These encodings are used to compare and match the faces in the webcam feed to the known faces in the dataset.

The module reads the images of the known people from a folder called "KnownDB" and encodes the images using the `findEncodings` function, which applies the `face_encodings` function to each image. The resulting encodings are stored in a variable called `knownFaces`.

The `while True` loop in the code captures frames from the webcam and resizes them for faster processing. The `face_locations` and `face_encodings` functions are applied to the current frame to detect faces and generate encodings. The `compare_faces` function is then used to compare the encodings of the detected faces to the known faces in the dataset, and the `face_distance` function is used to calculate the distance between the encodings. The face with the smallest distance is considered the best match and its corresponding name is displayed on the screen.

The `markAttendance` function is used to record the attendance of the recognized person in a CSV file with the current time stamp.

## Usage

   1. Place the images of known faces in a folder named "KnownDB" in the same directory as the script.
   2. Run the script using `python3 script_name.py`
   3. Allow the script to access the webcam when prompted
   4. The script will run in a loop and display the video feed from the webcam on the screen. If a known face is detected, the name of the person will be displayed on the screen and recorded in the "attendance.csv" file.
   5. Press 'q' on the keyboard to quit the script.

## Customization

The scaleFactor variable can be adjusted to change the size of the video feed displayed on the screen.
The format of the date and time recorded in the "attendance.csv" file can be changed in the markAttendance function.
Additional functionality can be added to the script by modifying the markAttendance function.

## Limitations
Some limitations of this module include:

- The module only detects one face per frame, thus it may not accurately record attendance if multiple faces are present in the frame.
- The module relies on accurate encoding of known faces, thus if the images of known faces in the "KnownDB" folder are of low quality or do not accurately represent the person, the module may not correctly match and record attendance.
- The module requires a webcam to function and cannot be used with pre-recorded video or images.
- The module uses the 'attendance.csv' file to record attendance, if the file is not present or is not in the correct format, the module will not function properly.
- The module uses the datetime library to record the time of attendance, it may not work properly if the system time is not accurate.
- If a new user wants to be added, their images should be added to the 'KnownDB' folder and the module should be run again to include the new user.
- The module is not resistant to spoofing/fake faces.
- The module can only detect people in the knownDB folder, it is not able to detect unknown people.
