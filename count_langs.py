#%%
import pandas as pd
import numpy as np
import json
import os

#%%
with open('./data/0227.json','r') as f:
    data = json.load(f)

path = './data/hydrated/data/dehydrated'

# dirs = [os.path.join(path,d) for d in os.listdir(path) if os.path.isdir(os.path.join(path,d))]

# dirs
for filename in os.listdir(path):
    f = os.path.join(path, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print(f)