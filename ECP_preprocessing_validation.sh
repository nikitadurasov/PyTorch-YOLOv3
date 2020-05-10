#!/usr/bin/bash

python preprocess_ECP_dataset_validation.py.

mv images/* data/custom/validation_images/
mv labels/* data/custom/validation_labels/

rm full_valid.txt

rm -r images
rm -r labels