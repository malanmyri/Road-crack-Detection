#Balancing Backgrounds vs labelled images
import os
import argparse
import random
import numpy as np
import shutil
import shutil


parser = argparse.ArgumentParser(description='Balancing dataset')
parser.add_argument('images_path', type=str, help='path to folder containing images to crop')
parser.add_argument('labels_path', type=str, help='path to folder containing labels to crop')
parser.add_argument('balanced_images_path', type=str, help='path to empty folder for cropped images.')
parser.add_argument('balanced_labels_path', type=str, help='path to empty folder for cropped images.')
parser.add_argument("percentage", type=float, help='Percentage of training data which is background.')

#python balancing.py cropim/ croplab/ balanced_images/ balanced_labels/ 0.1

args = parser.parse_args()


images_path = args.images_path
labels_path = args.labels_path
balanced_images_path = args.balanced_images_path
balanced_labels_path = args.balanced_labels_path
percentage = args.percentage

labels = os.listdir(labels_path)
images = os.listdir(images_path)

print(f"Number of labels: {len(labels)}")
print(f"Number of images: {len(images)}")

#All the background images
background = []
for image in images: 
    name = image[:-4]
    label_name = name + ".txt"
    if label_name not in labels: 
        background.append(image)

print(f"Number of backgrounds: {len(background)}")

#Backgrounds to include in the training set
backgrounds_included = []

a = int(len(labels)/0.9 * percentage)
choose_from = np.arange(0,a, 1)       
random.shuffle(choose_from)
for i in choose_from[:a]:     
    backgrounds_included.append(background[i])


images_to_include = []

for label in labels: 
    name = label[:-4]
    new_name = name + ".jpg"
    images_to_include.append(new_name)

for name in backgrounds_included:
    images_to_include.append(name)


for image in images_to_include:
    shutil.copy(images_path + image, balanced_images_path + image)

for label in labels:
    shutil.copy(labels_path + label, balanced_labels_path + label)


print(f"Number of balanced images: {len(os.listdir(balanced_images_path))}")

