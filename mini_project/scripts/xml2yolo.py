import xml.etree.ElementTree as ET
import glob
import os
import json
import argparse

parser = argparse.ArgumentParser(description='Balancing dataset')

parser.add_argument('images_path', type=str, help='')
parser.add_argument('xmls_path', type=str, help='')
parser.add_argument('labels_path', type=str, help='')


args = parser.parse_args()
#python xml2yolo.py images_not_cropped/ annotations/xmls/ labels_final/

images_path = args.images_path
labels_path = args.labels_path
xmls_path = args.xmls_path


def xml_to_yolo_bbox(bbox, w, h):
    # xmin, ymin, xmax, ymax
    x_center = ((bbox[2] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[1]) / 2) / h
    width = (bbox[2] - bbox[0]) / w
    height = (bbox[3] - bbox[1]) / h
    return [x_center, y_center, width, height]


def yolo_to_xml_bbox(bbox, w, h):
    # x_center, y_center width heigth
    w_half_len = (bbox[2] * w) / 2
    h_half_len = (bbox[3] * h) / 2
    xmin = int((bbox[0] * w) - w_half_len)
    ymin = int((bbox[1] * h) - h_half_len)
    xmax = int((bbox[0] * w) + w_half_len)
    ymax = int((bbox[1] * h) + h_half_len)
    return [xmin, ymin, xmax, ymax]


classes = ["D00", "D10", "D20", "D40"]

# create the labels folder (output directory)
os.mkdir(labels_path)

# identify all the xml files in the annotations folder (input directory)
files = glob.glob(os.path.join(xmls_path, '*.xml'))
# loop through each 
count = 0
for fil in files:
    print(f"Percentage done is: {count/len(files)}")
    count +=1
    basename = os.path.basename(fil)
    filename = os.path.splitext(basename)[0]
    # check if the label contains the corresponding image file
    if not os.path.exists(os.path.join(images_path, f"{filename}.jpg")):
        print(f"{filename} image does not exist!")
        continue

    result = []

    # parse the content of the xml file
    tree = ET.parse(fil)
    root = tree.getroot()
    width = int(root.find("size").find("width").text)
    height = int(root.find("size").find("height").text)

    for obj in root.findall('object'):
        label = obj.find("name").text
        # check for new classes and append to list
        if label in classes:
            index = classes.index(label)
            pil_bbox = [int(float(x.text)) for x in obj.find("bndbox")]
            yolo_bbox = xml_to_yolo_bbox(pil_bbox, width, height)
            # convert data to string
            bbox_string = " ".join([str(x) for x in yolo_bbox])
            result.append(f"{index} {bbox_string}")

    if result:
        # generate a YOLO format text file for each xml file
        with open(os.path.join(labels_path, f"{filename}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(result))

