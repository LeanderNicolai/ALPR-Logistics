# Nico-ALPR: Automatic License Plate Recognition for Logistics Management
This is a project that focused on the recognition and OCR of license plates for the automation and optimization of logistics management in warehouses of small to medium enterprises. Logistical Tracking is something that not all companies can afford to do, since it often requires manpower and can be quite mundane (at least to a certain degree). Therefore the idea was to create a logistics tracking system that automatically logs license plates, creating data about the user's business which can then later provide valuable insights.

The project is a combination of **object recognition** with **deep learning**, **image processing**, **optical character recognition** and **database logging**.

#### **As a disclaimer: I only had a single week to spend on this project, and that is all the time that has been spent on this project so far. It might be improved in the future.**

## A demonstration
Due to GDPR and German Privacy Laws it is not possible to show a recording from a public road to show the algorithm's actual performance, therefore a small scene from a German Movie was used for demonstration purposes.

![ALPR DEMO](https://github.com/LeanderNicolai/ALPR-Logistics/blob/master/DEMO.gif)

## How to use this project to read your own numberplates and automate your logistics:

1. **Clone** this repository
2. Install the requirements by running the following command in your shell while in this repository:

```pip install -r requirements.txt```

3. Download the weight files from [here:](https://drive.google.com/open?id=1s9_MLP9ABkC4xOZ0BPGEAnnlGimya6p3)
4. Create a folder in the folder of this repo named '**ckpt**' and put the downloaded weight files in there
4. Change video file source in **plate_recog.py** to run plate recognition and OCR on your own video source. (Line 31)
5. Specify an output path if you wish to save the video tracking output in plate_recog.py (Line 45)
6. Change the database connections in **plate_recog.py** if you wish to log the read plates in your database (Line 39)
7. You're ready to go: Run **plate_recog.py** and you will get a real time view of the plate recognition and OCR!

## How this project was created

### Intro -- Reasoning behind the project
 This project was created in order to gain knowledge in the field of computer vision while also creating a solution could that could provide some form of business value by automating specific processes. Logistical Tracking is something that not all companies can afford to do, since it often requires manpower and can be quite mundane (at least to a certain degree). Therefore the idea was to create a logistics tracking system that automatically logs license plates, creating data about the user's business which can then later provide valuable insights.

#### **Once again as a disclaimer: I only had a week to spend on this project, and that is all the time that has been spent on this project so far. It might be improved in the future.**

In order for this solution to work, quite a few interesting hurdles had be overcome, which are described below.

### Part 1: Retraining YOLO
##### 1. Shooting my own training footage
For this project I had to shoot my own training footage by the side of a public road, which then had to be annotated in order to train the network.
##### 2. Annotation of Images
I used the BBox Label Tool, which runs on Python 2.0, in order to annotate the images. Over a thousand images were annotated. That looked something like this.

<img align="center" width="550" src="https://github.com/LeanderNicolai/ALPR-Logistics/blob/master/imgs/P3.jpg">

##### 3. Reformatting of Output Files
Since the output of the BBox Label tool did not output the coordinates of the bounding boxes in a Pascal VOC format, which is in XML, I wrote a Python script that makes the conversion that is seen in the image below (Conversion is from **right to left**). That script can be found [here](https://github.com/LeanderNicolai/ALPR-Logistics/blob/master/PascalReformat.py).

<img align="center" width="600" src="https://github.com/LeanderNicolai/ALPR-Logistics/blob/master/imgs/P5.jpg">

##### 4. Training the Network
Once the images the network had to be trained. The total training took about 48 hours.

<img align="center" width="400" src="https://github.com/LeanderNicolai/ALPR-Logistics/blob/master/imgs/P6.jpg">     <img align="center" width="400"  src="https://github.com/LeanderNicolai/ALPR-Logistics/blob/master/imgs/P7.jpg">

##### 5. The results
The results after 48 hours were quite good, with adequate tracking that allowed for continuation witht the OCR part of the project.

### Part 2: Optical Character Recognition
For the optical character recognition Tesseract was used, which is an Open Source OCR Libary made by Google.

#### My Own Pre-Processing Pipeline
The results of using Tessearct directly on the bounding boxes drawn by the retrained network gave unsatisfactory results. Therefore some preprocessing and transformation had to be done. With use of some simple contrast changes, and a hough transform in order to straighten out the image, the results were greatly improved.

<img align="center" width="200" src="https://github.com/LeanderNicolai/ALPR-Logistics/blob/master/imgs/P1.jpg">     <img align="center" width="200"  src="https://github.com/LeanderNicolai/ALPR-Logistics/blob/master/imgs/P2.jpg">


### Database Storage
The project makes use of simple a SQL Alchemy Engine in order to send the read plates into the database. Since the OCR is not perfect yet, some filtering techniques were used in order to optimize correct storage.


## Future Improvements
Since this project was developed in merely a week, a lot of improvements could be made to this project. The main improvement would be to add more data into the YOLO Network, in order to improve the robustness of the bounding boxes. Secondly more experimentation could be done concerning the pre-processing in order to improve the OCR. Lastly, an important feature that could be added is an extensive dashboarding tool that creates effective overviews and insights of the user's logistics.
