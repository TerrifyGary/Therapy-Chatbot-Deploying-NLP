########################
# 將文章的熱門度進行label #
########################

import sqlite3
import pandas as pd

def main():
    cnx = sqlite3.connect('./Scraping/Data/labelTitle.db')
    df = pd.read_sql_query("SELECT * FROM labelTitle", cnx)

    length = df.shape[0]
    print(length)

if __name__ == "__main__":
    main()