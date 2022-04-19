#%%
import pandas as pd
import numpy as np
import json
import os
from collections import defaultdict
import re

# For code path
import sys
from pathlib import Path
#%%


code_path = Path(os.getcwd())
path = './data/hydrated/'

path = code_path.joinpath('data/hydrated')
#dirs = [os.path.join(path,d) for d in os.listdir(path) if os.path.isdir(os.path.join(path,d))]
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))] 
# %%
files.sort(key = lambda x: x[:10])

# %%
lang_days = defaultdict(lambda: defaultdict(int))
c = 0
for file in files:
    with open(path.joinpath(file),'r') as f:
        data = json.load(f)

        day = re.findall(f"[0-9-]+",file)[0]
        if day not in lang_days:
            lang_days[day] = defaultdict(int)
            print("added day",day)


        for i in range(len(data)):
            for j in range(len(data[i]["data"])):
                lang = data[i]["data"][j]["lang"]
                lang_days[day][lang] += 1

        # print(df.iloc[0]["data"][0]["context_annotations"])


#%%
days = list(lang_days.keys())

for day in days:
    N = sum(lang_days[day].values())
    lang_days[day]["other_p"] = 0
    lang_days[day][f"en_p"] = 0
    lang_days[day][f"uk_p"] = 0
    lang_days[day][f"ru_p"] = 0

    for lang in lang_days[day]:
        if lang != "en" and lang != "uk" and lang != "ru":
            lang_days[day]["other_p"] += lang_days[day][lang]/N
        else:
            lang_days[day][f"{lang}_p"] = lang_days[day][lang]/N



#%%

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(20,10),dpi=400)
plt.xticks(rotation=90,fontsize=15)
plt.yticks(fontsize=15)

colors = ["blue","red","green","purple"]
relevant_langs = ["en","uk","ru","other"]
relevant_langs_p = ["en_p","uk_p","ru_p","other_p"]

for i, lang in enumerate(relevant_langs_p):

    dat = [lang_days[day][lang] for day in days]

    ax.plot(days, dat, 'D-', color=colors[i], label = lang)



plt.title("daily language distribtion of Tweets",fontdict={'fontsize': 30})
plt.xlabel("day",fontdict={'fontsize': 30})
plt.ylabel("% of daily tweets",fontdict={'fontsize': 30})
plt.legend(prop={'size': 30}, loc='midlle right')

plt.show()

#%%
relevant_langs = ["en","uk","ru","other"]
N_points_lang = defaultdict(int)
for i, lang in enumerate(relevant_langs):

    N_lang = sum([lang_days[day][lang] for day in days])
    N_points_lang[lang] = N_lang

plt.pie(list(N_points_lang.values()),labels=list(N_points_lang), colors=colors, startangle=90, shadow=True,explode=(0.1, 0.1, 0.1, 0.1), autopct='%1.2f%%')

plt.title('Total langugae distribution')
plt.axis('equal')
plt.show()
# %%
