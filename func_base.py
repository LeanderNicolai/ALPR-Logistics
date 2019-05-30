from darkflow.net.build import TFNet
import cv2
import pytesseract
import PIL
import numpy as np
from math import sqrt
import re
import datetime
from sqlalchemy import create_engine


def clean_entry(txt):
    txt = txt.replace(' ', '')
    pattern = r'[A-Za-z0-9]+'
    txt = re.findall(pattern, txt)
    txt = ''.join(txt)
    real_plate = 'N'
    if len(txt) >= 6:
        if txt[-3:].isdigit():
            plate_pos = txt
            if txt[:2].isalpha():
                real_plate = txt
                real_plate = re.sub(r'[a-z]', '', real_plate)
                print('MATCHED CRITERIA ', real_plate, '\n\n')
    if len(real_plate) >= 6:
        confirmed_plate = real_plate
    else:
        confirmed_plate = 'N'
    return confirmed_plate


def crop_plate(result, frame):
    if result is not None:
        print('NUM PLATES FOUND IS ', len(result))
    result_dict = result[0]
    label = result_dict['label']
    confidence = result_dict['confidence']
    tl_dict = result_dict['topleft']
    br_dict = result_dict['bottomright']
    x_tl = tl_dict['x']
    y_tl = tl_dict['y']
    x_br = br_dict['x']
    y_br = br_dict['y']
    with_rect = cv2.rectangle(frame, (x_tl, y_tl), (x_br, y_br), (0, 255, 0), 2)
    crop_img = frame[y_tl:y_br, x_tl:x_br]
    if len(result) > 1:
        result_dict = result[1]
        label = result_dict['label']
        confidence2 = result_dict['confidence']
        tl_dict = result_dict['topleft']
        br_dict = result_dict['bottomright']
        x_tl = tl_dict['x']
        y_tl = tl_dict['y']
        x_br = br_dict['x']
        y_br = br_dict['y']
        with_rect = cv2.rectangle(with_rect, (x_tl, y_tl), (x_br, y_br), (255, 255, 0), 2)
    return crop_img, confidence, x_tl, y_tl, x_br, y_br, label, with_rect


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    line_length = []
    coordinates = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            xdif = abs(x1 - x2)
            ydif = abs(y1 - y2)
            length = sqrt(xdif**2 + ydif**2)
            if abs(y1 - y2) > 4:
                line_length.append(length)
                coordinates.append((x1, y1, x2, y2))
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        if len(line_length) > 0:
            m = max(line_length)
            index = [i for i, j in enumerate(line_length) if j == m]
            x1, y1, x2, y2 = coordinates[index[0]]
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            slope = (y1 - y2) / (x1-x2)
            rot_rad = np.arctan(slope)
            rot_deg = rot_rad * (180/np.pi)
        else:
            rot_deg = 0
            line_image = image
        return line_image, rot_deg


def pre_process(img):
    lane_image = np.copy(img)
    gray = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)
    canny = cv2.Canny(gray, 100, 150)
    hough = cv2.HoughLinesP(canny, 2, np.pi/180, 80, np.array([]), minLineLength=30, maxLineGap=5)
    if hough is not None:
        with_lines, rot_deg = display_lines(lane_image, hough)
        combo_image = cv2.addWeighted(lane_image, 0.8, with_lines, 1, 1)
        (h, w) = with_lines.shape[:2]
        center = (w / 2, h / 2)
        scale = 1
        M = cv2.getRotationMatrix2D(center, rot_deg-1, scale)
        rotated = cv2.warpAffine(lane_image, M, (w, h))
        enlarged = cv2.resize(rotated, None, fx=3, fy=3)
    else:
        rotated = lane_image
    return rotated


def read_plate(img):
    config = ("-l eng --oem 1 --psm 7")
    txt = pytesseract.image_to_string(img, config=config)
    return txt


def high_mention(rp):
    high_mention = []
    da_plates = [a for a, b in rp]
    unique_plates = set(da_plates)
    plate_count = [(da_plates.count(plate), plate) for plate in unique_plates]
    for amount, plate in plate_count:
        if amount >= 2:
            high_mention.append(plate)
    string_of_plates = ' '.join(high_mention)
    text_file = open("found_plates.txt", "w")
    text_file.write(string_of_plates)
    text_file.close()
    return high_mention


def full_recognition(video, tfnet, p, rp=[]):
    check, frame = video.read()
    key = cv2.waitKey(1)
    result = tfnet.return_predict(frame)
    crop_img = frame
    with_rect = frame
    text_over = frame
    show = frame
    b = 'N'
    if len(result) >= 1:
        crop_img, confidence, x_tl, y_tl, x_br, y_br, label, show = crop_plate(result, frame)
        if confidence >= 0.6:
            processed = pre_process(crop_img)
            cv2.imshow('pro', processed)
            p = p + 1
            cv2.waitKey(10)
            txt = read_plate(processed)
            if len(txt) >= 5:
                plate = clean_entry(txt)
            else:
                plate = 'N'
            if len(plate) >= 5:
                b = (plate, confidence)
                rp.append(b)
    show = cv2.resize(show, (1280, 720), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (90, 700)
    fontScale = 1
    fontColor = (0, 255, 0)
    lineType = 2
    if len(rp) >= 1:
        show = cv2.putText(show, f'plate found with id: {rp[-1]}',
                           bottomLeftCornerOfText,
                           font,
                           fontScale,
                           fontColor,
                           lineType)
    return show, key, b, p


def send_to_db(plate):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = f"INSERT INTO plates (plate, seenat) VALUES ('{plate}', '{now}');"
    db.execute(sql)
    return (print(f'Entered {plate} into Database'))


def clear_db(db):
    sql = f"DELETE from plates"
    db.execute(sql)
