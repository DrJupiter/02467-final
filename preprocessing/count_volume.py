# %%
import numpy as np
import os
from count_dehydrated import dehydrated
import pandas as pd

# For code path
import sys
from pathlib import Path

# This is used to read files in the module properly when the Main.py script is run from an external location.
#code_path = Path(*Path(os.path.realpath(sys.argv[0])).parts[:-1])
code_path = Path(os.getcwd())

path = code_path.joinpath('./data/complete/')
dirs = [os.path.join(path,d) for d in os.listdir(path) if os.path.isdir(os.path.join(path,d))]

# REMOVE LATER, BUT RN WE ONLY LOOK AT THE FIRST 20 DAYS
# %%
dirs.sort(key = lambda x: x[-10:])
dirs = dirs[:20]

# %%

volume_count = {d[-10:]: [] for d in dirs}

for dir in dirs:
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir,f))] 
    
    for i,file in enumerate(files):
        ids = np.loadtxt(os.path.join(dir,file))
        volume_count[dir[-10:]].append(len(ids))

# %%
for key in volume_count.keys():
    volume_count[key] = sum(volume_count[key])

# %%


# %%

total = dehydrated(path)

# %%
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
import seaborn as sns

def setup_plot():
    mpl.rcParams['lines.linewidth'] = 1
    mpl.rcParams['font.family'] = 'Arial'

    
    sns.set_theme(style="white", palette='pastel', font = 'Arial', font_scale=1.5)

    #sns.set_theme(style="white", palette='pastel', font = 'Microsoft Sans Serif', font_scale=1)
    myFmt = mdates.DateFormatter('%b %d')    
    print("Plot settings applied")

setup_plot()

# %%
#Converting to dataframe in order to plot xaxis with dateformatting

df = pd.DataFrame.from_dict(volume_count, orient = 'index')
df.index = pd.to_datetime(df.index)

#%%
fig, ax = plt.subplots(figsize=(15,3),dpi=400, constrained_layout = False)
ax.plot(df.index,df.values, '-o', label = 'Tweets pr. day', ls = "--", alpha = 0.5)

plt.xticks(fontsize = 15)
ax.set_ylim(18e4,32e4)
ax.legend(fontsize = 'xx-small')
ax.set_ylabel('Tweets pr. day')
ax.set_xlabel('Date')
ax.set_title("Volume of tweets surrounding the Russia-Ukraine War")
ax.xaxis.set_major_formatter(myFmt)

plt.savefig('volumedaily.png')
# %%
