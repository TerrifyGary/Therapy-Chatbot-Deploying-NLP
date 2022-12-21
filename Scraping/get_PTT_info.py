from bs4 import BeautifulSoup
import requests
import sqlite3
import os
from os.path import exists

conn = sqlite3.connect('./Scraping/Data/PTT_Gossip.db')
def createDataStruct():
        
    c = conn.cursor()
    c.execute('''CREATE TABLE ArticlesWithReactions
                (date text, author text, category text, title text, content text, comment_count text, like_count text, unlike_count text, url text)''') 
    conn.commit()
    conn.close()
    print('ArticleReactions Created Sucessfully.')

def get_web_info():
    c = conn.cursor()

    title = []
    title_url = []
    title_url_exitst = []   
    
    pages = 1000
    begin_page = 35037

    print("====== GET URL ======")
    for x in range(pages):
        num = begin_page-x
        url = f'https://www.ptt.cc/bbs/Gossiping/index{num}.html'
        const_url = 'https://www.ptt.cc/'
        web = requests.get(url, cookies={'over18':'1'})
        web.encoding='utf-8'      
        soup = BeautifulSoup(web.text, "html.parser")
        titles = soup.find_all('div', class_='title')
        output = ''           
        for i in titles:
            if i.find('a') != None:
                title.append(i.find('a').get_text())
                title_url.append(const_url + i.find('a')['href'])
        print("\r" + "{0}/{1}".format(x,pages))
    # print(title)
    print("====== CHECK URL WORKS ======")

    times = 0
    for url in title_url:
        web = requests.get(url, cookies={'over18':'1'})
        web.encoding='utf-8'       # 避免中文亂碼
        soup = BeautifulSoup(web.text, "html.parser")
        ERROR_MESSAGE = '404 page not found\n'
        output = soup.get_text()

        if output == ERROR_MESSAGE:
            title_url_exitst.append(0)
        else:
            title_url_exitst.append(1)
        
        times+=1
        print("\r" + "{0}/{1}".format(times,len(title)))

    print("====== WRITE INTO DATABASE ======")
    
    length = len(title_url_exitst)
    for x in range(length):
        if title_url_exitst[x]==1:
            article_url = title_url[x]
            web = requests.get(article_url, cookies={'over18':'1'})
            web.encoding='utf-8'       # 避免中文亂碼
            soup = BeautifulSoup(web.text, "html.parser")
            push = soup.find_all("div",{"class": "push"})
            target_soup = soup.find_all("span",{"class": "article-meta-value"})
            content_soup = soup.find_all("div")

            x_text = []
            for x in content_soup:
                x_text.append(x.text)
            if len(x_text)<5:
                content = "Page Data Not Found"
            else:
                content = x_text[5].split('--')[0]
            temp_content = content.split('\n')[2:]
            content = ''
            for t_con in temp_content:
                if t_con!='\n':
                    content+=t_con

            temp = []

            for x in target_soup:
                temp.append(x.text)
            if len(temp) == 4:
                author, category, title, date = temp
            else:
                author, category, title, date = "Page Data Not Found","Page Data Not Found","Page Data Not Found","Page Data Not Found"
                print("==== DATA NOT FOUND ====")
            
            
            title = title.split('] ')[-1]

            like = 0
            unlike = 0
            comment_count = len(push)

            for p in push:
                comment = str(p.text)
                like_or_unlike = comment[0]
                
                if like_or_unlike == '推':
                    like +=1 
                elif like_or_unlike == '噓':
                    unlike +=1    
        else:
            ERROR_MESSAGE = 'Article_NOT_FOUND'
            date, author, category, title, content, comment_count, like, unlike, article_url = "Article_NOT_FOUND"
            print("==== PAGE NOT FOUND ====")
        
        temp_list = [date, author, category, title, content, comment_count, like, unlike, article_url]
        c.execute('INSERT INTO ArticlesWithReactions VALUES (?,?,?,?,?,?,?,?,?)', temp_list)

        conn.commit()
    conn.close()    

def main():

    # os.remove("./Scraping/Data/PTT_Gossip.db")
    # createDataStruct()

    get_web_info()

if __name__ == "__main__":
    main()