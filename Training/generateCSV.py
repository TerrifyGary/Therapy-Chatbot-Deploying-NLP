import csv
from re import X
import sqlite3
import random as rn
import pandas as pd

def createData(name,header,data):
    with open(f'{name}.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        
        title, label = data
        length = len(title)

        for x in range(length):
            temp = [title[x],label[x]]
            # print(temp)
            writer.writerow(temp)

def getData():
    
    trainTitle, trainLabel, testTitle, testLabel = [],[],[],[]

    # ------ 把db讀取進來 ------ #
    cnx = sqlite3.connect('./Scraping/Data/labelTitle.db')
    df = pd.read_sql_query("SELECT * FROM labelTitle", cnx)
    length = df.shape[0]
    
    print("Titles Count = "+str(length))
    
    # ------ 將Titel, Label資料分級 ------ #

    tenthLength = length//10
    oneTitle  = []
    twoTitle  = []
    threeTitle  = []
    fourTitle  = []
    fiveTitle  = []
    sixTitle  = []
    sevenTitle  = []
    eightTitle  = []
    nineTitle  = []
    tenTitle  = []

    popRank = df.sort_values('poprank',ascending=True)
    for x in range(length):
        if x <= tenthLength:
            oneTitle.append(popRank['title'][x])
            
        elif x > tenthLength and x <= 2*tenthLength:
            twoTitle.append(popRank['title'][x])

        elif x > 2*tenthLength and x <= 3*tenthLength:
            threeTitle.append(popRank['title'][x])

        elif x > 3*tenthLength and x <= 4*tenthLength:
            fourTitle.append(popRank['title'][x])

        elif x > 4*tenthLength and x <= 5*tenthLength:
            fiveTitle.append(popRank['title'][x])

        elif x > 5*tenthLength and x <= 6*tenthLength:
            sixTitle.append(popRank['title'][x])

        elif x > 6*tenthLength and x <= 7*tenthLength:
            sevenTitle.append(popRank['title'][x])

        elif x > 7*tenthLength and x <= 8*tenthLength:
            eightTitle.append(popRank['title'][x])

        elif x > 8*tenthLength and x <= 9*tenthLength:
            nineTitle.append(popRank['title'][x])

        elif x > 9*tenthLength:
            tenTitle.append(popRank['title'][x])

    checkList = []
    checkTimes = 5
    isShuffled = True
    for i in range(checkTimes):
        checkList.append(oneTitle[-i])


    allTitles = [oneTitle,twoTitle,threeTitle,fourTitle,fiveTitle,sixTitle,sevenTitle,eightTitle,nineTitle,tenTitle]

    # ------ 標上label ------ #

    allLabels = [ 
        ['1']*len(allTitles[0]),
        ['2']*len(allTitles[1]),
        ['3']*len(allTitles[2]),
        ['4']*len(allTitles[3]),
        ['5']*len(allTitles[4]),
        ['6']*len(allTitles[5]),
        ['7']*len(allTitles[6]),
        ['8']*len(allTitles[7]),
        ['9']*len(allTitles[8]),
        ['10']*len(allTitles[9])
    ]

    # ------ 資料切割 ------ #
    trainPortion = 0.75

    for a,b in zip(allTitles,allLabels):
        temp_title = round(len(a)*trainPortion)
        temp_label = round(len(b)*trainPortion)
        if temp_title!=temp_label:
            print("!!!!Length Error!!!!")
            break
        else:
            temp = temp_label

        for y in range(temp):
            trainTitle.append(a[y])
            trainLabel.append(b[y])

        for z in range(temp,len(a),1):
            testTitle.append(a[z])
            testLabel.append(b[z])
    

    trainData, testData = [trainTitle,trainLabel], [testTitle,testLabel]
    return [trainData, testData]

def main():
    header = ['title', 'label']
    names = ['train','test']

    data = getData()

    for x,y in zip(names,data):
        createData(x,header,y)
    
if __name__ == "__main__":
    main()