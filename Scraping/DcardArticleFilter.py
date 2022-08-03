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
            
    articleFilteredLength = len(aritcleFilteredID) 
    # articleFilteredLength = 3 # 先試試看

    # ============== Code Below Are For Constructing The .db ============== #
    conn = sqlite3.connect('./Scraping/Data/FilteredArticles.db')
    
    c = conn.cursor()
    countContentNotFound = 0
    previousEnd = 0
    minute = 1
    
    for x in range(previousEnd,articleFilteredLength,1):
        if countContentNotFound == 3:
            print("Too Many Content Not Found.")
            break
        articleID = aritcleFilteredID[-x]
        print(articleID)
        articleTitle = aritcleFilteredTitle[-x]
        articleContent = getContent(articleID)
        if articleContent == 'Article Not Found':
            countContentNotFound += 1
        else:
            time.sleep(minute*10)
        print(articleContent)
        heartReaction, laughReaction, shockReaction, cryReaction, madReaction, admiredReaction = getEmotions(articleID)
        temp_list = [articleID, articleTitle, articleContent, heartReaction, laughReaction, shockReaction, cryReaction, madReaction, admiredReaction]
        c.execute('INSERT INTO FilteredArticles VALUES (?,?,?,?,?,?,?,?,?)', temp_list)
        print("Now Finished = "+ str(round((x*100/articleFilteredLength))) +"% ʢᵕᴗᵕʡ, No."+str(x)+". ʕ·ᴥ·ʔ")


    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
    # createDataStruct()