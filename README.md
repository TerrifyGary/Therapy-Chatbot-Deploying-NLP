# Therapy-Chatbot-Deploying-NLP
2022 Paper Project

1. Clone 專案
2. 執行 ```conda activate```
3. 確認所使用的所有函式庫都有安裝妥當。

目標 : 

- 利用爬蟲的方式，將 Dcard 文章抓取下來，將標題、摘要、ID等的關鍵資料，存到 SQL 的資料庫中。
- 將文章內容進行 label ，並將資料傳給 NLP model 進行訓練。
- 設計簡單的 UI，利用 Flask 製作出簡單的網頁 UI。

<img src="https://media.giphy.com/media/KDspjK5MT9xhqyycfR/giphy.gif" width="480" height="270"/>

## Part I. Scraping Scraping And Organizing

To Do List :
- [x] 尋找 Dcard 論壇主題主體架構的```json```檔案。
- [x] 利用 ```json``` 函式庫抓取，並找出想要的資料項。
- [x] 存入 ```SQL``` database，方便未來做資料的存取。
- [x] 簡單的篩選器，將適合的文章篩選出來。
- [x] 利用 ```id``` 抓取符合條件的文章出來，並建立新的 Filterd Articles 資料庫。

## Part II. Slicing Words And Data Preprocessing

To Do List :
- [x] 利用 CKIP 和 Jieba 做斷詞，並比較。
- [ ] 將不需要的符號，過濾出來，讓我們的資料只留關鍵的詞。
 
## Part III. Lableing Training And Refining

To Do List :
- [ ] 上標籤。
- [ ] 找 Pre-trained models。
- [ ] Refine 訓練結果，並多方評估 model 是否合適。
（ 滾動式更新 ）

## Part IV. Front-End Engineering Connecting

To Do List :
- [ ] 間單 HTML UI。
- [ ] 做出聊天室，串接```python code```。
- [ ] 美化。  
（ 滾動式更新 ）