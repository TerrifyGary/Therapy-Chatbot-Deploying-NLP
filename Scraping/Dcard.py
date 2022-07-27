import requests
import json
import sqlite3
import cloudscraper

conn = sqlite3.connect('./Scraping/Data/articleList.db')

def createDataStruct():
    
    c = conn.cursor()
    c.execute('''CREATE TABLE articles
                (id text, topic text, title text, excerpt text, withImages bool, withVideos bool)''') 
    conn.commit()
    conn.close()

def get_web_info(topic,popular,length):
    c = conn.cursor()
    result = requests.get(f"https://www.dcard.tw/service/api/v2/forums/{topic}/posts?popular={popular}&limit={str(length)}")
    data = json.loads(result.text)

    for x in range(length):
        articleID = (data[x]['id'])
        articleTitle = (data[x]['title'])
        articleExcerpt = (data[x]['excerpt'])
        articleWithImages = (data[x]['withImages'])
        articleWithVideos = (data[x]['withVideos'])
        articleCategories = topic
        temp_list = [articleID,articleCategories,articleTitle,articleExcerpt,articleWithImages,articleWithVideos]
        c.execute('INSERT INTO articles VALUES (?,?,?,?,?,?)', temp_list)
        print(articleID, articleTitle)

def new_get_web_info(topic,popular,length):
    c = conn.cursor()
    url = f"https://www.dcard.tw/service/api/v2/forums/{topic}/posts?popular={popular}&limit={str(length)}"

    #----- 抓取網頁的html -----#
    isTarget = False
    while isTarget==False:
        scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
        scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
        result = scraper.get(url).text
        if result[0]!='<':
            isTarget = True
            break
    
    #----- 切串切割與整理 -----#
    data = result.replace('{','')
    data = data.replace('}','')
    data = data.replace('[','')
    data = data.replace(']','')
    data = data.replace('"','')
    output = data.split(',')

    #----- 抓取要的重點 -----#
    allID, allTitle, allExcerpt, allWithImages, allWithVideos = [], [], [], [], []
    keyID, keyTitle, keyExcerpy, keyWithImages, keyWithVideos = 'id:', 'tit', 'exc', 'withIm', 'withVi'
    for x in output:
        if x[:3] == keyID and len(x)<=13:
            temp = x
            temp = temp.split(":")[-1]
            allID.append(temp)
        elif x[:3] == keyTitle:
            temp = x
            temp = temp.split(":")[-1]
            allTitle.append(temp)
        elif x[:3] == keyExcerpy:
            temp = x
            temp = temp.split(":")[-1]
            allExcerpt.append(temp)
        if x[:6] == keyWithImages:
            temp = x
            temp = temp.split(":")[-1]
            allWithImages.append(temp)
        elif x[:6] == keyWithVideos:
            temp = x
            temp = temp.split(":")[-1]
            allWithVideos.append(temp)

    #----- 可以存進去資料庫了 -----#
    for x in range(length):
        articleID = (allID[x])
        articleTitle = (allTitle[x])
        articleExcerpt = (allExcerpt[x])
        articleWithImages = (allWithImages[x])
        articleWithVideos = (allWithVideos[x])
        articleCategories = topic
        temp_list = [articleID,articleCategories,articleTitle,articleExcerpt,articleWithImages,articleWithVideos]
        c.execute('INSERT INTO articles VALUES (?,?,?,?,?,?)', temp_list)
        print(articleID, articleTitle)

# res = get_web_info("mood","false",99)
res = new_get_web_info("mood","false",99)
conn.commit()
conn.close()
# createDataStruct()
#----- 嗚嗚嗚嗚 為什麼沒事要加上那個害我全部都要重改 希望不要再被改了哭哭 -----#