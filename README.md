# Automated Attendance Tracking and Productivity Analytics using Face Recognition
![Python](https://img.shields.io/badge/Python-3.10-python)
![NumPy](https://img.shields.io/badge/NumPy-1.25.2-cyan)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9-blue)
![face_recognition](https://img.shields.io/badge/face--recognition-1.3.0-brown)
![PySpark](https://img.shields.io/badge/Pyspark-3.5.1-orange)

## Introduction

This project is a sophisticated end-to-end solution designed to automate attendance tracking using face recognition and analyze employee productivity. It encompasses three main stages: data ingestion, data transformation, and application in productivity analysis. This tool is particularly useful for environments that require monitoring entry and exit times, such as offices, schools, and conferences.


## Features
- **Real-time face detection and recognition**: Real-time Face Detection and Recognition: Efficiently identifies and logs known faces from the webcam feed.
- **Accurate Attendance Logging**: Records attendance with precise timestamps.
- **Session Tracking**: Logs the "IN"s and "OUT"s for each person per session.
- **Data Cleaning**: Filters out brief appearances (less than 1 minute) to maintain accurate records.
- **Comprehensive Data Transformation**: Processes raw attendance data to clean and organize it for further analysis.
- **Productivity Analysis**: Analyzes attendance data to provide insights into employee productivity.


## Getting Started

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/debanjansaha-git/Virtual_Attendance_System
   ```
2. Navigate to the project directory:
   ```bash
   cd Virtual_Attendance_System
   ```

3. Install the pre-requisites for face-recognition
   ```
   brew install cmake
   brew install dlib
   ```

4. You can install the required libraries using pip:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

### Execute Program

To run the code, simply execute the script in a Python environment. 
   ```bash
   python attendance.py
   ```

The script will open a window showing the webcam feed and will begin detecting and recognizing faces.

Once the data has been captured successfully, run the data transformation scipt
   ```bash
   python data_transformation.py
   ```

Once all the data is ready, we can execute applications built to monitor employee attendance and productivity by running the interactive notebook: `productivity_analytics.ipynb` using either Jupyter or Google Colab or similar tools.

## Stages of the Project

## 1. Data Ingestion

The initial stage involves capturing attendance data using face recognition. The system uses a webcam to detect and recognize faces in real-time, logging attendance details in a CSV file.

**Key Points**:

- Uses face_recognition and opencv-python libraries.
- Captures images from a webcam and matches them against a known database of faces.
- Logs attendance with timestamps in attendance.csv.


## 2. Data Transformation

The next stage involves transforming the raw attendance data into a structured format suitable for downstream analysis using PySpark.

- Reads the raw attendance CSV file.
- Filters out intermittent "IN" and "OUT" entries within 2 seconds.
- Tracks the first "IN" and last "OUT" for each person.
- Outputs the cleaned data to a new CSV file.

## 3. Data Science Use Case: Employee Attendance and Productivity Analysis

This stage involves analyzing the transformed attendance data to gain insights into employee productivity.

### Objective
To analyze employee attendance data to gain insights into attendance patterns, productivity, and behavior. This analysis aims to uncover trends, identify anomalies, and provide actionable recommendations to improve productivity and attendance management.

### Data Processing and Feature Engineering
- **Data Cleaning**: Remove invalid or incomplete records and handle missing values.
- **Feature Engineering**: Create features such as total hours worked, number of breaks, late arrivals, and early departures.
- **Session Tracking**: Identify and track sessions for each employee to log the first "IN" and the last "OUT" of each day.

### Key Metrics
- **Total Hours Worked**: Calculate the total hours worked by each employee each day.
- **Late Arrivals**: Identify instances where employees arrived after the designated start time.
- **Early Departures**: Identify instances where employees left before the designated end time.
- **Number of Breaks**: Count the number of breaks taken by each employee each day.
- **Long Breaks**: Identify breaks that are longer than a specified duration.

### Statistical Analysis
- **Descriptive Statistics**: Summarize key metrics such as mean, median, and standard deviation.
- **Correlation Analysis**: Examine the relationship between the number of breaks and total hours worked.

#### Hypothesis Testing:
1. **ANOVA**: Compare the mean number of late arrivals and early departures across different employees.
2. **T-test**: Compare the mean total hours worked before and after implementing any policy changes.
3. **Shapiro-Wilk Test**: Test for normality of the distribution of arrival times.

### Machine Learning
Predictive Modeling: Build models to predict employee productivity based on attendance patterns.
Anomaly Detection: Identify unusual attendance patterns that may indicate issues such as absenteeism or lack of productivity.

### Visualization
- **Time Series Analysis**: Visualize attendance patterns over time.
- **Heatmaps**: Show the frequency of late arrivals and early departures.
- **Box Plots**: Display the distribution of total hours worked and breaks taken.
Applications
- **HR Management**: Use insights from the analysis to improve attendance policies and manage employee performance.
- **Employee Engagement**: Identify employees who may need support or intervention to improve attendance.
- **Productivity Optimization**: Develop strategies to maximize productivity based on attendance data.

  #### Please Find the visualization dashboard:

![Tableau Dashboard]([https://img.shields.io/badge/NumPy-1.25.2-cyan](https://public.tableau.com/views/AttendanceAnalysis_17176390759380/AnalysisofAttendance?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link))
  

## Limitations
Some limitations of this module include:

- The module relies on accurate encoding of known faces, thus if the images of known faces in the "KnownDB" folder are of low quality or do not accurately represent the person, the module may not correctly match and record attendance.
- The module can only detect people in the knownDB folder, it is not able to detect unknown people.

## Conclusion

This face recognition and attendance tracking system is a useful tool for logging attendance in real-time using a webcam. With further enhancements, it can be integrated into larger systems for automated attendance management.

Feel free to contribute to this project or provide feedback to improve its functionality.
