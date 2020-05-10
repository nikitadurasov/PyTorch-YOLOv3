# coding: utf-8

import os
import json
import pandas as pd

LABELS_PATH = input("Enter labels folder: ")
city_names = sorted(os.listdir(LABELS_PATH))
print('Number of cities:', len(city_names))

data_pd = []

# Count class occurances
for i in range(len(city_names)):
    for each in sorted(os.listdir(LABELS_PATH + city_names[i])):
        file_name = LABELS_PATH + city_names[i] + '/' + each
        with open(file_name) as json_file:
            data = json.load(json_file)
            for obj in data['children']:
                class_label = obj['identity']
                area = (obj['x1'] - obj['x0']) * (obj['y1'] - obj['y0'])

                data_pd.append([class_label, area])

boxes = pd.DataFrame(data=data_pd, columns=["Class", "Box Area"])

print(boxes.groupby("Class").describe())
