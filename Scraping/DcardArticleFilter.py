from bs4 import BeautifulSoup
import requests
import sqlite3
import pandas as pd

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

# ============== Code Below Are For Scraping Filterd Data .db ============== #

def scapringArticleIndex(category, id):
    url = "https://www.dcard.tw/f/"+category+"/p/"+id
    r = requests.get(url)
    if r.status_code != 200:
        print('Status Code Error')
        text = 'Status Code Error'
    else:
        soup = BeautifulSoup(r.text,'html.parser')
        filter_1 = soup.find_all('div',class_='sc-ebb1bedf-0 aiaXw')
        
        text = filter_1[0].text
        
    return text
    

# ============== Code Below Are For Constructing The .db ============== #

conn = sqlite3.connect('./Scraping/Data/FilteredArticles.db')
def createDataStruct():
    
    c = conn.cursor()
    c.execute('''CREATE TABLE FilteredArticles
                (id text, title text, content text)''') 
    conn.commit()
    conn.close()


c = conn.cursor()

for x in range(100):
    articleID = aritcleFilteredID[x]
    articleTitle = aritcleFilteredTitle[x]
    articleCategory = aritcleFilteredCategory[x]
    articleContent = scapringArticleIndex(articleCategory,articleID)
    temp_list = [articleID, articleTitle,articleContent]
    c.execute('INSERT INTO FilteredArticles VALUES (?,?,?)', temp_list)


conn.commit()
conn.close()

# createDataStruct()