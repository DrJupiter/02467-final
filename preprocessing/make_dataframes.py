# %%
from html import entities
from xml.etree.ElementInclude import include
import numpy as np
import os
import json
import pandas as pd
import pickle
import re
from collections import defaultdict


# For code path
import sys
from pathlib import Path

# This is used to read files in the module properly when the Main.py script is run from an external location.
#code_path = Path(*Path(os.path.realpath(sys.argv[0])).parts[:-1])
code_path = Path(os.getcwd())

path = code_path.joinpath('./../data/hydrated')
save_path = code_path.joinpath('./../data/dataframes')


#dirs = [os.path.join(path,d) for d in os.listdir(path) if os.path.isdir(os.path.join(path,d))]
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))] 

# hashtags_re = r"#[^#\s.,;:'`]+"
# hashtags_re = re.compile(hashtags_re)

#%%

### Create a df for each json file

# loop over files in path
for file in files:

    # Create new dataframe
    # df = pd.DataFrame(columns=[
    #     "tweet_id",
    #     "user_id",
    #     "parent_id",
    #     "lang",
    #     "text",
    #     "tweet_type",
    #     "created_time",
    #     "hashtags",
    #     "topics",
    #     "mentions",
    #     # "username"
    #     ])

    df = {}

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
                if type_ in ['retweeted']:

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
            df[tweet_id] = essential_tweet_data

    #save df
    new_df = pd.DataFrame.from_dict(df,orient="index")
    new_df.to_pickle(f"{save_path}/{file[:-9]}.pkl") #uncomment to save data
    print("done with file", file[:-9])
    # break

#%%
new_df.loc["1497841013703987200"]

#%%
##############################################################################################
##############################################################################################
#%%
### Create df's by date

# Concat by date and save to data/dataframes_dates
save_path_dates = code_path.joinpath('./../data/dataframes_dates')
dataframes_files = [f for f in os.listdir(save_path) if os.path.isfile(os.path.join(save_path,f))] 

start_date = 0
for i,dataframe in enumerate(dataframes_files):
    if dataframe[-11:-6] != start_date:
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

## Create the one true DF
dataframes_files_dates = [f for f in os.listdir(save_path_dates) if os.path.isfile(os.path.join(save_path_dates,f))] 

MASSIVE_LIST = []
for df_name in dataframes_files_dates:
    df = pd.read_pickle(f"{save_path_dates}/{df_name}")
    MASSIVE_LIST.append(df)
    
THE_GREAT_DF = pd.concat(MASSIVE_LIST)
THE_GREAT_DF.to_pickle(f"THE_ONE_DF.pkl")

#%%
##############################################################################################
##############################################################################################
THE_GREAT_DF = pd.read_pickle("./THE_ONE_DF.pkl")

#%%
## Use the ONE GREAT DF to find all tweets tweeted by a person we has tweeted in either ussian or ukranian

THE_GREAT_DF["iloc"] = np.arange(len(THE_GREAT_DF.index))
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
                    "iloc_value": [tweet[10]]
                    # "en_text":[tweet[11]],
                    # "overall_sentiement":[tweet[12]],
                    # "president": [tweet[13]],
                    # "word_wise_sentiement":[tweet[14]],
                    }
    for index in essential_tweet_data:
        user_dict[tweet[1]][index] += essential_tweet_data[index]
user_MASSIVE_ONE = pd.DataFrame.from_dict(user_dict,orient="index")
#%%

THE_GREAT_DF["nationality"] = "unknown"

#%%

def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    if (a_set & b_set):
        return True 
    else:
        return False
#%%
ru_uk_idxs = []
for i,(langs,ilocs) in enumerate(zip(user_MASSIVE_ONE["langs"],user_MASSIVE_ONE["iloc_value"])):
    
    if "uk" in langs:
        for iloc_ in ilocs:
            THE_GREAT_DF.iloc[iloc_,11] = "uk" 
            ru_uk_idxs.append(iloc_)
    
    if "ru" in langs:
        for iloc_ in ilocs:
            THE_GREAT_DF.iloc[iloc_,11] = "ru" 
            ru_uk_idxs.append(iloc_)

