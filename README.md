# Automatic License Plate Recognition for Logistics Automation and Optimization
This is project that focused on the recognition and OCR of European and predominantly German License plates for the automation and optimization of logistics management in warehouses of Small to Medium Enterprises. In short, the project is a combination of the retraining of YOLO, a Deep Learning based Object Detection system, in combination with the Tesseract Library after applying my own pre-processing techniques.


## A demonstration
Due to GDPR and Privacy Laws it is obviously not possible to show a recording from a public road to show the algorithms capabilities, therefore a small scene from a German Movie was used for demonstration purposes. 

![ALPR DEMO](https://github.com/LeanderNicolai/ALPR-Logistics/blob/master/DEMO.gif)

## How to use this project

1. Clone this repository
2. Install all dependencies
3. Change video file source in plate_recog.py
4. Specify an output path if you wish to save the video tracking output
5. Change the database connections in func_base.py if you wish to log the read plated in your database
6. You're ready to go!

