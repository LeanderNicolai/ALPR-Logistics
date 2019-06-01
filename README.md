# Automatic License Plate Recognition for Logistics Automation and Optimization
This is project that focused on the recognition and OCR of European and predominantly German License plates for the automation and optimization of logistics management in warehouses of Small to Medium Enterprises. In short, the project is a combination of the retraining of YOLO, a Deep Learning based Object Detection system, in combination with the Tesseract Library after applying my own pre-processing techniques.


## A demonstration
Due to GDPR and Privacy Laws it is obviously not possible to show a recording from a public road to show the algorithms capabilities, therefore a small scene from a German Movie was used for demonstration purposes. 

![ALPR DEMO](https://github.com/LeanderNicolai/ALPR-Logistics/blob/master/DEMO.gif)

## How to use this project

1. Clone this repository
2. Install the requirements by running the following command in your shell, with a (conda) virtual environment if you prefer.         ```pip install -r requirements.txt```
3. Download the weight files from [here:](https://drive.google.com/open?id=1s9_MLP9ABkC4xOZ0BPGEAnnlGimya6p3)
4. Create a folder in the folder of this repo named 'ckpt' and put the downloaded weight files in there
4. Change video file source in plate_recog.py to run plate recognition and OCR on your own video source. (Line 31)
5. Specify an output path if you wish to save the video tracking output in plate_recog.py (Line 45)
6. Change the database connections in plate_recog.py if you wish to log the read plated in your database (Line 39)
7. You're ready to go: Run plate_recog.py and you will get a real time view of the plate recognition and OCR!

