# %%
import numpy as np
import os
from count_dehydrated import dehydrated

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

total = dehydrated(path)

# %%
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(20,10),dpi=400)
plt.xticks(rotation=90,fontsize=15)
plt.yticks(fontsize=15)
ax.set_ylim(0*50e3,30e4)
ax.plot(*zip(*volume_count.items()), '-o', color='purple')
plt.title("Volume of tweets surrounding the Russia-Ukraine War",fontdict={'fontsize': 20})
# %%
