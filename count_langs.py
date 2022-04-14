#%%
from xml.etree.ElementInclude import default_loader
import pandas as pd
import numpy as np
import json
import os
from collections import defaultdict
import re
#%%


path = './data/hydrated/data/dehydrated'

lang_days = defaultdict(lambda: defaultdict(int))

c = 0

for filename in os.listdir(path):
    # print("filenam",filename)
    f = os.path.join(path, filename)
    # checking if it is a file
    if os.path.isfile(f):
        with open(f,'r') as fi:
            data = json.load(fi)

        day = re.findall(f"[0-9-]+",f)[0]
        if day not in lang_days:
            lang_days[day] = defaultdict(int)
            print("added day",day)


        for i in range(len(data)):
            for j in range(len(data[i]["data"])):
                lang = data[i]["data"][j]["lang"]
                lang_days[day][lang] += 1

        # print(df.iloc[0]["data"][0]["context_annotations"])
    

#%%

lang_days["2022-03-12"]["uk"]


#%%
import matplotlib.pyplot

