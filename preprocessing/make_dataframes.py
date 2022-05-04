# %%
from html import entities
from xml.etree.ElementInclude import include
import numpy as np
import os
import json
import pandas as pd
import pickle

from collections import defaultdict


# For code path
import sys
from pathlib import Path

# This is used to read files in the module properly when the Main.py script is run from an external location.
#code_path = Path(*Path(os.path.realpath(sys.argv[0])).parts[:-1])
code_path = Path(os.getcwd())

##%%


path = code_path.joinpath('./../data/hydrated')
save_path = code_path.joinpath('./../data/dataframes')


#dirs = [os.path.join(path,d) for d in os.listdir(path) if os.path.isdir(os.path.join(path,d))]
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))] 


## %%
# files.sort(key = lambda x: x[:10])
# files
## %%
import re

hashtags_re = r"#[^#\s.,;:'`]+"
hashtags_re = re.compile(hashtags_re)
#for te in test_string:
#    print(hashtags.findall(y,te))

#%%

### Create a df for each json file

# loop over files in path
for file in files:

    # Create new dataframe
    df = pd.DataFrame(columns=[
        "tweet_id",
        "user_id",
        "parent_id",
        "lang",
        "text",
        "tweet_type",
        "created_time",
        "hashtags",
        "topics",
        "mentions",
        # "username"
        ])

    # load data
    with open(path.joinpath(file),'r') as f:
        data = json.load(f)

    # loop over tweetsets in file
    for q,tweetset in enumerate(data):

        # get list of ref tweets
        if tweetset.get("includes") is not None:
            ref_tweets = tweetset['includes'].get('tweets')  # Get retuns None, if the index isnt avail
        else:
            continue

        # get ref ids
        if ref_tweets is not None:
            ref_tweet_ids = {ref_tweets[i]['id']:ref_tweets[i] for i in range(len(ref_tweets))}

        # Get all normal tweet data
        tweets = tweetset['data']

        # loop over tweets in tweetset
        for t,tweet in enumerate(tweets):

            # get universal data 1
            tweet_id = tweet["id"]
            user_id = tweet["author_id"]
            created_at = tweet["created_at"]
            parent_id = None
            
            # print(tweet_id)

            # Get tweet type
            type_ = "original"
            type_data = tweet.get('referenced_tweets')

            if type_data is not None:
                type_ = type_data[0]['type']
                parent_id = type_data[0]['id']

                # # Special if not original tweet
                if type_ in ['retweeted', 'replied_to']:

                    # get proper context annotations, text and id
                    # if ref_tweets is not None:

                        # get real id
                        
                    _tweet = ref_tweet_ids.get(parent_id)

                    if _tweet is not None:
                        reffing_tweet = tweet
                        tweet = _tweet
                                         
            ### Start getting values for dataframe

            ## Get universal data 2
            lang = tweet["lang"].lower()
            text = tweet["text"].lower() #ADDED lower (untested)

            hashtag_list = []
            mention_list = []
            context_anno_domains = []

            domains = tweet.get('context_annotations')
            if domains is not None:
                topics = [dom['entity']['name'] for dom in tweet['context_annotations']]
                topics = set(topics)
                for topic in topics:
                    context_anno_domains.append(topic.lower())
            

            tweet_entities = tweet.get("entities")
            if tweet_entities is not None:
                hashtags_ = tweet_entities.get("annotations")
                mentions_ = tweet_entities.get("mentions")

                if hashtags_ is not None:
                    for hashtag in hashtags_:
                        tag = hashtag["normalized_text"]
                        hashtag_list.append(tag.lower())
                    
                if mentions_ is not None:
                    for mention in mentions_:
                        mention_username = mention["username"]
                        mention_id = mention["id"]
                        mention_list.append([mention_id.lower(),mention_username.lower()])

            essential_tweet_data = {
                                    "tweet_id": tweet_id,
                                    "user_id": user_id,
                                    "parent_id": parent_id,
                                    "lang":lang,
                                    "text":text,
                                    "tweet_type":type_,
                                    "created_time":created_at,
                                    "hashtags":hashtag_list,
                                    "topics":context_anno_domains, 
                                    "mentions":mention_list,
                                    # username
                                    }
            df.loc[tweet_id] = essential_tweet_data

    #save df
    df.to_pickle(f"{save_path}/{file[:-9]}.pkl") #uncomment to save data
    print("done with file", file[:-9])

