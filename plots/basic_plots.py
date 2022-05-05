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

# %%
#COUNT LANGUAGE 
setup_plot()
fig, ax = plt.subplots(figsize=(15,10),dpi=400, constrained_layout = False)

N_points_lang = defaultdict(int)


#colors = sns.color_palette('pastel')[0:4]
relevant_langs = ["uk",'en',"ru","other"]
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

plt.title('Language distribution in Tweets', fontsize=20)
plt.savefig('pie_stock.png')
#plt.axis('equal')

# %%

#unique_users = []
russian_users = []
ukrainian_users = []
for index, user in enumerate(df['user_id'][df['lang'] == 'ru']):
    if user not in russian_users:
        russian_users.append(user)

for index, user in enumerate(df['user_id'][df['lang'] == 'uk']):
    if user not in ukrainian_users:
        ukrainian_users.append(user)

#%%
russian_and_ukrainian = [user for user in russian_users if user in ukrainian_users]
#only 355. Removing these from Russian users

for user in russian_and_ukrainian:
    russian_users.remove(user)

# %%
#assigning all of their tweets to Ukranian or Russian
for user in russian_users:
    df.loc[df['user_id'] == user, 'lang'] = 'ru'

for user in ukrainian_users:
    df.loc[df['user_id'] == user, 'lang'] = 'uk'

#%%
#saving
df.to_csv('lang_proxy.csv')

#%%
#loading
df = pd.read_csv('c:\\Users\\rune7\\Documents\\GitHub\\02467-final\\lang_proxy.csv')

#%%
setup_plot()
fig, ax = plt.subplots(figsize=(15,10),dpi=400, constrained_layout = False)
N_points_lang = defaultdict(int)

relevant_langs = ["uk",'en',"ru","other"]
cap_langs = ["Russian","Anglo Saxon","Ukrainian","Other nationalities"]


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
plt.title('Nationality distribution using language as proxy',weight = 'bold',fontsize =20)
plt.savefig('pie_lang_proxy.png')
# %%
### Plotting time of day distribution for each day ###

small = df[0:100000]

# %%


# %%
# %%


freqmatrix = np.zeros((31,24))

#Counting tweets for each hour of each day
for i in range(len(df['times'])):
    freqmatrix[int(df['times'][i].day),int(df['times'][i].hour)] += 1

#%%

#Sorting tweet frequencies to be chronological
chronological =[]
chronological.append(freqmatrix[27])
chronological.append(freqmatrix[28])
for i in range(19):
    chronological.append(freqmatrix[i+1])


#%%
def daterange(start_date, end_date):
    delta = datetime.timedelta(hours=1)
    while start_date < end_date:
        yield start_date
        start_date += delta


timedelta = []

start_date = datetime.datetime(2022, 2, 27, 7, 00)
end_date = datetime.datetime(2022, 3, 19, 00, 00)
for single_date in daterange(start_date, end_date):
    timedelta.append(single_date.strftime("%Y-%m-%d %H:%M"))

#%%
chron_flat = []
for day in chronological:
    for hour in day:
        if hour != 0: #all 0 elements are in beginning and end, this is therefore fine
            chron_flat.append(hour)

#%%
d = {'Time': timedelta,'Frequency': chron_flat}
df2 = pd.DataFrame(d)
df3 = pd.DataFrame({'Frequency': chron_flat}, index = pd.to_datetime(timedelta))


#%%
#myFmt = mdates.DateFormatter('%b #Y')
#
#fig, ax = plt.subplots(figsize=(15,5),dpi=400, constrained_layout = False)
#ax.plot(timedelta,chron_flat)
#ax.set_ylabel('Tweets pr. hour')
#ax.set_xlabel('Time')
#ax.xaxis.set_major_formatter(myFmt)

# %%
myFmt = mdates.DateFormatter('%b %d')
#%%
#df2.set_index('Time')
rolled = df3['Frequency'].rolling('6H').mean()

#%%
fig, ax = plt.subplots(figsize=(15,3),dpi=400, constrained_layout = False)
#ax.plot(df2.Time, df2.Frequency, label = 'Tweets pr. hour raw', ls = "--", alpha = 0.5)
#ax.plot(df2.Time,rolled.values, label = 'Tweets pr. hour rolled', color = "k")

ax.plot(df3.index, df2.Frequency, label = 'Tweets pr. hour raw', ls = "--", alpha = 0.5)
ax.plot(df3.index,rolled.values, label = 'Tweets pr. hour rolled', color = "k")



#n = 24  # Keeps every 24th label
plt.xticks(fontsize = 15)
#[l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i % n != 0]
ax.set_ylim([0,4000])
ax.legend(fontsize = 'xx-small')
ax.set_ylabel('Tweets pr. hour')
ax.set_xlabel('Date')
ax.set_title('Frequency of Tweets over time of day')
ax.xaxis.set_major_formatter(myFmt)

plt.savefig('tweetfreq.png')
# %%
