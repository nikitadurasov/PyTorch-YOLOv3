#!/usr/bin/bash

python preprocess_ECP_dataset_validation.py.

mv images/* data/custom/validation_images/
mv labels/* data/custom/validation_labels/

mv full_valid.txt data/custom/

rm -r images
rm -r labels