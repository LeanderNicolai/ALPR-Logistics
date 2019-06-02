'''
This overly extensive code was written by Nicolai van der Laan in order to fix
his own problem of having 1006 annotations in the wrong format. I hope this will
fix your problems in the same way it fixed mine.
'''

import glob
import os


def zero_xml(filenumber, imagepath):
    string = f'''<annotation verified="yes">
        <folder>Annotation</folder>
        <filename>{filenumber}.jpg</filename>
        <path>{imagepath}{filenumber}.jpg</path>
        <source>
            <database>Unknown</database>
        </source>
        <size>
            <width>950</width>
            <height>534</height>
            <depth>3</depth>
        </size>
        <segmented>0</segmented>

    </annotation>'''
    return string


def single_xml(filenumber, imagepath, xmin, xmax, ymin, ymax):
    string = f'''<annotation verified="yes">
        <folder>Annotation</folder>
        <filename>{filenumber}.jpg</filename>
        <path>{imagepath}{filenumber}.jpg</path>
        <source>
            <database>Unknown</database>
        </source>
        <size>
            <width>950</width>
            <height>534</height>
            <depth>3</depth>
        </size>
        <segmented>0</segmented>
        <object>
        <name>PLATE</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>{xmin}</xmin>
            <ymin>{ymin}</ymin>
            <xmax>{xmax}</xmax>
            <ymax>{ymax}</ymax>
        </bndbox>
    </object>
    </annotation>'''
    return string


def double_xml(filenumber, imagepath, xmin_1, ymin_1, xmax_1, ymax_1, xmin_2, ymin_2, xmax_2, ymax_2):
    string = f'''<annotation verified="yes">
        <folder>Annotation</folder>
        <filename>{filenumber}.jpg</filename>
        <path>{imagepath}{filenumber}.jpg</path>
        <source>
            <database>Unknown</database>
        </source>
        <size>
            <width>950</width>
            <height>534</height>
            <depth>3</depth>
        </size>
        <segmented>0</segmented>
        <object>
        <name>PLATE</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>{xmin_2}</xmin>
            <ymin>{ymin_2}</ymin>
            <xmax>{xmax_2}</xmax>
            <ymax>{ymax_2}</ymax>
        </bndbox>
    </object><object>
        <name>PLATE</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>{xmin_1}</xmin>
            <ymin>{ymin_1}</ymin>
            <xmax>{xmax_1}</xmax>
            <ymax>{ymax_1}</ymax>
        </bndbox>
    </object>
    </annotation>'''
    return string


cwd = os.getcwd()

## Location of the .txt files to be converted
txt_files = glob.glob(cwd + '/bbox_labels/*.txt')

## Location of the images that belong to the .txt labels
## IMPORTANT: THESE LOCATIONS MUST BE FROM WHERE THE YOLO NETWORK WILL BE TRAINED
## SO: First put all the images in place from where you will train the network with its annotations, then do the conversion.
imagepath = cwd + '/001/'

for filename in txt_files:
    with open(filename, 'r') as file:
        xml_name = filename[:-3] + 'xml'
        filenumber = filename[-9:-4]
        data = file.read()
        data = data.replace('\n', ' ')
        data = data.strip('\n')
        coordinates = data.split(' ')
        if data[0] == '0':
            xml_string = zero_xml(filenumber, imagepath)
            print(xml_string)
            xml_filename = f'{filenumber}.xml'
            xml_file = open('xml_labels/' + xml_filename, 'w')
            xml_file.write(xml_string)
            xml_file.close()
            continue
        if data[0] == '1':
            xmin_1 = coordinates[1]
            ymin_1 = coordinates[2]
            xmax_1 = coordinates[3]
            ymax_1 = coordinates[4]
            xml_string = single_xml(filenumber, imagepath, xmin_1, xmax_1, ymin_1, ymax_1)
            print(xml_string)
            xml_filename = f'{filenumber}.xml'
            xml_file = open('xml_labels/' + xml_filename, 'w')
            xml_file.write(xml_string)
            xml_file.close()
        if data[0] == '2':
            xmin_1 = coordinates[1]
            ymin_1 = coordinates[2]
            xmax_1 = coordinates[3]
            ymax_1 = coordinates[4]
            xmin_2 = coordinates[5]
            ymin_2 = coordinates[6]
            xmax_2 = coordinates[7]
            ymax_2 = coordinates[8]
            xml_string = double_xml(filenumber, imagepath, xmin_1, ymin_1,
                                    xmax_1, ymax_1, xmin_2, ymin_2, xmax_2, ymax_2)
            print(xml_string)
            xml_filename = f'{filenumber}.xml'
            xml_file = open('xml_labels/' + xml_filename, 'w')
            xml_file.write(xml_string)
            xml_file.close()