#%%

### Create df's by date

# Concat by date and save to data/dataframes_dates
save_path_dates = code_path.joinpath('./../data/dataframes_dates')
dataframes_files = [f for f in os.listdir(save_path) if os.path.isfile(os.path.join(save_path,f))] 

start_date = 0
for i,dataframe in enumerate(dataframes_files):
    if dataframe[-11:-6] != start_date:
        print(dataframe[-11:-6],start_date, dataframe[-11:-6] != start_date)
        if i > 0:
            df = pd.concat(df_list)
            df.to_pickle(f"{save_path_dates}/{start_date}.pkl")
        start_date = dataframe[-11:-6]
        df_list = []
        df = pd.read_pickle(f"{save_path}/{dataframe}")  
        df_list.append(df)
    else:
        df = pd.read_pickle(f"{save_path}/{dataframe}")  
        df_list.append(df)
df = pd.concat(df_list)
df.to_pickle(f"{save_path_dates}/{start_date}.pkl")




#%%

##############################################################################################
##############################################################################################

#%%

#### Look at who talks about putin and zelensky

def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    if (a_set & b_set):
        return True 
    else:
        return False

putin_words = ["Putin","Vladimir Putin", "putin","vladimir putin"] # dublicate words should be removed when the data is gernereated again, as all will be lower then
zelen_words = ["Volodymyr","Volodymyr Zelenskyy","Zelenskyy","volodymyr zelenskyy","volodymyr","zelenskyy","ZelenskyyUa","Volodymyr Zelensky","Zelensky","zelensky"]

def get_president_data(dataframe):
    
    topics = dataframe["topics"] + dataframe["hashtags"]

    putin_list, zelensky_list = [], []
    
    for tweet_topics in topics:        

        if common_member(tweet_topics,putin_words):
            putin_list.append(dataframe["tweet_id"])

        if common_member(tweet_topics,zelen_words):
            zelensky_list.append(dataframe["tweet_id"])

    return putin_list, zelensky_list

l1, l2 = get_president_data(df)
len(l1), len(l2)

#%%

dataframes_files_dates = [f for f in os.listdir(save_path_dates) if os.path.isfile(os.path.join(save_path_dates,f))] 

tweeted_putin_id_list, tweeted_zelen_id_list = [], []
for df_name in dataframes_files_dates:
    df = pd.read_pickle(f"{save_path_dates}/{df_name}")
    putin_list, zelen_list = get_president_data(df)  
    tweeted_putin_id_list += putin_list
    tweeted_zelen_id_list += zelen_list

len(tweeted_putin_id_list), len(tweeted_zelen_id_list)

#%%

## Create the one true DF

MASSIVE_LIST = []
for df_name in dataframes_files_dates:
    df = pd.read_pickle(f"{save_path_dates}/{df_name}")
    MASSIVE_LIST.append(df)
    
THE_GREAT_DF = pd.concat(MASSIVE_LIST)
# THE_GREAT_DF.to_pickle(f"THE_ONE_DF.pkl")

#%%

## Lang counter

en_counter = 0
for lang in THE_GREAT_DF["lang"]:
    if lang == "en":
        en_counter += 1

en_counter/len(THE_GREAT_DF)

#%%


##############################################################################################
##############################################################################################




#%%
### MAKE USER DATAFRAME
save_path_dates = code_path.joinpath('./../data/dataframes_dates')
dataframes_files_dates = [f for f in os.listdir(save_path_dates) if os.path.isfile(os.path.join(save_path_dates,f))] 

#%%

user_dict = defaultdict(lambda : defaultdict(list))

for df_name in dataframes_files_dates:
    df = pd.read_pickle(f"{save_path_dates}/{df_name}")
    # print(df)
    for i,tweet in enumerate(df.values):
        essential_tweet_data = {
                        "tweet_ids": [tweet[0]],
                        "parent_ids": [tweet[2]],
                        "langs":[tweet[3]],
                        "texts":[tweet[4]],
                        "tweet_types":[tweet[5]],
                        "created_times":[tweet[6]],
                        "hashtags":[tweet[7]],
                        "topics":[tweet[8]], 
                        "mentions":[tweet[9]],
                        }
        for index in essential_tweet_data:
            user_dict[tweet[1]][index] += essential_tweet_data[index]
#%%
user_df = pd.DataFrame.from_dict(user_dict,orient="index")










#%%
##############################################################################################
##############################################################################################
##############################################################################################

