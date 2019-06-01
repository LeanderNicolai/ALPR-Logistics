# Automatic License Plate Recognition for Logistics Automation and Optimization
This is project that focused on the recognition and OCR of European and predominantly German License plates for the automation and optimization of logistics management in warehouses of Small to Medium Enterprises. In short, the project is a combination of the retraining of YOLO, a Deep Learning based Object Detection system, in combination with the Tesseract Library after applying my own pre-processing techniques.


## A demonstration
Due to GDPR and Privacy Laws it is obviously not possible to show a recording from a public road to show the algorithms capabilities, therefore a small scene from a German Movie was used for demonstration purposes. 

![ALPR DEMO](https://github.com/LeanderNicolai/ALPR-Logistics/blob/master/DEMO.gif)

## How to use this project

1. Clone this repository
2. Install the requirements by running the following command in your shell while in this repository:

```pip install -r requirements.txt```

3. Download the weight files from [here:](https://drive.google.com/open?id=1s9_MLP9ABkC4xOZ0BPGEAnnlGimya6p3)
4. Create a folder in the folder of this repo named 'ckpt' and put the downloaded weight files in there
4. Change video file source in plate_recog.py to run plate recognition and OCR on your own video source. (Line 31)
5. Specify an output path if you wish to save the video tracking output in plate_recog.py (Line 45)
6. Change the database connections in plate_recog.py if you wish to log the read plates in your database (Line 39)
7. You're ready to go: Run plate_recog.py and you will get a real time view of the plate recognition and OCR!

##How this project was created

###Intro -- Reasoning behind the project
This project was created in order to gain knowledge in the field of computer vision while also creating a solution which could that could provide some form of business value by automating specific processes. Since Logistical Tracking is something that not all companies can afford to do, since it often requires manpower and can be quite mundane (at least to a certain degree). Therefore the idea was to create a logistics tracking system that automatically logs license plates, creating data about the user's business which can then later provide valuable insights.

In order for this solution to work, quite a few interesting hurdles had be overcome, which are described below. 

###Retraining YOLO
1. Shooting my own training footage
2. Annotation of Images
3. Reformatting of Output Files
4. Training the Network
5. The results

###Optical Character Recognition

####Testing Pytesseract

####My Own Pre-Processing Pipeline

###Database Storage
