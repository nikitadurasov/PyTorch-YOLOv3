mv images/* data/custom/images/
mv labels/* data/custom/labels/

mv train.txt data/custom/
mv valid.txt data/custom/
mv classes.names data/custom/

cd config/
bash create_custom_model.sh 16
cd ..

rm -r images
rm -r labels