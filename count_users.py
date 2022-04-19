#%%

import pandas as pd
import numpy as np
import json
import os
from collections import defaultdict
import re

from sklearn.preprocessing import scale
#%%

path = './data/hydrated/data/dehydrated'

uset_tweet_count = defaultdict(int)

for filename in os.listdir(path):
    # print("filenam",filename)
    f = os.path.join(path, filename)
    # checking if it is a file
    if os.path.isfile(f):
        with open(f,'r') as fi:
            data = json.load(fi)

        for i in range(len(data)):
            for j in range(len(data[i]["data"])):
                user = data[i]["data"][j]["author_id"]
                uset_tweet_count[user] += 1


#%%
print(len(uset_tweet_count))
uset_tweet_count

#%%

tweet_count_count = defaultdict(int)

for x in uset_tweet_count.values():
    tweet_count_count[x] += 1

tweet_count_count

#%%

import matplotlib.pyplot as plt

# topic_count = {"fisk":15, "gaffel": 22, "ost": 69,"cola": 4}

fig, ax = plt.subplots(figsize=(15,7),dpi=400)
plt.xticks(rotation=45,fontsize=15)
plt.yticks(fontsize=15)

ax.bar(list(tweet_count_count),list(tweet_count_count.values()))

plt.yscale("log")

plt.title("Users tweet count",fontdict={'fontsize': 20})
plt.xlabel("Tweet count",fontdict={'fontsize': 20})
plt.ylabel("Number of users (log scale)",fontdict={'fontsize': 20})

plt.show()

#%%
tweet_count_count[120]