##############################################
# 從抓取下來的文章列表中篩選，並抓取標題、內文、情緒 ＃
##############################################

import sqlite3
import pandas as pd
import cloudscraper
from getEmotion import getEmotions
import time

def getContent(postID):
    url = f"https://www.dcard.tw/service/api/v2/posts/{postID}"
    timeout = time.time() + 5
    isTarget = False
    while (isTarget==False):    
        scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
        result = scraper.get(url).text
        if result[0] == '{':
            isTarget = True
        if time.time() > timeout:
            content = "Article Not Found"
            print("Did Not Get The Content : "+postID +" .")
            return content
    data = result.replace('{','')
    data = data.replace('}','')
    data = data.replace('"','')
    data = data.replace('[','')
    data = data.replace(']','')
    output = data.split(',')
    
    content = ''
    for x in output:
        if x[:7] == 'content':
            content = x.split(':')[1]

    return content

def createDataStruct():
    conn = sqlite3.connect('./Scraping/Data/FilteredArticles.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE FilteredArticles
                (id text, title text, content text, heartReaction text, laughReaction text, shockReaction text, cryReaction text, madReaction text, admiredReaction text)''') 
    conn.commit()
    conn.close()
    print("Database Created Successfully.")

def main():
    # ============== Code Below Are For Load In Our .db ============== #

    cnx = sqlite3.connect('./Scraping/Data/articleList.db')
    df = pd.read_sql_query("SELECT * FROM articles", cnx)

    length = df.shape[0]
    aritcleFilteredID = []
    aritcleFilteredCategory = []
    aritcleFilteredTitle = []

    for x in range (length):
        if (df['withImages'][x] == 0 and df['withVideos'][x]==0 and df['topic'][x]=='mood'):
            aritcleFilteredID.append(df['id'][x])
            aritcleFilteredTitle.append(df['title'][x])
            aritcleFilteredCategory.append(df['topic'][x])
            
    #

    # ============== Code Below Are For Constructing The .db ============== #
    conn = sqlite3.connect('./Scraping/Data/FilteredArticles.db')
    
    c = conn.cursor()
    
    countContentNotFound = 0
    previousEnd = 1190
    minute = 0

    articleFilteredLength = len(aritcleFilteredID)
    print(articleFilteredLength)
    # articleFilteredLength = previousEnd+3# 先試試看
    
    for x in range(previousEnd+1,previousEnd+20,1):
        if countContentNotFound == 3:
            print("Too Many Content Not Found.")
            break
        articleID = aritcleFilteredID[-x]
        print("1. "+articleID)
        articleTitle = aritcleFilteredTitle[-x]
        print("2. "+articleTitle)
        articleContent = getContent(articleID)
        if articleContent == 'Article Not Found':
            countContentNotFound += 1
            pass
        else:
            time.sleep(minute*60)
            print("3. "+articleContent)
            heartReaction, laughReaction, shockReaction, cryReaction, madReaction, admiredReaction = getEmotions(articleID)
            print(heartReaction, laughReaction, shockReaction, cryReaction, madReaction, admiredReaction)
            temp_list = [articleID, articleTitle, articleContent, heartReaction, laughReaction, shockReaction, cryReaction, madReaction, admiredReaction]
            c.execute('INSERT INTO FilteredArticles VALUES (?,?,?,?,?,?,?,?,?)', temp_list)
        print("Now Finished = "+ str(round((x*100/articleFilteredLength))) +"% ʢᵕᴗᵕʡ, No."+str(x)+". ʕ·ᴥ·ʔ")
        time.sleep(minute*2)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
    # createDataStruct()