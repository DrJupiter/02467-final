# %%
from html import entities
import numpy as np
import os
import json
import pandas as pd
import pickle

from collections import defaultdict


# For code path
import sys
from pathlib import Path

from sympy import topological_sort

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

# our_hashtags = defaultdict(int)
# twit_hashtags = defaultdict(int)

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
        ref_tweets = tweetset['includes'].get('tweets')  # Get retuns None, if the index isnt avail

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
            type = "original"
            type_data = tweet.get('referenced_tweets')

            if type_data is not None:
                type = type_data[0]['type']
                parent_id = type_data[0]['id']

                # # Special if not original tweet
                if type in ['retweeted', 'replied_to']:

                    # get proper context annotations, text and id
                    # if ref_tweets is not None:

                        # get real id
                        
                    _tweet = ref_tweet_ids.get(parent_id)

                    if _tweet is not None:
                        reffing_tweet = tweet
                        tweet = _tweet

                        # parent only relevant for these types of tweets
                        # parent_id = tweet["id"]

                            


                        # else:
                        #     if tweet.get('context_annotations') is None:
                        #         tweet_text = tweet['text']
                        #         for hashtag in hashtags.findall(tweet_text):
                        #             # Hashtags
                        #             None
                        #         continue

                                                
            ### Start getting values for dataframe

            ## Get universal data 2
            lang = tweet["lang"]
            text = tweet["text"]

            hashtag_list = []
            mention_list = []
            context_anno_domains = []

            domains = tweet.get('context_annotations')
            if domains is not None:
                topics = [dom['entity']['name'] for dom in tweet['context_annotations']]
                topics = set(topics)
                for topic in topics:
                    context_anno_domains.append(topic)
            

            tweet_entities = tweet.get("entities")
            if tweet_entities is not None:
                hashtags_ = tweet_entities.get("annotations")
                mentions_ = tweet_entities.get("mentions")

                if hashtags_ is not None:
                    for hashtag in hashtags_:
                        tag = hashtag["normalized_text"]
                        hashtag_list.append(tag)
                    
                if mentions_ is not None:
                    for mention in mentions_:
                        mention_username = mention["username"]
                        mention_id = mention["id"]
                        mention_list.append([mention_id,mention_username])

            essential_tweet_data = {
                                    "tweet_id": tweet_id,
                                    "user_id": user_id,
                                    "parent_id": parent_id,
                                    "lang":lang,
                                    "text":text,
                                    "tweet_type":type,
                                    "created_time":created_at,
                                    "hashtags":hashtag_list,
                                    "topics":context_anno_domains, 
                                    "mentions":mention_list,
                                    # username
                                    }
            df.loc[tweet_id] = essential_tweet_data
            # print(df)
            # print("Fisk",tweet_id)
            # print(len(essential_tweet_data))
            # df = df.append(essential_tweet_data, ignore_index=True)
            # print(df)

    #save df
    df.to_pickle(f"{save_path}/{file[:-9]}.pkl")
    print("done with file", file[:-9])

#%%

### Concat by date and save to data/dataframes_dates
save_path_dates = code_path.joinpath('./../data/dataframes_dates')
dataframes_files = [f for f in os.listdir(save_path) if os.path.isfile(os.path.join(save_path,f))] 

start_date = 0
for i,dataframe in enumerate(dataframes_files):
    if dataframe[-11:-6] != start_date:
        print(dataframe[-11:-6],start_date, dataframe[-11:-6] != start_date)
        if i > 0:
            print(i)
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

def get_president_data(dataframe):
    
    topics = dataframe["topics"]+dataframe["hashtags"]
    
    putin_list, zelensky_list = [], []
    
    if "putin" in topics:
        putin_list.append(dataframe["tweet_id"])
    if "Volodymyr Zelenskyy" in topics:
        zelensky_list.append(dataframe["tweet_id"])
        

    return putin_list, zelensky_list

#%%
dataframe = "03-08.pkl"
df = pd.read_pickle(f"{save_path_dates}/{dataframe}")  
get_president_data(dataframe)
# df.to_pickle(f"{save_path_dates}/{dataframe[:-9]}.pkl")
df
#%%

