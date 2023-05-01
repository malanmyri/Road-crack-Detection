import os
import argparse


parser = argparse.ArgumentParser(description='Submission')

parser.add_argument('images_path', type=str, help='')
parser.add_argument('labels_path', type=str, help='')


args = parser.parse_args()
images = args.images_path
labels = args.labels_path


path =  images
list_of_images = []
for file in os.listdir(path):
    list_of_images.append(str(file)[:-4])

path =  labels
list_of_predictions = []
for file in os.listdir(path):
    list_of_predictions.append(str(file)[:-4])

missing = []
for file in list_of_images: 
    if file not in list_of_predictions: 
        missing.append(file)

for file in missing:
    path = labels
    txt = file + ".txt"
    f = open(path + txt, "w")

    