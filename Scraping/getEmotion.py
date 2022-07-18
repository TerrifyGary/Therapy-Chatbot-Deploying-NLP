from bs4 import BeautifulSoup
# from fake_useragent import UserAgent
import requests
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time
import random
import json
import sqlite3
import cloudscraper

def main():
    #------- 抓取目標文章資訊 -------#
    
    print(getEmotions('239432528'))

def convertDigit(words):
    temp = ""
    for c in words:
        if c.isdigit() == True:
            temp+=c
    temp = int(temp)
    if temp == 4000:
        temp = 0
    return temp

def getEmotions(postID):

    url = "https://www.dcard.tw/service/api/v2/posts/"+postID
    isTarget = False

    while isTarget==False:
        scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
        scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
        result = scraper.get(url).text
        if result[0]!='<':
            isTarget = True
            break

    #------- 切割字串元件 -------#
    data = result.replace('{','')
    data = data.replace('}','')
    data = data.replace('"','')
    output = data.split(',')

    isAllEmotionError = True
    
    if  "reactions:[id:286f599c-f86a-4932-82f0-f5a06f1eca03" in output:
        isAllEmotionError = False
        labelHeart = output.index("reactions:[id:286f599c-f86a-4932-82f0-f5a06f1eca03")
    else:
        print("labelHeart Error")
        labelHeart = 0
    
    if "id:e8e6bc5d-41b0-4129-b134-97507523d7ff" in output:
        isAllEmotionError = False
        labelLaugh = output.index("id:e8e6bc5d-41b0-4129-b134-97507523d7ff")
    else:
        print("labelLaugh Error")
        labelLaugh = 0

    if "id:4b018f48-e184-445f-adf1-fc8e04ba09b9" in output:
        isAllEmotionError = False
        labelShock = output.index("id:4b018f48-e184-445f-adf1-fc8e04ba09b9")
    else:
        print("labelShock Error")
        labelShock = 0

    if "id:514c2569-fd53-4d9d-a415-bf0f88e7329f" in output:
        isAllEmotionError = False
        labelCry = output.index("id:514c2569-fd53-4d9d-a415-bf0f88e7329f")
    else:
        print("labelCry Error")
        labelCry = 0

    if "id:aa0d425f-d530-4478-9a77-fe3aedc79eea" in output:
        isAllEmotionError = False
        labelMad = output.index("id:aa0d425f-d530-4478-9a77-fe3aedc79eea")
    else:
        print("labelMad Error")
        labelMad = 0

    if "id:011ead16-9b83-4729-9fde-c588920c6c2d" in output:
        isAllEmotionError = False
        labelAdmired = output.index("id:011ead16-9b83-4729-9fde-c588920c6c2d")
    else:
        print("labelAdmired Error")
        labelAdmired = 0

    if  isAllEmotionError == True:
        # print("Emotional Error")
        return "Emotional Error."
    else:
        mood = [output[labelHeart+1], output[labelLaugh+1], output[labelShock+1], output[labelCry+1], output[labelMad+1], output[labelAdmired+1]]
        
        numbers = []
        for x in mood:
            numbers.append(convertDigit(x))
        return numbers

if __name__ == "__main__":
    main()