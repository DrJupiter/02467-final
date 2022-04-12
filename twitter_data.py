# %%
import yaml
import twarc
from twarc.expansions import EXPANSIONS, USER_FIELDS, TWEET_FIELDS, PLACE_FIELDS, LIST_FIELDS
import numpy as np

# %%
with open("./secret/keys.yaml", "r") as keyfile:
    keys = yaml.load(keyfile, yaml.FullLoader)

t = twarc.Twarc2(keys['ApiKey'], keys['ApiKeySecret'], keys['AccessToken'], keys['AccessTokenSecret'], bearer_token = keys['BearerToken'])

# %%
path = './data/dehydrated/2022-02-27_3.csv'
ids = np.loadtxt(path)
ids = ids.astype(int)

# %%

tweets = t.tweet_lookup(ids)

# %%
data = list(tweets)


# %%
import json 

# save data

with open('./data/0227.json', 'w') as f:
    json.dump(f, data) 

# %%
# load data again
with open('./data/0227.json','r') as f:
    data = json.load(f)


# load file and then for each id create a csv file

# %%

import os
path = './data/dehydrated'
dirs = [os.path.join(path,d) for d in os.listdir(path) if os.path.isdir(os.path.join(path,d))]


for dir in dirs:
    print(dir)
    dirname = os.path.dirname(dir)
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir,f))] 
    print(files)
    for file in files:
        ids = np.loadtxt(os.path.join(dir,file))
        ids = ids.astype(int)
        #tweets = t.tweet_lookup(ids)
        #data = list(tweets)
        #with open(f'./data/hydrated/{dirname}/{file}.json','r') as f:
        #    data = json.dump(data,f)

    

# %%
