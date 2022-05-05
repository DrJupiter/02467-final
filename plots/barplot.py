#%%
import pandas as pd
import os
import matplotlib as mpl
import matplotlib.pylab as plt
from collections import defaultdict
import seaborn as sns

import dateutil.parser
import datetime as datetime
import numpy as np
import matplotlib.dates as mdates
import matplotlib.ticker as mtick


from setup_plot import setup_plot
setup_plot()

# %%
#dict = {"VK": 0.73, "Youtube":0.68,"Instagram":0.59,"Odnoklassniki":0.42,"Facebook":0.37,"TikTok":0.35,"Twitter":0.14,"Moy Mir":0.13}
#df = pd.DataFrame.from_dict(dict, orient ="index")

d ={'Platforms':["VK","Youtube","Instagram","Odnoklassniki","Facebook","TikTok","Twitter","Moy Mir"],"Userbase":[0.73,0.68,0.59,0.42,0.37,0.35,0.14,0.13]}
df = pd.DataFrame(data = d)
#%%
platforms = df['Platforms']
userbase = df['Userbase']
colors = sns.color_palette("pastel")

#%%
#platforms = list(dict.keys())
#data = list(dict.values())
#xaxis = np.arange(len(df.values))


#yaxis = np.array([0.73,0.68,0.59,0.42,0.37,0.35,0.14,0.13])
#xaxis = np.arange(len(df.values))


#percent_str = [str(int(p*100))+"%" for p in data]
# %%

fig, ax = plt.subplots(figsize=(16,9))

ax.barh(platforms,userbase, color = colors)
ax.invert_yaxis()

for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)

ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')

plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) 


for i in ax.patches:
    plt.text(i.get_width()+0.01, i.get_y()+0.5,
             str(round((i.get_width()), 2)),
             fontsize = 15, fontweight ='bold',
             color ='grey')

ax.set_title('Proliferation of Social media platforms in Russia')

ax.text(0.75, 0.15, 'Source: statisa.com',
        transform = ax.transAxes, fontsize = 15)

plt.savefig("socailmedia.png")

# %%
