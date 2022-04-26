# %%
from html import entities
import numpy as np
import os
import json
import pandas as pd

from collections import defaultdict


# For code path
import sys
from pathlib import Path

# This is used to read files in the module properly when the Main.py script is run from an external location.
#code_path = Path(*Path(os.path.realpath(sys.argv[0])).parts[:-1])
code_path = Path(os.getcwd())

##%%


path = code_path.joinpath('./../data/hydrated')
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

our_hashtags = defaultdict(int)
twit_hashtags = defaultdict(int)

# loop over files in path
for file in files:

    # Create new dataframe
    df = pd.DataFrame(columns=[
        "id",
        "author_id",
        "lang",
        "text",
        "created_time",
        "hashtags",
        "topics",
        "tweet_type",
        "parent_id",
        "mentions"
        ])

    # load data
    with open(path.joinpath(file),'r') as f:
        data = json.load(f)

    # loop over tweetsets in file
    for q,tweetset in enumerate(data):

        # get list of ref tweets
        ref_tweets = tweetset['includes'].get('tweets')  # Get retuns None, if the index isnt avail

        # get ref ids
        ref_tweet_ids = {ref_tweets[i]['id']:ref_tweets[i] for i in range(len(ref_tweets))} if ref_tweets is not None else None 

        # Get all normal tweet data
        tweets = tweetset['data']

        # loop over tweets in tweetset
        for t,tweet in enumerate(tweets):
            # tweet_id = tweet.get("id")
            # tweet_text = tweet.get("text")
            # tweet_time_created = tweet.get("created_at")
            

            # Get tweet type
            type_data = tweet.get('referenced_tweets')

            if type_data is not None:
                type = type_data[0]['type']

                # # Special if not original tweet
                if type in ['retweeted', 'replied_to']:

                    # get proper context annotations, text and id
                    if ref_tweets is not None:

                        # get real id
                        id = type_data[0]['id']
                        _tweet = ref_tweet_ids.get(id)

                        if _tweet is not None:
                            tweet = _tweet

                        # else:
                        #     if tweet.get('context_annotations') is None:
                        #         tweet_text = tweet['text']
                        #         for hashtag in hashtags.findall(tweet_text):
                        #             # Hashtags
                        #             None
                        #         continue
                            
                            
            domains = tweet.get('context_annotations')
            if domains is None:
                None
                # no_context += 1
            else:

                topics = [dom['entity']['name'] for dom in tweet['context_annotations']]
                topics = set(topics)
                for topic in topics:
                    None
                    # topic_count[topic] += 1
                    # Adds topic to dataframe

            tweet_entities = tweet.get("entities")
            if tweet_entities is not None:
                hashtags_ = tweet_entities.get("annotations")
                mentions_ = tweet_entities.get("mentions")

                if hashtags_ is not None:
                    for hashtag in hashtags_:
                        tag = hashtag["normalized_text"]
                        twit_hashtags[tag] += 1
                        
                if mentions_ is not None:
                    for mention in mentions_:
                        mention_name = mention["username"]
                        mention_id = mention["id"]

            
            # hashtags = hashtags_re.findall(tweet['text'])
            # for hashtag in hashtags:
            #     our_hashtags[hashtag] += 1
            #     # topic_count[hashtag] += 1
            #     # Adds topic to dataframe


        #     if t == 5:
        #         break
        # break
#%%
sum([val for val in our_hashtags.values()])

#%%
sum([val for val in twit_hashtags.values()])





# %%
import matplotlib.pyplot as plt

topic_count_list = list(zip(topic_count,topic_count.values()))
topic_count_list.sort(reverse=True, key = lambda x: x[1])
names = [x[0] for x in topic_count_list]
counts = [x[1] for x in topic_count_list]
n = 10

fig, ax = plt.subplots(figsize=(15,7),dpi=400)
plt.xticks(rotation=90,fontsize=15)
plt.yticks(fontsize=15)

import seaborn as sns

sns.barplot(names[:n], counts[:n], palette='Blues_d')
#ax.bar(names[:n], counts[:n])

plt.title("Topic occurrences",fontdict={'fontsize': 20})
plt.xlabel("Topic",fontdict={'fontsize': 20})
plt.ylabel("Number of occurrences (links)",fontdict={'fontsize': 20})

plt.show()
# %%