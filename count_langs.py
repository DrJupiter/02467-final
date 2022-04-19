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
days = list(lang_days.keys())


for day in days:
    N = sum(lang_days[day].values())
    lang_days[day]["other"] = 0
    lang_days[day]["other_p"] = 0
    lang_days[day][f"en_p"] = 0
    lang_days[day][f"uk_p"] = 0
    lang_days[day][f"ru_p"] = 0

    for lang in lang_days[day]:
        if lang != "en" and lang != "uk" and lang != "ru":
            lang_days[day]["other"] += lang_days[day][lang]
            lang_days[day]["other_p"] += lang_days[day][lang]/N
        else:
            lang_days[day][f"{lang}_p"] = lang_days[day][lang]/N

#%%
lang_days["2022-03-12"]["en_p"]

# %%

# x = r"#[\w]+"
# y = r"#[^#\s.,;:'`]+"

# test_string = ["#ged","#ged#fisk", "#ged1fisk", "#ged2.fisk", "#ged3? fisk", "#asjdkl#asjdklsiiee ;3 #sdokpwekr3pwoe"]

# for te in test_string:
#     print(re.findall(y,te))


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
plt.legend(prop={'size': 30})

plt.show()

#%%
relevant_langs = ["ru","en","uk","other"]
cap_langs = ["Russian","English","Ukrainian","Other languages"]
N_points_lang = defaultdict(int)
for i, lang in enumerate(relevant_langs):

    N_lang = sum([lang_days[day][lang] for day in days])
    print(N_lang)
    N_points_lang[lang] = N_lang

plt.pie(list(N_points_lang.values()),labels=list(cap_langs), colors=colors, startangle=90, shadow=True,explode=(0.1, 0.1, 0.1, 0.1), autopct='%1.2f%%')

plt.title('Total language distribution')
plt.axis('equal')
plt.show()
# %%

sum([lang_days[day]["other_p"] for day in days])