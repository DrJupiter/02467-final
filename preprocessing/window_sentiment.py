#%%
import pandas as pd
import pickle
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.text import Text
from nltk.tokenize import word_tokenize

s_analyzer = SentimentIntensityAnalyzer()
df_uk_ru = pd.read_pickle("only_ru_uk_data.pkl")

#%%

def window_sentiment(txt,word,window_size):
    # print(word_tokenize(txt))
    concordance = Text(word_tokenize(txt)).concordance_list(word,width=window_size*10)
    # print(concordance)
    sentiment_list = []
    for concor in concordance:
        txt_list = concor.left[-window_size:] + concor.right[:window_size]
        txt = " ".join(map(str,txt_list))
        sentiment_list.append(s_analyzer.polarity_scores(txt))
    return sentiment_list

txtt = df_uk_ru.iloc[0]["en_text"] + ' ' + 'ukraine love'

window_sentiment(txtt,"ukraine",5)
#%%
keys = ["neg", "neu","pos","compound"]

def equalize_sentiment(sentiment_list,keys=keys):
    N = len(sentiment_list)

    d = {key:0 for key in keys}
    for sentiment_dicts in sentiment_list:
        for key in keys:
            d[key] += sentiment_dicts[key]/N

    return d

txtt = df_uk_ru.iloc[0]["en_text"] + ' ' + 'ukraine love'
sentiment_list = window_sentiment(txtt,"ukraine",5)
equalize_sentiment(sentiment_list, keys = keys)

#%%
search_words = ["ukraine","russia","putin","zelensky","zelenskyy"]

def sentiment_dict_from_txt(txt,search_words = search_words):
    
    topic_d = {}
    for word in search_words:
        sentiment_list = window_sentiment(txt,word,5)
        if len(sentiment_list) == 1:
            topic_d[word] = sentiment_list[0]
        else:
            topic_d[word] = equalize_sentiment(sentiment_list)

    zelensky_list = [topic_d["zelensky"],topic_d["zelenskyy"]]
    topic_d["zelenskyy"] = equalize_sentiment(zelensky_list)
    del topic_d["zelensky"]
    return topic_d

txtt = df_uk_ru.iloc[0]["en_text"] + ' ' + 'ukraine'+ "zelensky fat bad" + "zelenskyy good nice"
sentiment_dict_from_txt(txtt,search_words = search_words)

#%%

wordwise_sentiment_list = []
for i,en_text in enumerate(df_uk_ru["en_text"]):
    if en_text is not None:
        sent_d = sentiment_dict_from_txt(en_text)
        wordwise_sentiment_list.append(sent_d)
    else:
        wordwise_sentiment_list.append(None)

df_uk_ru["sentiment_dict"] = wordwise_sentiment_list

#%%
df_uk_ru