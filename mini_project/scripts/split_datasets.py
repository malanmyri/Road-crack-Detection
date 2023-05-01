import random
import glob
import os
import shutil
import argparse


parser = argparse.ArgumentParser(description='Submission')

parser.add_argument('images_path', type=str, help='')
parser.add_argument('labels_path', type=str, help='')

args = parser.parse_args()
label_dir = args.labels_path
image_dir = args.images_path

def copyfiles(fil, root_dir):
    basename = os.path.basename(fil)
    filename = os.path.splitext(basename)[0]

    # copy image
    src = fil
    dest = os.path.join(root_dir, image_dir, f"{filename}.jpg")
    shutil.copyfile(src, dest)

    # copy annotations
    src = os.path.join(label_dir, f"{filename}.txt")
    dest = os.path.join(root_dir, label_dir, f"{filename}.txt")
    if os.path.exists(src):
        shutil.copyfile(src, dest)


lower_limit = 0
files = glob.glob(os.path.join(image_dir, '*.jpg'))

random.shuffle(files)

folders = {"train": 0.8, "valid": 0.2, "test": 0.0}
check_sum = sum([folders[x] for x in folders])

assert check_sum == 1.0, "Split proportion is not equal to 1.0"

for folder in folders:
    os.mkdir(folder)
    temp_label_dir = os.path.join(folder, label_dir)
    os.mkdir(temp_label_dir)
    temp_image_dir = os.path.join(folder, image_dir)
    os.mkdir(temp_image_dir)

    limit = round(len(files) * folders[folder])
    print(f"count will continue up to {len(files)- lower_limit}")
    count = 0
    for fil in files[lower_limit:lower_limit + limit]:
        count += 1
        print(count)
        copyfiles(fil, folder)
    lower_limit = lower_limit + limit