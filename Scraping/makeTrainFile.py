##############################################
# 將抓取的標題與熱門度資訊做統整，變成可訓練的資料庫 #
##############################################

import sqlite3
import pandas as pd

conn = sqlite3.connect('./Scraping/Data/labelTitle.db')

def createDataStruct():
    conn = sqlite3.connect('./Scraping/Data/labelTitle.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE labelTitle
                (title text, poprank int)''') 
    conn.commit()
    conn.close()
    print("Database Created Successfully.")

def main():
    cnx = sqlite3.connect('./Scraping/Data/ArticleReactions.db')
    df = pd.read_sql_query("SELECT * FROM ArticlesWithReactions", cnx)

    length = df.shape[0]
    popValue = []

    for x in range (length):
        temp = int(df['commentcount'][x]) + int(df['likecount'][x]) + int(df['collectioncont'][x]) 
        popValue.append(temp)

    print(len(popValue))

    c = conn.cursor()

    for x in range(length):
        title = df['title'][x]
        pop = popValue[x]
        temp_list = [title,pop]
        c.execute('INSERT INTO labelTitle VALUES (?,?)', temp_list)

    conn.commit()
    conn.close()

    print(length)

if __name__ == "__main__":
    main()
    # createDataStruct()