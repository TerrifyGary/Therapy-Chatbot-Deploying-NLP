########################
# 將文章的熱門度進行label #
########################

import sqlite3
import pandas as pd
# Create your connection.
def main():
    cnx = sqlite3.connect('./Scraping/Data/labelTitle.db')
    df = pd.read_sql_query("SELECT * FROM labelTitle", cnx)

    length = df.shape[0]
    tenthLength = length//10

    popRank = df.sort_values('poprank',ascending=True)
    titles = []
    labels = []

    for x in range(length):
        titles.append(popRank['title'][x])
        if x <= tenthLength:
            labels.append('1')
        elif x > tenthLength and x <= 2*tenthLength:
            labels.append('2')
        elif x > 2*tenthLength and x <= 3*tenthLength:
            labels.append('3')
        elif x > 3*tenthLength and x <= 4*tenthLength:
            labels.append('4')
        elif x > 4*tenthLength and x <= 5*tenthLength:
            labels.append('5')
        elif x > 5*tenthLength and x <= 6*tenthLength:
            labels.append('6')
        elif x > 6*tenthLength and x <= 7*tenthLength:
            labels.append('7')
        elif x > 7*tenthLength and x <= 8*tenthLength:
            labels.append('8')
        elif x > 8*tenthLength and x <= 9*tenthLength:
            labels.append('9')
        elif x > 9*tenthLength:
            labels.append('10')

    for x in range(length):
        print(titles[x], labels[x])
    
    print(length)

if __name__ == "__main__":
    main()