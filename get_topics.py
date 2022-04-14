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
path = code_path.joinpath('data/hydrated/data/dehydrated/')
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

for file in files[:2]:
    with open(path.joinpath(file),'r') as f:
        data = json.load(f)
    for q in range(len(data)):
        ref_tweets = data[q]['includes']['tweets']
        id_ref_tweets = {ref_tweets[i]['id']:ref_tweets[i] for i in range(len(ref_tweets))}
        for t in range(len(data[q]['data'])):
            # insert hastag function
            tweet= data[q]['data'][t]
            type = tweet['referenced_tweets'][0]['type']
            if type in ['retweeted', 'replied_to']:
                # get proper context annotations and text
                id = tweet['id']
                tweet = id_ref_tweets[id]
            else:
                # just continue as planned
                pass
            for dom in tweet['context_annotations']:
                topic = dom['entity']['name'] 
                topic_count[topic] += 1
            for hashtag in hashtags.findall(tweet['text']):
                topic_count[hashtag] += 1
            



    
# %%
