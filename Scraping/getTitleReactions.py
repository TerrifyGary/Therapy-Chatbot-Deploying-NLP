import requests
import json
import sqlite3
import cloudscraper

conn = sqlite3.connect('./Scraping/Data/ArticleReactions.db')

def createDataStruct():
    
    c = conn.cursor()
    c.execute('''CREATE TABLE ArticlesWithReactions
                (id text, topic text, title text, commentcount text, likecount text, collectioncont text)''') 
    conn.commit()
    conn.close()
    print('ArticleReactions Created Sucessfully.')

def get_web_info(topic,popular,length):
    c = conn.cursor()
    result = requests.get(f"https://www.dcard.tw/service/api/v2/forums/{topic}/posts?popular={popular}&limit={str(length)}")
    data = json.loads(result.text)

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
    for x in range(length):
        articleID = (allID[x])
        articleTitle = (allTitle[x])
        articleCommentCount = (allCommentCount[x])
        articleLikeCount = (allLikeCount[x])
        articleCollectionCount = (allCollectionCount[x])
        articleCategories = topic
        temp_list = [articleID,articleCategories,articleTitle, articleCommentCount, articleLikeCount, articleCollectionCount]
        c.execute('INSERT INTO ArticlesWithReactions VALUES (?,?,?,?,?,?)', temp_list)
        print(articleID, articleTitle)


def main():
    # res = get_web_info("mood","false",99)
    topic = ['mood','relationship', 'talk']
    for x in topic:
        new_get_web_info(x,"true",99)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
    # createDataStruct()