#!/usr/bin/bash

python preprocess_ECP_dataset.py.

mv images/* data/custom/images/
mv labels/* data/custom/labels/

rm train.txt 
rm valid.txt 

rm -r images
rm -r labels