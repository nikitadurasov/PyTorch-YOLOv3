import shutil, os
from skimage.io import imread, imsave
from shutil import copyfile
import json

DAY_DATA_PATH = 'ECP/day/img/train/'
NIGHT_DATA_PATH = 'ECP/night/img/train/'

DAY_LABELS_PATH = 'ECP/day/labels/train/'
NIGHT_LABELS_PATH = 'ECP/night/labels/train/'

day_city_names = sorted(os.listdir(DAY_DATA_PATH))
night_city_names = sorted(os.listdir(NIGHT_DATA_PATH))

print('Number of cities in DAY:',len(day_city_names))
print('Number of cities in NIGHT:',len(night_city_names))

posible_classes = ["pedestrian", 
                   "rider", 
                   "person-group-far-away", 
                   "rider+vehicle-group-far-away", 
                   "bicycle-group", 
                   "buggy-group", 
                   "motorbike-group", 
                   "scooter-group", 
                   "tricycle-group", 
                   "wheelchair-group",
                   "bicycle", 
                   "buggy", 
                   "motorbike", 
                   "scooter", 
                   "tricycle", 
                   "wheelchair"]

SAVE_DATA_PATH = 'images/'
SAVE_LABELS_PATH = 'labels/'

######## creating temp directories for data ########
if not os.path.exists(SAVE_DATA_PATH) and not os.path.exists(SAVE_LABELS_PATH):
    os.makedirs(SAVE_DATA_PATH)
    os.makedirs(SAVE_LABELS_PATH)
    
######## creating original directories for data in repo ########
if not os.path.exists("data/custom/images/") and not os.path.exists("data/custom/labels/"):
    os.makedirs("data/custom/images/")
    os.makedirs("data/custom/labels/")
    
######## copy data to images/ ########
for i in range(len(day_city_names)):
    for each in sorted(os.listdir(DAY_DATA_PATH + day_city_names[i])):
        src_path = os.path.join(DAY_DATA_PATH, day_city_names[i], each)
        dest_path = os.path.join(SAVE_DATA_PATH, "day_" + each)
        copyfile(src_path, dest_path)
                
######## copy data to images/ ########
for i in range(len(night_city_names)):
    for each in sorted(os.listdir(NIGHT_DATA_PATH + night_city_names[i])):
        src_path = os.path.join(NIGHT_DATA_PATH, night_city_names[i], each)
        dest_path = os.path.join(SAVE_DATA_PATH, "night_" + each)
        copyfile(src_path, dest_path)
        
######## write to train.txt and valid.txt ########
f1 = open("train.txt","w+")
f2 = open("valid.txt","w+")

for i in range(len(day_city_names)):
    for each in sorted(os.listdir(DAY_DATA_PATH + day_city_names[i])):
        name = os.path.join('data/custom/images/', 'day_' + each)
        if i<=28:
            f1.write(name + '\n')
        else:
            f2.write(name + '\n')
            
f1.close()
f2.close()

######## write to train.txt and valid.txt ########
f1 = open("train.txt","w+")
f2 = open("valid.txt","w+")

for i in range(len(night_city_names)):
    for each in sorted(os.listdir(NIGHT_DATA_PATH + night_city_names[i])):
        name = os.path.join('data/custom/images/', 'night_' + each)
        if i<=5:
            f1.write(name + '\n')
        else:
            f2.write(name + '\n')
            
f1.close()
f2.close()

######## writing class.names ########
f = open("classes.names","w+")

for each in posible_classes:
    f.write(each + '\n')

f.close()

######## make ECP labels compatible with repo format ########
for i in range(len(day_city_names)):
    for each in sorted(os.listdir(DAY_LABELS_PATH + day_city_names[i])):
        file_name = os.path.join(DAY_LABELS_PATH, day_city_names[i], each)
        with open(file_name) as json_file:
            f = open(SAVE_LABELS_PATH + "day_" + each.split(".")[0] + ".txt","w+")
            data = json.load(json_file)
            
            image_width = data['imagewidth']
            image_height = data['imageheight']
            
            for obj in data['children']:
                label_idx = posible_classes.index(obj['identity'])
                x_center = (obj['x0'] + obj['x1']) / 2 / image_width
                width = (obj['x1'] - obj['x0']) / image_width
                y_center = (obj['y0'] + obj['y1']) / 2 / image_height
                height = (obj['y1'] - obj['y0']) / image_height
            
                f.write(f"{label_idx} {x_center} {y_center} {width} {height}\n")
            f.close()
            
######## make ECP labels compatible with repo format ########
for i in range(len(night_city_names)):
    for each in sorted(os.listdir(NIGHT_LABELS_PATH + night_city_names[i])):
        file_name = os.path.join(NIGHT_LABELS_PATH, night_city_names[i], each)
        with open(file_name) as json_file:
            f = open(SAVE_LABELS_PATH + "night_" + each.split(".")[0] + ".txt","w+")
            data = json.load(json_file)
            
            image_width = data['imagewidth']
            image_height = data['imageheight'] 
                
            for obj in data['children']:
                label_idx = posible_classes.index(obj['identity'])
                x_center = (obj['x0'] + obj['x1']) / 2 / image_width
                width = (obj['x1'] - obj['x0']) / image_width
                y_center = (obj['y0'] + obj['y1']) / 2 / image_height
                height = (obj['y1'] - obj['y0']) / image_height
            
                f.write(f"{label_idx} {x_center} {y_center} {width} {height}\n")
            f.close()