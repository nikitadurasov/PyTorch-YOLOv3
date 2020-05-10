mv images/* data/custom/images/
mv labels/* data/custom/labels/

mv train.txt data/custom/
mv valid.txt data/custom/
mv classes.names data/custom/

rm -r images
rm -r labels