#%%

## Get packages needed for translation and sentiment

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from googletrans import Translator
from emoji_translate.emoji_translate import Translator as emoji_trans
import wordninja as nin
from time import perf_counter

translator = Translator()

analyzer = SentimentIntensityAnalyzer()
emo = emoji_trans(exact_match_only=False, randomize=True)


#%%
start = perf_counter()
non_en = []
for i, lang in enumerate(THE_GREAT_DF["lang"]):
    if lang != "en":
        non_en.append(i)

print(perf_counter()-start)



#%%


#%%

dfs = [pd.read_pickle(f"{save_path_dates}/{df_name}") for df_name in dataframes_files_dates]
#%%
lang_df = pd.read_csv("lang_proxy.csv")
df_ru_uk = lang_df[np.logical_or(lang_df["lang"]=="ru",lang_df["lang"]=="uk")]
len(df_ru_uk)
#%%

## Translate to english and translate emojis

re_web_finder = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+"

start_time = perf_counter()

df_ru_uk["en_text"] = "not_assigned"
en_text = []
for i,(txt,lang) in enumerate(zip(df_ru_uk["text"],df_ru_uk["lang"])):

    for r in re.findall(re_web_finder,txt):
        txt = txt.replace(r,".")
    try:
        if lang != "en":
            txt_no_emos = emo.demojify(txt)
            txt_trans = translator.translate(txt_no_emos).text
            txt_trans = nin.split(txt_trans)
            txt_final = " ".join(map(str,txt_trans)).lower()
            en_text.append(txt_final) 

        else:
            txt_no_emos = emo.demojify(txt)
            txt_trans = nin.split(txt_no_emos)
            txt_final = " ".join(map(str,txt_trans)).lower()
            en_text.append(txt_final) 
    except:
        en_text.append(None)


    print(i)
    # if i % 1000 == 0 and i > 0:
    #     break


print(perf_counter()-start_time)

#%%
df_ru_uk["en_text"] = en_text
# # %%
# NN = int(N/100)
# for i in range(NN):
#     # print(i % int(NN/10))
#     if i % int(NN/10) == 0:
#         print(True,i)
#%%
df_ru_uk.to_pickle("only_ru_uk_data")
#%%


#%%
t = "https://t.co/8arxrlzszg i hope the ukrainian followers i might have are safe, i hope https://t.co/8alzszg from the bottom of my heart that all ukrainians are safe, you don't deserve any of this, you deserve much, much better. sending love and support.♡❤"

t.replace("hope"," ")
# t

for r in re.findall(re_web_finder,t):
    t = t.replace(r," ")

t

#%%

tt = "fisk"
tt.replace("f"," ")


#%%
## Sentiment

for i,tweet_id in enumerate(THE_GREAT_DF.index):
    txt = THE_GREAT_DF["text"].loc[tweet_id]
    compound_sentiment = analyzer.polarity_scores(txt)["compound"]
    THE_GREAT_DF.loc[tweet_id]["compound_sentiment"] = compound_sentiment






#%%
THE_GREAT_DF

#%%
[x for x in THE_GREAT_DF]

#%%

aa = pd.DataFrame(columns=["fisk","ged"])
aa.at[1,["fisk"]] = 2
aa.at[3,["ged"]] = 3

aa["tyk"] = [33,33]

aa




#%%

user_dict = defaultdict(lambda : defaultdict(list))


for i,tweet in enumerate(THE_GREAT_DF.values):
    essential_tweet_data = {
                    "tweet_ids": [tweet[0]],
                    "parent_ids": [tweet[2]],
                    "langs":[tweet[3]],
                    "texts":[tweet[4]],
                    "tweet_types":[tweet[5]],
                    "created_times":[tweet[6]],
                    "hashtags":[tweet[7]],
                    "topics":[tweet[8]], 
                    "mentions":[tweet[9]],
                    }
    for index in essential_tweet_data:
        user_dict[tweet[1]][index] += essential_tweet_data[index]
#%%
user_df = pd.DataFrame.from_dict(user_dict,orient="index")







#%%

##############################################################################################
##############################################################################################

### SAVE FILES

#%%
user_df.to_pickle("user_df.pkl")
#%%
THE_GREAT_DF.to_pickle("THE_GREAT_DF.pkl")
#%%
THE_GREAT_DF = pd.read_pickle("THE_GREAT_DF.pkl")
#%%

#%%