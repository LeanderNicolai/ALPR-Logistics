from darkflow.net.build import TFNet
import cv2
import pytesseract
import os
import PIL
import numpy as np
from math import sqrt
import re
import datetime
from sqlalchemy import create_engine
from func_base import clean_entry, crop_plate, display_lines, pre_process, clear_db
from func_base import read_plate, high_mention, full_recognition, send_to_db

use_database = input('Would you like to save the plates to a database? Answer with Y or N \n\n')
use_database.upper()


cwd = os.getcwd()

# Load model options with checkpoint
options = {"model": "cfg/tiny_own.cfg",
           "load": 28250,
           "threshold": 0.03,
           "gpu": 0.8}
tfnet = TFNet(options)


rp = []

# Specifiy video Path
video = cv2.VideoCapture('LI.mp4')
plate_list = []
i = 0
p = 0


# Database Connection
if use_database == 'Y':
    conns = f'postgres://localhost/numberplates'
    db = create_engine(conns, encoding='latin1', echo=False)
    clear_db(db)
realplates = []

# Output video location
out = cv2.VideoWriter('Output.avi', cv2.VideoWriter_fourcc(
    'M', 'J', 'P', 'G'), 30, (1280, 720))


# Recognition loop per individual frame
while(video.isOpened()):
    show, key, plate, p = full_recognition(video, tfnet, p)
    if len(plate) > 1:
        realplates.append(plate)
    if use_database == 'Y':
        if realplates is not None:
            if (len(realplates) % 8) == 0:
                queries = high_mention(realplates)
                if queries is not None:
                    for plate in queries:
                        send_to_db(plate)
            realplates = []
    out.write(show)
    cv2.imshow('result', show)
    if key == ord('q'):
        high_mention(rp)
        break

video.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows()
