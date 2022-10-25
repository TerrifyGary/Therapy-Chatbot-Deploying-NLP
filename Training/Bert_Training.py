import sys
import numpy as np
import random as rn
import pandas as pd

import torch
from pytorch_pretrained_bert import BertModel
from torch import nn
from pytorch_pretrained_bert import BertTokenizer
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from torch.optim import Adam
from torch.nn.utils import clip_grad_norm_

from keras_preprocessing.sequence import pad_sequences
from IPython.display import clear_output
from transformers import AutoTokenizer, AutoModelForMaskedLM
import matplotlib.pyplot as plt


import sqlite3
import jieba.analyse

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report

# ---- 我也不確定這是尬麻的 ---- #
rn.seed(321)
np.random.seed(321)
torch.manual_seed(321)
torch.cuda.manual_seed(321)

# ---- 載入csv，並切出 text、labels ---- #
train_data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/train.csv')
test_data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/test.csv') 
train_data = train_data.to_dict(orient='records')
test_data = test_data.to_dict(orient='records')
train_texts, train_labels = list(zip(*map(lambda d: (d['title'], d['label']), train_data)))
test_texts, test_labels = list(zip(*map(lambda d: (d['title'], d['label']), test_data)))

# ---- jieba 斷詞，之後 tokenize 要用 ---- #
def jiebaSlice(content):
    stopword_set = []

    with open('/content/drive/MyDrive/Colab Notebooks/stopword.txt','r', encoding='utf-8') as stopwords:
        for stopword in stopwords:
            stopword_set.append(stopword.strip('\n'))

    content = content.strip('\n')
    # jieba.set_dictionary("jieba_dict/dict.txt.big")
    words = jieba.posseg.cut(content)
    slicedWords = []
    for word, flag in words:
        if word not in stopword_set:
            slicedWords.append(word)

    return slicedWords

# ---- 載入要用的tokenizer ---- #
tokenizer = AutoTokenizer.from_pretrained('bert-base-chinese', do_lower_case=True)

# ---- 將文字作斷詞，並加入特殊的token (讓BERT可以訓練) ---- #
train_tokens = list(map(lambda t: ['[CLS]'] + jiebaSlice(t) + ['[SEP]'], train_texts))
test_tokens = list(map(lambda t: ['[CLS]'] + jiebaSlice(t) + ['[SEP]'], test_texts))
# Output: ['[CLS]', '律師', 'ep3', '自閉', '症家', '屬', '理想', '現實', '[SEP]']

# ---- 做tokenize ---- #
train_tokens_ids = pad_sequences(list(map(tokenizer.convert_tokens_to_ids, train_tokens)), maxlen=512, truncating="post", padding="post", dtype="int")
test_tokens_ids = pad_sequences(list(map(tokenizer.convert_tokens_to_ids, test_tokens)), maxlen=512, truncating="post", padding="post", dtype="int")
# Output : [ 101  100 2761  100 6624  102 ... ]

# ---- 將標籤轉成np.array (可以訓練的形狀) ---- #
train_y = np.array(train_labels)
test_y = np.array(test_labels) 

# ---- 設定我們的 masks ---- #
train_masks = [[float(i > 0) for i in ii] for ii in train_tokens_ids]
test_masks = [[float(i > 0) for i in ii] for ii in test_tokens_ids]

# ---- 利用 baseline_model 來預測看看結果 ---- #
baseline_model = make_pipeline(CountVectorizer(ngram_range=(1,10)), LogisticRegression()).fit(train_texts, train_labels)
baseline_predicted = baseline_model.predict(test_texts)
print("BASELINE PREDICTION.")
print(classification_report(test_labels, baseline_predicted))

