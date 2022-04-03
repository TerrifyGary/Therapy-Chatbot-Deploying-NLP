from bs4 import BeautifulSoup
# from fake_useragent import UserAgent
import requests
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time
import random
import json
import sqlite3

conn = sqlite3.connect('./Scraping/Data/ArticleList.db')
 
def createDataStruct():
    
    c = conn.cursor()
    c.execute('''CREATE TABLE rating
                (id text, title text, excerpt text, withImages bool, withVideos bool)''') 
    conn.commit()
    conn.close()

def get_web_info(topic,popular,length):
    c = conn.cursor()
    result = requests.get(f"https://www.dcard.tw/service/api/v2/forums/{topic}/posts?popular={popular}&limit={str(length)}")
    data = json.loads(result.text)

 
    data[0]['id']

    for x in range(length):
        articleID = (data[x]['id'])
        articleTitle = (data[x]['title'])
        articleExcerpt = (data[x]['excerpt'])
        articleTopics = (data[x]['topics'])
        articleWithImages = (data[x]['withImages'])
        articleWithVideos = (data[x]['withVideos'])
        temp_list = [articleID,articleTitle,articleExcerpt,articleWithImages,articleWithVideos]
        c.execute('INSERT INTO rating VALUES (?,?,?,?,?)', temp_list)
        print(articleID, articleTitle)


res = get_web_info("talk","true",30)

# createDataStruct()

conn.commit()
conn.close()