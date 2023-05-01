# This script was used to transform Sahi pickles coco predictions into yolov5.


import os
import pickle
from typing import List, Tuple
import argparse

parser = argparse.ArgumentParser(description='pickled coco to yolov5')
parser.add_argument('coco_annotations_path', type=str, help='')
parser.add_argument('yolov5_output_dir', type=str, help='')
parser.add_argument('images_dir', type=str, help='')



args = parser.parse_args()

coco_annotations_path = args.coco_annotations_path
yolov5_output_dir = args.yolov5_output_dir
images_dir = args.images_dir


class_map = {'D00': 0, 'D10': 1, 'D20': 2, "D40":3}
def convert_coco_to_yolov5(coco_annotations_path: str, yolov5_output_dir: str, images_dir: str):
    # Load categories from COCO annotations file
    # Loop over each file in the COCO annotations directory and convert to YOLOv5 format
    for file_name in os.listdir(coco_annotations_path):
        if not file_name.endswith('.pickle'):
            continue
        file_path = os.path.join(coco_annotations_path, file_name)
        # Load COCO annotations from pickle file
        with open(file_path, 'rb') as f:
            coco_annotations = pickle.load(f)

        # Loop over each annotation and convert to YOLOv5 format
        for ann in coco_annotations:
            bbox = ann.bbox
            category_id = str(class_map[ann.category.name])
            score = ann.score

            # Get image width and height from corresponding image file
            name = file_name[:-7]
            img_path = os.path.join(images_dir, name + ".jpg")
            img_w, img_h = get_image_size(img_path)

            # Normalize bbox coordinates
            
            bbox_norm = xml_to_yolo_bbox(bbox, img_w, img_h)

            # Write YOLOv5 annotation to file
            output_file_path = os.path.join(yolov5_output_dir, name + ".txt")
            with open(output_file_path, 'a') as f:
                f.write(f"{category_id} {bbox_norm[0]:.6f} {bbox_norm[1]:.6f} {bbox_norm[2]:.6f} {bbox_norm[3]:.6f} {score.value:.6f}\n")


def get_image_size(image_path: str) -> Tuple[int, int]:
    from PIL import Image
    with Image.open(image_path) as img:
        return img.size

def xml_to_yolo_bbox(bbox, w, h):
    # xmin, ymin, xmax, ymax
    x_center = ((bbox.maxx + bbox.minx) / 2) / w
    y_center = ((bbox.maxy + bbox.miny) / 2) / h
    width = (bbox.maxx - bbox.minx) / w
    height = (bbox.maxy - bbox.miny) / h
    return [x_center, y_center, width, height]




convert_coco_to_yolov5(coco_annotations_path, yolov5_output_dir, images_dir)