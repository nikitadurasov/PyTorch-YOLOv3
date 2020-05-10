#!/usr/bin/bash

wget --auth-no-challenge --user=$1 --password=$2 --output-document=ECP_day_img_train.zip http://eurocity-dataset.tudelft.nl//eval/downloadFiles/downloadFile/detection?file=ecpdata%2FECP_day_img_train.zip 
wget --auth-no-challenge --user=$1 --password=$2 --output-document=ECP_day_labels_train.zip http://eurocity-dataset.tudelft.nl//eval/downloadFiles/downloadFile/detection?file=ecpdata%2FECP_day_labels_train.zip 

wget --auth-no-challenge --user=$1 --password=$2 --output-document=ECP_night_img_train.zip http://eurocity-dataset.tudelft.nl//eval/downloadFiles/downloadFile/detection?file=ecpdata%2FECP_night_img_train.zip 
wget --auth-no-challenge --user=$1 --password=$2 --output-document=ECP_night_labels_train.zip http://eurocity-dataset.tudelft.nl//eval/downloadFiles/downloadFile/detection?file=ecpdata%2FECP_night_labels_train.zip 

unzip "*.zip"