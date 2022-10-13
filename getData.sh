rm -f ./Scraping/Data/labelTitle.db
rm -f train.csv
rm -f test.csv

python Scraping/makeTrainFile.py
python Scraping/makeTrainFile.py

python Training/generateCSV.py