#%%
# len(set(ru_uk_idxs))
#%%

df_ru_uk = THE_GREAT_DF[np.logical_or(THE_GREAT_DF["nationality"] == "uk",THE_GREAT_DF["nationality"] == "ru")]

#%%

df_ru_uk = df_ru_uk.set_index("tweet_id")
df_ru_uk.to_pickle("./dfs/df_ru_uk_n.pkl")

#%%
df_ru_uk
#%%
##############################################################################################
##############################################################################################


## Get packages needed for translation and sentiment

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from googletrans import Translator
from emoji_translate.emoji_translate import Translator as emoji_trans
from nltk.tokenize import word_tokenize

from time import perf_counter

translator = Translator()

analyzer = SentimentIntensityAnalyzer()
emo = emoji_trans(exact_match_only=False, randomize=True)

#%%
## Translate to english and translate emojis

# df_ru_uk = pd.read_pickle("only_ru_uk_data.pkl")
# df_ru_uk = pd.read_pickle("./dfs/translated-text-ru-uk.pkl")
df_ru_uk = pd.read_pickle("./dfs/df_ru_uk_n.pkl")

re_web_finder = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+"

df_ru_uk["en_text"] = "not_assigned"
en_text = []
for i,(txt,lang) in enumerate(zip(df_ru_uk["text"],df_ru_uk["lang"])):

    for r in re.findall(re_web_finder,txt):
        txt = txt.replace(r,".")

    try:
        if lang != "en":
            if lang == "uk":
                src_lang = "ukrainian"
            elif lang == "ru":
                src_lang = "russian"
            txt_no_emos = emo.demojify(txt)
            txt_trans = translator.translate(txt_no_emos,src=src_lang).text
            txt_trans = word_tokenize(txt_trans)
            txt_final = " ".join(map(str,txt_trans)).lower()
            en_text.append(txt_final) 

        else:
            txt_no_emos = emo.demojify(txt)
            txt_trans = word_tokenize(txt_no_emos)
            txt_final = " ".join(map(str,txt_trans)).lower()
            en_text.append(txt_final) 
    except:
        en_text.append(None)

    print(i/180,"%")
    # if i == 100:
    #     break

df_ru_uk["en_text"] = en_text

##############################################################################################
##############################################################################################
#%%
df_ru_uk.to_pickle("./dfs/df_ru_uk_n_trans.pkl")
#%%
###################### RUN SENTIMENT WINDOW PART ######################
#%%
translated_text_ru_uk_sentiment = pd.read_pickle("./dfs/translated-text-ru-uk_sentiment_n.pkl")
#%%
#### Look at who talks about putin and zelensky

putin_words = ["Putin","Vladimir Putin", "putin","vladimir putin"] # dublicate words should be removed when the data is gernereated again, as all will be lower then
zelen_words = ["Volodymyr","Volodymyr Zelenskyy","Zelenskyy","volodymyr zelenskyy","volodymyr","zelenskyy","ZelenskyyUa","Volodymyr Zelensky","Zelensky","zelensky","zelenskyyua"]
re_quote = r"\'(.*?)\'"


def get_president_data(dataframe):
    p,z = 0,0
    topics = dataframe["topics"]
    hastags = dataframe["hashtags"]
    print((dataframe["topics"]))
    
    president_list = []
    
    for i in range(len(topics)):
        # print(topics[i],hastags[i],type(topics[i]),type(hastags[i]))
        tweet_topics = topics[i]+hastags[i] #re.findall(re_quote,topics[i]+hastags[i])
        print(tweet_topics)
        tweet_president_list = []
        # print(tweet_topics)
        if common_member(tweet_topics,putin_words):
            tweet_president_list.append("putin")
            p+= 1

        if common_member(tweet_topics,zelen_words):
            tweet_president_list.append("zelenskyy")
            z+= 1

        president_list.append(tweet_president_list)

    print(p,z)
    return president_list