# ---- BERT Binary 的分類器 ---- #
# !!!! 我覺得問題就在這裡，不應該用 Binary 的才對 !!!! #
class BertBinaryClassifier(nn.Module):
    def __init__(self, dropout=0.1):
        super(BertBinaryClassifier, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-chinese')
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(768, 1)
        # 因為有十種 labels 所以，應該要是 10 才合理，我覺得啦
        # self.linear = nn.Linear(768, 10)
        self.sigmoid = nn.Sigmoid()
        # 可以考慮加入 softmax, cross entropy
    
    def forward(self, tokens, masks=None):
        _, pooled_output = self.bert(tokens, attention_mask=masks, output_all_encoded_layers=False)
        dropout_output = self.dropout(pooled_output)
        linear_output = self.linear(dropout_output)
        # proba = self.sigmoid(linear_output)
        # 應該要輸出十個數值出來
        return proba

# ---- 載入cuda、model ---- #
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
bert_clf = BertBinaryClassifier()
bert_clf = bert_clf.cuda()

# ---- 清除記憶體位置 ---- #
y, x, pooled = None, None, None
torch.cuda.empty_cache()     # Clearing Cache space for fresh Model run
print(str(torch.cuda.memory_allocated(device)/1000000 ) + 'M')

# ---- 將 train 分成五個 BATCH，訓練 10 個 Epochs ---- #
BATCH_SIZE = 5
EPOCHS = 10

# ---- 將tokens、y、mask 轉乘torch.tensor ---- #
train_tokens_tensor = torch.tensor(train_tokens_ids)
train_y_tensor = torch.tensor(train_y.reshape(-1, 1)).float()
train_masks_tensor = torch.tensor(train_masks)

test_tokens_tensor = torch.tensor(test_tokens_ids)
test_y_tensor = torch.tensor(test_y.reshape(-1, 1)).float()
test_masks_tensor = torch.tensor(test_masks)

# ---- 利用 DataLoader 把資料包裝來 ---- #
train_dataset = TensorDataset(train_tokens_tensor, train_masks_tensor, train_y_tensor)
train_sampler = RandomSampler(train_dataset)
train_dataloader = DataLoader(train_dataset, sampler=train_sampler, batch_size=BATCH_SIZE)

test_dataset = TensorDataset(test_tokens_tensor, test_masks_tensor, test_y_tensor)
test_sampler = SequentialSampler(test_dataset)
test_dataloader = DataLoader(test_dataset, sampler=test_sampler, batch_size=BATCH_SIZE)

# ---- 設定 loss function 為 Sigmoid ---- #
param_optimizer = list(bert_clf.sigmoid.named_parameters()) 
optimizer_grouped_parameters = [{"params": [p for n, p in param_optimizer]}]

# ---- 設定 Optimizer 為 Sigmoid ---- #
optimizer = Adam(bert_clf.parameters(), lr=3e-6)

# ---- 再一次清空 cache ---- #
torch.cuda.empty_cache()

# ---- 開始跑訓練 ---- #
for epoch_num in range(EPOCHS):
    bert_clf.train() 
    train_loss = 0
    for step_num, batch_data in enumerate(train_dataloader):
        token_ids, masks, labels = tuple(t.to(device) for t in batch_data)
        print(str(torch.cuda.memory_allocated(device)/1000000 ) + 'M')
        logits = bert_clf(token_ids, masks)
        
        loss_func = nn.BCELoss()

        batch_loss = loss_func(logits, labels)
        train_loss += batch_loss.item()
        
        bert_clf.zero_grad()
        batch_loss.backward()
        
        clip_grad_norm_(parameters=bert_clf.parameters(), max_norm=1.0)
        optimizer.step()
        
        clear_output(wait=True)
        print('Epoch: ', epoch_num + 1)
        print("\r" + "{0}/{1} loss: {2} ".format(step_num, len(train_data) / BATCH_SIZE, train_loss / (step_num + 1)))

# ---- 計算準確度 ---- #
bert_clf.eval()
bert_predicted = []
all_logits = []
with torch.no_grad():
    for step_num, batch_data in enumerate(test_dataloader):

        token_ids, masks, labels = tuple(t.to(device) for t in batch_data)

        logits = bert_clf(token_ids, masks)
        loss_func = nn.BCELoss()
        loss = loss_func(logits, labels)
        numpy_logits = logits.cpu().detach().numpy()
        
        bert_predicted += list(numpy_logits[:, 0] > 0.5)
        all_logits += list(numpy_logits[:, 0])

print("Result.")
print(classification_report(test_y, bert_predicted))