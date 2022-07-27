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
            print("Did Not Get The Result : "+postID +" .")
            break
    
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
            
    # articleFilteredLength = len(aritcleFilteredID) 
    articleFilteredLength = 10 # 先試試看

    # ============== Code Below Are For Constructing The .db ============== #
    conn = sqlite3.connect('./Scraping/Data/FilteredArticles.db')
    def createDataStruct():
        
        c = conn.cursor()
        c.execute('''CREATE TABLE FilteredArticles
                    (id text, title text, content text, heartReaction text, laughReaction text, shockReaction text, cryReaction text,  text,  text)''') 
        conn.commit()
        conn.close()


    c = conn.cursor()

    
    for x in range(articleFilteredLength):
        articleID = aritcleFilteredID[x]
        print(articleID)
        articleTitle = aritcleFilteredTitle[x]
        articleContent = getContent(articleID)
        allEmotions = getEmotions(articleID)
        heartReaction, laughReaction, shockReaction, cryReaction, madReaction, admiredReaction = allEmotions
        temp_list = [articleID, articleTitle, articleContent, heartReaction, laughReaction, shockReaction, cryReaction, madReaction, admiredReaction]
        c.execute('INSERT INTO FilteredArticles VALUES (?,?,?,?,?,?,?,?,?)', temp_list)
        print("Now Finished = "+ str(round((x*100/articleFilteredLength))) +"% ʢᵕᴗᵕʡ, No."+str(x)+". ʕ·ᴥ·ʔ")

    conn.commit()
    conn.close()

    # createDataStruct()

if __name__ == "__main__":
    main()