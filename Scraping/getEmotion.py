import cloudscraper

def main():
    print(getEmotions('239465600'))

#------- 字元轉換成數字 -------#
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
    #------- 抓取目標文章資訊 -------#
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

    #------- 宣告尋找目標 -------#
    isAllEmotionError = True
    heartReaction = "reactions:[id:286f599c-f86a-4932-82f0-f5a06f1eca03"
    laughReaction = "id:e8e6bc5d-41b0-4129-b134-97507523d7ff"
    shockReaction = "id:4b018f48-e184-445f-adf1-fc8e04ba09b9"
    cryReaction = "id:514c2569-fd53-4d9d-a415-bf0f88e7329f"
    madReaction = "id:aa0d425f-d530-4478-9a77-fe3aedc79eea"
    admiredReaction = "id:011ead16-9b83-4729-9fde-c588920c6c2d"
    
    #------- 條件式抓取目標 -------#
    if  heartReaction in output:
        isAllEmotionError = False
        labelHeart = output.index(heartReaction)
    else:
        print("labelHeart Error")
        labelHeart = 0
    
    if laughReaction in output:
        isAllEmotionError = False
        labelLaugh = output.index(laughReaction)
    else:
        print("labelLaugh Error")
        labelLaugh = 0

    if  shockReaction in output:
        isAllEmotionError = False
        labelShock = output.index(shockReaction)
    else:
        print("labelShock Error")
        labelShock = 0

    if cryReaction in output:
        isAllEmotionError = False
        labelCry = output.index(cryReaction)
    else:
        print("labelCry Error")
        labelCry = 0

    if madReaction in output:
        isAllEmotionError = False
        labelMad = output.index(madReaction)
    else:
        print("labelMad Error")
        labelMad = 0

    if admiredReaction in output:
        isAllEmotionError = False
        labelAdmired = output.index(admiredReaction)
    else:
        print("labelAdmired Error")
        labelAdmired = 0

    #------- 判斷情緒是否都有抓到 -------#
    #------- 並將目標轉換成數字 -------#
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