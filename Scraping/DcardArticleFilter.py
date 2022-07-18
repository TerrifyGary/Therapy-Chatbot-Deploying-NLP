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

# ============== Codes Below Are For Getting Today's ClassName ============== #

def secretClassName():
    url = "https://www.dcard.tw/f/relationship/p/235931948"
    className = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    divs = soup.findAll('div')

    for i in divs:
        if i.has_attr('class'):
            className.append(i.get('class'))
    x = className[54]
    target = x[0] + " " + x[1] # 這邊有點寫死，但能用就好 >W<"
    return target

# ============== Codes Below Are For Scraping Filterd Data .db ============== #

def scapringArticleIndex(category, id, className):
    url = "https://www.dcard.tw/f/"+category+"/p/"+id
    r = requests.get(url)

    if r.status_code != 200:
        print('Status Code Error')
        text = 'Status Code Error'
    else:
        soup = BeautifulSoup(r.text,'html.parser')
        #--- Below is to scrape the whole article ---#
        filter_1 = soup.find_all('div',class_='sc-93f2df6d-0 gUmQDX')
        if filter_1 is not None and len(filter_1) >= 1:
            text = filter_1[0].text
        else:
            text = 'List Error'
        
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

target = secretClassName()
print("Target = "+target)

for x in range(articleFilteredLength):
    articleID = aritcleFilteredID[x]
    articleTitle = aritcleFilteredTitle[x]
    articleCategory = aritcleFilteredCategory[x]
    articleContent = scapringArticleIndex(articleCategory,articleID,target)
    temp_list = [articleID, articleTitle,articleContent]
    c.execute('INSERT INTO FilteredArticles VALUES (?,?,?)', temp_list)
    print("Now Finished = "+ str(round((x*100/articleFilteredLength))) +"% ʢᵕᴗᵕʡ, No."+str(x)+". ʕ·ᴥ·ʔ")
    print(articleID)

conn.commit()
conn.close()

# createDataStruct()