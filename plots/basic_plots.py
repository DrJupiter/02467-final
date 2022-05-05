#%%
import pandas as pd
import os
import matplotlib as mpl
import matplotlib.pylab as plt
from collections import defaultdict
import seaborn as sns

from setup_plot import setup_plot
setup_plot()


#%%
os.chdir('c:\\Users\\rune7\\Documents\\GitHub\\02467-final\\data')

for i, pkl in enumerate(os.listdir()):
    if i == 0:
        df = pd.read_pickle(pkl)
    else:
        df2 = pd.read_pickle(pkl)
        df = pd.concat([df,df2])

#

# %%
len(df[df['lang']=='en'])
# %%

fig, ax = plt.subplots(figsize=(15,10),dpi=400, constrained_layout = False)

N_points_lang = defaultdict(int)


#colors = sns.color_palette('pastel')[0:4]
relevant_langs = ["uk",'en',"ru","other"]
relevant_langs_p = ["en_p","uk_p","ru_p","other_p"]
cap_langs = ["Russian","English","Ukrainian","Other languages"]


total = 0
for i, lang in enumerate(relevant_langs):

    if lang == 'other':
        dat = 1-total
    else:
        dat = len(df[df['lang']==lang])/len(df)
        total += dat
    N_points_lang[lang] = dat



ax.pie(list(N_points_lang.values()),labels=list(cap_langs), startangle=90, shadow=False,explode=(0.05, 0.05, 0.05, 0.05), autopct='%1.2f%%')
#ax.xticks(rotation=90,fontsize=15)
#ax.yticks(fontsize=15)
plt.title('Total language distribution',loc = 'center',)
#plt.axis('equal')

# %%
