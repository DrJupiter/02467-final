# %%
import numpy as np
import os
import json

# For code path
import sys
from pathlib import Path

# This is used to read files in the module properly when the Main.py script is run from an external location.
#code_path = Path(*Path(os.path.realpath(sys.argv[0])).parts[:-1])
code_path = Path(os.getcwd())

# %%
path = code_path.joinpath('data/hydrated')
#dirs = [os.path.join(path,d) for d in os.listdir(path) if os.path.isdir(os.path.join(path,d))]
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))] 
# %%
files.sort(key = lambda x: x[:10])

# %%
import re

hashtags = r"#[^#\s.,;:'`]+"
hashtags = re.compile(hashtags)
#for te in test_string:
#    print(hashtags.findall(y,te))

# %%
from collections import defaultdict

topic_count = defaultdict(lambda: 0)
no_context = 0
none_type = 0
for file in files[:2]:
    with open(path.joinpath(file),'r') as f:
        data = json.load(f)
    for q in range(len(data)):
        ref_tweets = data[q]['includes']['tweets']
        id_ref_tweets = {ref_tweets[i]['id']:ref_tweets[i] for i in range(len(ref_tweets))}
        for t in range(len(data[q]['data'])):
            # insert hastag function
            tweet= data[q]['data'][t]
            
            type = tweet.get('referenced_tweets')
            if type is None:
                none_type += 1
            if type in ['retweeted', 'replied_to']:
                # get proper context annotations and text
                print(type)
                id = tweet['referenced_tweets'][0]['id']
                # entities
                #id = tweet['id']
                _tweet = id_ref_tweets.get(id)
                if _tweet is not None:
                    tweet = _tweet
                else:
                    if tweet.get('context_annotations') is not None:
                        pass
                    else:
                        for hashtag in hashtags.findall(tweet['text']):
                            topic_count[hashtag] += 1
                        continue
            else:
                # just continue as planned
                pass
            domains = tweet.get('context_annotations')
            if domains is None:
                no_context += 1
            else:
                for dom in tweet['context_annotations']:
                    topic = dom['entity']['name'] 
                    topic_count[topic] += 1
            for hashtag in hashtags.findall(tweet['text']):
                topic_count[hashtag] += 1
            



    
# %%
import matplotlib.pyplot as plt

# topic_count = {"fisk":15, "gaffel": 22, "ost": 69,"cola": 4}

fig, ax = plt.subplots(figsize=(15,7),dpi=400)
plt.xticks(rotation=45,fontsize=15)
plt.yticks(fontsize=15)

ax.bar(list(topic_count),list(topic_count.values()))

plt.title("Topic occurrences",fontdict={'fontsize': 20})
plt.xlabel("topic",fontdict={'fontsize': 20})
plt.ylabel("Number of occurrences (links)",fontdict={'fontsize': 20})

plt.show()
# %%