president_to_df_list = get_president_data(translated_text_ru_uk_sentiment)

# translated_text_ru_uk_sentiment["president_mentioned"] = president_to_df_list
#%%
#%%
df_ru_uk.to_pickle("./dfs/translated-text-ru-uk.pkl")


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
##############################################################################################
##############################################################################################


#%%
# df_uk_ru = pd.read_pickle("df_uk_ru_presidents.pkl")

#%%
## Sentiment

sentiment_list = []
for i,tweet_txt in enumerate(translated_text_ru_uk_sentiment["en_text"]):
    if tweet_txt is not None:
        compound_sentiment = analyzer.polarity_scores(tweet_txt)
        sentiment_list.append(compound_sentiment)
    else:
        sentiment_list.append(None)

translated_text_ru_uk_sentiment["sentiment_scores"] = sentiment_list


#%%
translated_text_ru_uk_sentiment

#%%

##############################################################################################
##############################################################################################
#%%
translated_text_ru_uk_sentiment.to_pickle("./dfs/translated-text-ru-uk.pkl")
#%%

#%%
### MAKE USER DATAFRAME
# save_path_dates = code_path.joinpath('./../data/dataframes_dates')
# dataframes_files_dates = [f for f in os.listdir(save_path_dates) if os.path.isfile(os.path.join(save_path_dates,f))] 
def make_user_df(old_df_name):
    user_dict = defaultdict(lambda : defaultdict(list))

    for i, (idx,tweet) in enumerate(zip(old_df_name.index,old_df_name.values)):
        essential_tweet_data = {
                        "tweet_ids": [idx],
                        "parent_ids": [tweet[1]],
                        "langs":[tweet[2]],
                        "texts":[tweet[3]],
                        "tweet_types":[tweet[4]],
                        "created_times":[tweet[5]],
                        "hashtags":[tweet[6]],
                        "topics":[tweet[7]], 
                        "mentions":[tweet[8]],
                        "iloc": [tweet[9]],
                        "nationality": [tweet[10]],
                        "en_text":[tweet[11]],
                        "overall_sentiement":[tweet[14]],
                        "president": [tweet[13]],
                        "word_wise_sentiement":[tweet[12]],
                        }
        for index in essential_tweet_data:
            user_dict[tweet[0]][index] += essential_tweet_data[index]
    new_df_name = pd.DataFrame.from_dict(user_dict,orient="index")
    return new_df_name

user_tt_ru_uk_s = make_user_df(translated_text_ru_uk_sentiment)
user_tt_ru_uk_s.to_pickle("./dfs/user_trans_senti_ru_uk.pkl")


##############################################################################################
##############################################################################################

#%%
user_tt_ru_uk_s

#%%

##############################################################################################
##############################################################################################

### SAVE FILES

# #%%
# user_df.to_pickle("user_df.pkl")
# #%%
# THE_GREAT_DF.to_pickle("THE_GREAT_DF.pkl")
# #%%
# THE_GREAT_DF = pd.read_pickle("./dfs/THE_GREAT_DF.pkl")
# #%%
# THE_GREAT_DF.loc["1497841013703987200"]
# #%%




# #%%
# df_ru_uk_n = pd.read_pickle("./dfs/translated-text-ru-uk.pkl")
# df_ru_uk_n

# #%%
# # df_ru_uk_n = df_ru_uk_n.set_index("tweet_id")
# df_ru_uk_n["parent_id"] = 0
# #%%
# col_i = df_ru_uk_n.columns.get_loc("parent_id")
# for i,idx in enumerate(df_ru_uk_n.index):
#     # THE_GREAT_DF.loc[tweet_id]
#     df_ru_uk_n.iloc[i, col_i] = THE_GREAT_DF.iloc[idx]["parent_id"]
#     print(i)

# #%%
# df_ru_uk_n.to_pickle("./dfs/translated-text-ru-uk.pkl")


# #%%
# df0227 = pd.read_pickle("./../data/dataframes_dates/02-27.pkl")

# #%%
# df0227.loc["1497841013703987200"]


#%%

#%%
