import requests
import json
import sqlite3

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

 
    data[0]['id']

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


res = get_web_info("mood","false",99)

conn.commit()
conn.close()

# createDataStruct()