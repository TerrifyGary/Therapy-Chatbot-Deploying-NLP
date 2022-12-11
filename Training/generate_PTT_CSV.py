import csv
from re import X
import sqlite3
import random as rn
import pandas as pd
import statistics

def genertateFeatureCSV(trainPortion):
    
    cnx = sqlite3.connect('./Scraping/Data/PTT_Gossip.db')
    df = pd.read_sql_query("SELECT * FROM ArticlesWithReactions", cnx)

    # -- 計算出這項指標的平均值 -- #
    target = df[]
    titles = df['title']
    target_int = [eval(x) for x in target]
    avg_target = sum(target_int)/len(target_int)
    first_half, second_half = [], []
    
    # -- 計算出小於平均值的平均值 與  大於平均值的平均值 -- #
    for x in target_int:
        if x < avg_target:
            first_half.append(x)
        else:
            second_half.append(x)
    avg_first_half, avg_second_half = sum(first_half)/len(first_half), sum(second_half)/len(second_half)
    
    # -- 將標題分成四個label -- #
    zero_title, one_title, two_title, three_title = [], [], [], []
    print(avg_first_half, avg_target, avg_second_half)
    print("standard deviation : "+str(statistics.stdev(target_int)))
    
    # -- 把 title 拿去分類 -- #
    
    for x in range(len(target)):
        if target_int[x]<avg_first_half:
            zero_title.append(titles[x])
        elif avg_first_half<=x<avg_target:
            one_title.append(titles[x])
        elif avg_target<=x<avg_second_half:
            two_title.append(titles[x])
        elif x>avg_second_half:
            three_title.append(titles[x])
    print(len(zero_title), len(one_title), len(two_title), len(three_title))
    
    # -- 標上標籤 -- #
    
    allTitles = [zero_title, one_title, two_title, three_title]
    allLabels = [
        ['1']*len(zero_title),
        ['2']*len(one_title),
        ['3']*len(two_title),
        ['4']*len(three_title)
    ]
    
    # -- 切割 train, test -- #
    
    trainTitle, trainLabel, testTitle, testLabel = [],[],[],[]
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

def createData(name,data):
    
    header = ['title', 'label']
    with open(f'{name}_PTT.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        
        title, label = data
        length = len(title)

        for x in range(length):
            temp = [title[x],label[x]]
            # print(temp)
            writer.writerow(temp)

def main():
    names = ['train','test']  
    data = genertateFeatureCSV(0.75)
    for x,y in zip(names,data):
        createData(x,y,m)

if __name__ == "__main__":
    main()