####################################
# 抓取文章的標題、留言數、愛心數、收藏數 #
####################################
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import requests
import json
import sqlite3
import cloudscraper
import time



conn = sqlite3.connect('./Scraping/Data/ArticleReactions.db')

def createDataStruct():
    
    c = conn.cursor()
    c.execute('''CREATE TABLE ArticlesWithReactions
                (id text, topic text, title text, commentcount text, likecount text, collectioncont text)''') 
    conn.commit()
    conn.close()
    print('ArticleReactions Created Sucessfully.')

def get_web_info_json(topic,popular,length):
    c = conn.cursor()
    result = requests.get(f"https://www.dcard.tw/service/api/v2/forums/{topic}/posts?popular={popular}&limit={str(length)}")
    data = json.loads(result.text)
    print(result)

    for x in range(length):
        articleID = (data[x]['id'])
        articleTitle = (data[x]['title'])
        articleCommentCount = (data[x]['excerpt'])
        articleLikeCount = (data[x]['withImages'])
        articleCollectionCount = (data[x]['withVideos'])
        articleCategories = topic
        temp_list = [articleID,articleCategories,articleTitle,articleCommentCount,articleLikeCount,articleCollectionCount]
        c.execute('INSERT INTO ArticlesWithReactions VALUES (?,?,?,?,?,?)', temp_list)
        print(articleID, articleTitle)
    
    conn.commit()
    conn.close()

def get_web_info_selenium(topic,popular):
    c = conn.cursor()

    url = f"https://www.dcard.tw/service/api/v2/forums/{topic}/posts?popular={popular}&limit={str(99)}"

    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    time.sleep(3)
    driver.close()

    soup = BeautifulSoup(html,"html.parser")
    data = json.loads(soup.text)
    # length = len(data['id'])

    for x in range(90):
        articleID = (data[x]['id'])
        articleTitle = (data[x]['title'])
        articleCommentCount = (data[x]['totalCommentCount'])
        articleLikeCount = (data[x]['likeCount'])
        articleCollectionCount = (data[x]['collectionCount'])
        articleCategories = topic
        temp_list = [articleID,articleCategories,articleTitle,articleCommentCount,articleLikeCount,articleCollectionCount]
        c.execute('INSERT INTO ArticlesWithReactions VALUES (?,?,?,?,?,?)', temp_list)
        print(articleID, articleTitle)
    
    conn.commit()
    


def get_web_info_cloudscraper(topic,popular):
    print("new_get_web_info Function.")
    c = conn.cursor()
    url = f"https://www.dcard.tw/service/api/v2/forums/{topic}/posts?popular={popular}&limit={str(99)}"

    #----- 抓取網頁的html -----#
    noTargetTimes = 0
    isTarget = False
    while isTarget==False:
        # scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
        scraper = cloudscraper.create_scraper(
            interpreter='nodejs',
            captcha={
                'provider': 'capmonster',
                'api_key': '05637e39a4e150c8d01f13f1cb905747',
                'no_proxy':'True'
            }
        )  # returns a CloudScraper instance
        result = scraper.get(url).text
        noTargetTimes+=1
        if result[0]!='<':
            isTarget = True
            break
        else:
            print("No Target Times = "+str(noTargetTimes))
            if noTargetTimes>=10:
                isTarget = False
                break
    
    if isTarget==True:
        #----- 切串切割與整理 -----#
        data = result.replace('{','')
        data = data.replace('}','')
        data = data.replace('[','')
        data = data.replace(']','')
        data = data.replace('"','')
        output = data.split(',')

        #----- 抓取要的重點 -----#
        allID, allTitle, allCommentCount, allLikeCount, allCollectionCount = [], [], [], [], []
        keyID, keyTitle, keyCommentCount, keyLikeCount, keyCollectionCount = 'id:', 'tit', 'com', 'lik', 'col'
        for x in output:
            if x[:3] == keyID and len(x)<=13:
                temp = x
                temp = temp.split(":")[-1]
                allID.append(temp)
            elif x[:3] == keyTitle:
                temp = x
                temp = temp.split(":")[-1]
                allTitle.append(temp)
            elif x[:3] == keyCommentCount:
                temp = x
                temp = temp.split(":")[-1]
                allCommentCount.append(temp)
            elif x[:3] == keyLikeCount:
                temp = x
                temp = temp.split(":")[-1]
                allLikeCount.append(temp)
            elif x[:3] == keyCollectionCount:
                temp = x
                temp = temp.split(":")[-1]
                allCollectionCount.append(temp)

        #----- 可以存進去資料庫了 -----#
        for x in range(len(allID)):
            articleID = (allID[x])
            articleTitle = (allTitle[x])
            articleCommentCount = (allCommentCount[x])
            articleLikeCount = (allLikeCount[x])
            articleCollectionCount = (allCollectionCount[x])
            feedbackList = [articleCommentCount, articleLikeCount, articleCollectionCount]
            articleCategories = topic
            temp_list = [articleID,articleCategories,articleTitle, articleCommentCount, articleLikeCount, articleCollectionCount]
            c.execute('INSERT INTO ArticlesWithReactions VALUES (?,?,?,?,?,?)', temp_list)
            print(articleID, articleTitle)

        conn.commit()
        conn.close()
    else:
        print('CloudScrapper Failed TO Get Article Info.')



def main():
    # get_web_info_selenium("mood","true")
    # get_web_info_selenium("mood","false")
    # get_web_info_selenium("relationship","true")
    # get_web_info_selenium("relationship","false")
    # get_web_info_selenium("talk","true")
    get_web_info_selenium("talk","false")



    # topic = ['mood','relationship', 'talk']
    # for x in topic:
    #     get_web_info_selenium(x,"true")
    #     # time.sleep(60)
    #     get_web_info_selenium(x,"false")
    #     # time.sleep(60)
    conn.close()


if __name__ == "__main__":
    main()
    # createDataStruct()