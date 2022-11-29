rm -f ./Scraping/Data/labelTitle.db
rm -r *.csv

python Scraping/makeTrainFile.py
python Scraping/makeTrainFile.py

python Training/generateCombinedCSV.py
python Training/generateSeperateCSV.py