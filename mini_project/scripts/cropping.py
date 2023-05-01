
from PIL import Image, ImageDraw
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser(description='Crop images.')
parser.add_argument('px_min', type=float, help='minimum x-coordinate ratio')
parser.add_argument('px_max', type=float, help='maximum x-coordinate ratio')
parser.add_argument('py_min', type=float, help='minimum y-coordinate ratio')
parser.add_argument('py_max', type=float, help='maximum y-coordinate ratio')
parser.add_argument('images_path', type=str, help='path to folder containing images to crop')
parser.add_argument('labels_path', type=str, help='path to folder containing labels to crop')
parser.add_argument('cropped_images_path', type=str, help='path to empty folder for cropped images')
parser.add_argument('cropped_labels_path', type=str, help='path to empty folder for cropped labels')
parser.add_argument('description', type=str, help='extra term added to the cropped images to separate them from the original name.')



args = parser.parse_args()

px_min = args.px_min
px_max = args.px_max
py_min = args.py_min
py_max = args.py_max
images_path = args.images_path
labels_path = args.labels_path
cropped_images_path = args.cropped_images_path
cropped_labels_path = args.cropped_labels_path
description = args.description


def yolo_to_xml_bbox(bbox, w, h):
    # x_center, y_center width heigth
    w_half_len = (bbox[2] * w) / 2
    h_half_len = (bbox[3] * h) / 2
    xmin = int((bbox[0] * w) - w_half_len)
    ymin = int((bbox[1] * h) - h_half_len)
    xmax = int((bbox[0] * w) + w_half_len)
    ymax = int((bbox[1] * h) + h_half_len)
    return [xmin, ymin, xmax, ymax]

def xml_to_yolo_bbox(bbox, w, h):
    # xmin, ymin, xmax, ymax
    x_center = ((bbox[2] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[1]) / 2) / h
    width = (bbox[2] - bbox[0]) / w
    height = (bbox[3] - bbox[1]) / h
    return [x_center, y_center, width, height]




def crop_img( filename_label, new_label_folder,  left, right, top, bottom, width, height):
    label_path = labels_path + filename_label
    with open( label_path, 'r', encoding='utf8') as f:
        
        result = []
        for line in f:
            data = line.strip().split(' ')
            bbox = [float(x) for x in data[1:]]
            
            [xmin, ymin, xmax, ymax] = yolo_to_xml_bbox(bbox, width, height)
            if xmin < right and xmax > left: 
                if ymin < bottom and ymax > top: 
                    x_min = max( left,  xmin)
                    x_max = min( right,xmax)
                    y_min = max( top,  ymin )
                    y_max = min( bottom, ymax)

                    bbox = [x_min, y_min, x_max, y_max]

                    #Need to modify bbox so that the pixels are resised
                    new_width = abs(right-left)
                    new_height = abs(top-bottom)

                    bbox = [x_min -left,y_min - top, x_max -left , y_max-top]
                    yolo_bbox = xml_to_yolo_bbox(bbox, new_width, new_height)
                    # convert data to string
                    bbox_string = " ".join([str(x) for x in yolo_bbox])

                    result.append(f"{int(data[0])} {bbox_string}")
        if result: 
            label_path = new_label_folder + name + description + ".txt"
            with open(label_path, "x", encoding="utf-8") as f:
                f.write("\n".join(result))


count = 0
files = os.listdir(images_path)
for file in files:
    count+= 1
    print(f"Percentage done: {count/len(files)}")

    try:

        img = Image.open(images_path + file)
        width, height = img.size


        left = width*px_min
        right = px_max *width
        bottom= py_max * height
        top=  py_min* height

        name = file[:-4]

        img = img.crop((left, top, right, bottom))
        img.save(cropped_images_path + name + description + ".jpg")

        
        filename_label =  name + ".txt"
        crop_img(filename_label, cropped_labels_path,  left, right, top, bottom, width, height)
    
    except:
        None

# python cropping.py 0 0.6 0.5 1 images_not_cropped/ labels_not_cropped/  cropim/ croplab/ lower_left