import sqlite3
import random
import pandas as pd
import jieba.analyse
import os
import sys
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER

def jiebaSlice(content):
    stopword_set = []

    with open('Analyzing/stopword.txt','r', encoding='utf-8') as stopwords:
        for stopword in stopwords:
            stopword_set.append(stopword.strip('\n'))

    content = content.strip('\n')
    # jieba.set_dictionary("jieba_dict/dict.txt.big")
    words = jieba.posseg.cut(content)
    slicedWords = []
    for word, flag in words:
        if word not in stopword_set:
            slicedWords.append(word)

    return slicedWords
    
def ckipSlice(content):
    # Download data
    # 下面這邊的，可以想清楚再下載沒關係，因為真的有點大XDD
    # data_utils.download_data("./") 

    # Load model without GPU
    # 啊如果，真的載下來了，記得把路徑改成 ./data
    ws = WS("/Users/garychen/Documents/ckiptagger/data")
    pos = POS("/Users/garychen/Documents/ckiptagger/data")
    ner = NER("/Users/garychen/Documents/ckiptagger/data")
    
    sentence_list = [f'{content}']
    
    word_sentence_list = ws(sentence_list)
    pos_sentence_list = pos(word_sentence_list)
    entity_sentence_list = ner(word_sentence_list, pos_sentence_list)

    # Release model
    del ws
    del pos
    del ner
    
    result = []
    # Show results
    def print_word_pos_sentence(word_sentence, pos_sentence):
        assert len(word_sentence) == len(pos_sentence)
        all_word = []
        for word, pos in zip(word_sentence, pos_sentence):
            # print(f"{word}({pos})", end="\u3000")
            all_word.append(word)
        return all_word

    for i, sentence in enumerate(sentence_list):
        result = (print_word_pos_sentence(word_sentence_list[i],  pos_sentence_list[i]))
    
    return result

def isEmoji(content):
    if not content:
        return False
    if u"\U0001F600" <= content and content <= u"\U0001F64F":
        return True
    elif u"\U0001F300" <= content and content <= u"\U0001F5FF":
        return True
    elif u"\U0001F680" <= content and content <= u"\U0001F6FF":
        return True
    elif u"\U0001F1E0" <= content and content <= u"\U0001F1FF":
        return True
    else:
        return False
    
def listFilter(inputList):    
    temp = []
    emoji = []
    for x in inputList:
        if x.isalpha():
            temp.append(x)
        if isEmoji(x) == True:
            emoji.append(x)
    return temp,emoji

def main():        
    cnx = sqlite3.connect('./Scraping/Data/FilteredArticles.db')
    df = pd.read_sql_query("SELECT * FROM FilteredArticles", cnx)
    length = df.shape[0]

    test_article = df['content'][random.randint(0,length)]

    print(test_article)

    # 看你這邊想要用哪一種。
    # result = ckipSlice(test_article)
    
    result = jiebaSlice(test_article)
    categorizeList = listFilter(result)

    print(categorizeList)

    countFreuency = [[x,result.count(x)] for x in set(result)]

    print(countFreuency)

    output = open('Analyzing/dcard_seg.txt', 'w', encoding='utf-8')
    for x in range(length):
        currentArticle = df["content"][x]
        if currentArticle!="Status Code Error" and currentArticle!="List Error":
            sliceArticle = jiebaSlice(currentArticle)
            categorizeList,emojiList = listFilter(sliceArticle)
            for y in categorizeList:
                output.write(y+' ')
        print("ʢᵕᴗᵕʡ "+str(x)+"/"+str(length)+" ----- "+ str(round((x*100/length))) +"% Data. ʕ·ᴥ·ʔ")
    output.close()

if __name__ == "__main__":
    main()