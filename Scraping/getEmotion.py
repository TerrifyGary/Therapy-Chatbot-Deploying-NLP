import cloudscraper
import time


def main():
    print(getEmotions('238643904'))

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
    timeout = time.time() + 5
    url = "https://www.dcard.tw/service/api/v2/posts/"+postID
    print(url)
    isTarget = False

    while isTarget==False:
        scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
        scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
        result = scraper.get(url).text
        if result[0] == '{':
            isTarget = True
        if time.time() > timeout:
            mood = ["Emotion Error"]*6
            print("Did Not Get Emotion : "+postID + " ." )
            return mood
    time.sleep(3)
    #------- 切割字串元件 -------#
    data = result.replace('{','')
    data = data.replace('}','')
    data = data.replace('"','')
    data = data.replace('[','')
    data = data.replace(']','')
    output = data.split(',')

    #------- 宣告尋找目標 -------#
    isEmotionError = [False, False, False, False, False, False]
    heartReaction = "reactions:[id:286f599c-f86a-4932-82f0-f5a06f1eca03"
    laughReaction = "id:e8e6bc5d-41b0-4129-b134-97507523d7ff"
    shockReaction = "id:4b018f48-e184-445f-adf1-fc8e04ba09b9"
    cryReaction = "id:514c2569-fd53-4d9d-a415-bf0f88e7329f"
    madReaction = "id:aa0d425f-d530-4478-9a77-fe3aedc79eea"
    admiredReaction = "id:011ead16-9b83-4729-9fde-c588920c6c2d"
    
    #------- 條件式抓取目標 -------#
    if  heartReaction in output:
        labelHeart = output.index(heartReaction)
    else:
        # print("labelHeart Error")
        isEmotionError[0] = True
        labelHeart = 0
    
    if laughReaction in output:
        labelLaugh = output.index(laughReaction)
    else:
        # print("labelLaugh Error")
        isEmotionError[1] = True
        labelLaugh = 0


    if  shockReaction in output:
        labelShock = output.index(shockReaction)
    else:
        # print("labelShock Error")
        isEmotionError[2] = True
        labelShock = 0

    if cryReaction in output:

        labelCry = output.index(cryReaction)
    else:
        # print("labelCry Error")
        isEmotionError[3] = True
        labelCry = 0


    if madReaction in output:

        labelMad = output.index(madReaction)
    else:
        # print("labelMad Error")
        isEmotionError[4] = True
        labelMad = 0


    if admiredReaction in output:
        labelAdmired = output.index(admiredReaction)
    else:
        # print("labelAdmired Error")
        isEmotionError[5] = True
        labelAdmired = 0


    #------- 判斷情緒是否都有抓到 -------#
    #------- 並將目標轉換成數字 -------#
    EmotionIndex = [labelHeart, labelLaugh, labelShock, labelCry, labelMad, labelAdmired]
    mood = [0, 0, 0, 0, 0, 0]
    if not any(isEmotionError) == True:
        mood = [0, 0, 0, 0, 0, 0]
    else:
        for x in range(len(isEmotionError)):
            if isEmotionError[x] == True:
                mood[x] = 0
            else:
                indexEmotion = EmotionIndex[x]+1
                mood[x] = convertDigit(output[indexEmotion])
    
    return mood

if __name__ == "__main__":
    main()