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
    popRank = df.sort_values('comment_count',ascending=True)
    target = popRank['comment_count']
    titles = popRank['title']
    contents = popRank['content']
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

    dataLength = len(target)
    quaLength = dataLength//4
    print("dataLength\n")
    print(dataLength)

    # -- 計算出正向度 -- #

    count_data_PosNeg = [0,0,0]
    PosNegs= []
    for x in range(dataLength):
        if popRank['like_count'][x] > popRank['unlike_count'][x]:
            PosNegs.append('1')
            count_data_PosNeg[0]+=1
        elif popRank['like_count'][x] == popRank['unlike_count'][x]:
            PosNegs.append('2')
            count_data_PosNeg[1]+=1
        elif popRank['like_count'][x] < popRank['unlike_count'][x]:
            PosNegs.append('3')
            count_data_PosNeg[2]+=1

    print("Pos And Neg Distribution :")
    print(count_data_PosNeg)
    print("\n")
    
    # -- 將標題分成四個label -- #
    zero_title, one_title, two_title, three_title = [], [], [], []
    zero_content, one_content, two_content, three_content = [], [], [], []
    zero_PosNeg, one_PosNeg, two_PosNeg, three_PosNeg = [], [], [], []

    print(avg_first_half, avg_target, avg_second_half)
    print("standard deviation : "+str(statistics.stdev(target_int)))
    
    # -- 把 title 拿去分類 -- #
    
    for x in range(dataLength):
        if x<quaLength:
            zero_title.append(titles[x])
            zero_content.append(contents[x])
            zero_PosNeg.append(PosNegs[x])

        elif quaLength <= x < 2 * quaLength:
            one_title.append(titles[x])
            one_content.append(contents[x])
            one_PosNeg.append(PosNegs[x])

        elif 2 * quaLength <= x <3 * quaLength:
            two_title.append(titles[x])
            two_content.append(contents[x])
            two_PosNeg.append(PosNegs[x])

        elif x>3 * quaLength:
            three_title.append(titles[x])
            three_content.append(contents[x])
            three_PosNeg.append(PosNegs[x])

    print("Comment Label Distribution : ")
    print(len(zero_title), len(one_title), len(two_title), len(three_title)) 
    print("\n")
    # -- 標上標籤 -- #
    
    allTitles = [zero_title, one_title, two_title, three_title]
    allContents = [zero_content, one_content, two_content, three_content]
    allPosNegs = [zero_PosNeg, one_PosNeg, two_PosNeg, three_PosNeg]
    allLabels = [
        '1'*len(zero_title),
        '2'*len(one_title),
        '3'*len(two_title),
        '4'*len(three_title)
    ]
    
    # -- 標上標籤 -- #
    count_data_PosNeg = [0,0,0]
    

    # -- 切割 train, test -- #
    
    trainTitle, trainContent, trainPosNeg, trainLabel = [], [], [], []
    testTitle, testContent, testPosNeg, testLabel = [], [], [] , []
    for a,b,c,d in zip(allTitles,allContents,allPosNegs,allLabels):
        temp_title = round(len(a)*trainPortion)
        temp_label = round(len(b)*trainPortion)

        temp = temp_label
        temp_ = len(a)-temp_label

        for y in range(temp_,len(a),1):
            trainTitle.append(a[y])
            trainContent.append(b[y])
            trainPosNeg.append(c[y])
            trainLabel.append([d[y]])

        for z in range(temp,len(a),1):
            testTitle.append(a[z])
            testContent.append(b[z])
            testPosNeg.append(c[z])
            testLabel.append(d[z])
    
    print(len(trainTitle))
    print(len(testTitle))
    trainData, testData = [trainTitle, trainContent, trainPosNeg, trainLabel], [testTitle, testContent, testPosNeg, testLabel]
    return [trainData, testData]

def createData(name,data):
    
    header = ['title', 'content', 'PosNeg', 'label']
    with open(f'{name}_PTT.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        
        title, content, PosNeg, label = data
        length = len(title)

        for x in range(length):
            temp = [title[x],content[x],PosNeg[x],label[x]]
            # print(temp)
            writer.writerow(temp)

def main():
    names = ['train','test']  
    data = genertateFeatureCSV(0.8)
    for x,y in zip(names,data):
        createData(x,y)

if __name__ == "__main__":
    main()