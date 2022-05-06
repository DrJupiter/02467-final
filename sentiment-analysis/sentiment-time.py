#%%
from re import I 
import matplotlib as mpl
import matplotlib.pylab as plt
import matplotlib.dates as mdates
import seaborn as sns

def setup_plot():
    mpl.rcParams['lines.linewidth'] = 1
    #mpl.rcParams['font.family'] = 'Microsoft Sans Serif'
    mpl.rcParams['font.family'] = 'Arial'

    
    #these don't work for some reason
    #mpl.rcParams['axes.titleweight'] = 'bold'
    #mpl.rcParams['axes.titlesize'] = '90'
    
    sns.set_theme(style="white", palette='pastel', font = 'Arial', font_scale=1.5)

    #sns.set_theme(style="white", palette='pastel', font = 'Microsoft Sans Serif', font_scale=1)
    #myFmt = mdates.DateFormatter('%b #Y')
    
    print("Plot settings applied")

# %%

import pandas as pd

path = '../data/dataframes/translated-text-ru-uk_sentiment.pkl'
df =pd.read_pickle(path)
# %%

df['date'] = pd.to_datetime(df['created_time'])
df.index = df['date']

# %%

# three

def get_lang(df, lang):
    return df[(df['lang'] == lang).to_numpy()]

def get_nationality(df, nationality):
    return df[(df['nationality'] == nationality).to_numpy()]

df_uk = get_nationality(df, 'uk') 
df_uk = get_nationality(df, 'uk') 
df_ru = get_lang(df, 'ru') 
df_ru = get_lang(df, 'ru') 
# %%

import numpy as np

def get_daily_sentiment(df, keys=[], dates = None):
    dates = dates if dates is not None else np.unique(np.vectorize(str)(df['date'].dt.date.values))

    # Will contain the cummulative sentiment of each of the keys for each day.
    daily_sentiment = {date: {} for date in dates}
    for date in dates:
        sentiment = {key: 0 for key in keys}
        key_count = {key: 0 for key in keys}
        try:
            date_df = df.loc[str(date)]
        except KeyError:
            date_df = None
            print(f"{date} was not found in dataset")
        if date_df is not None:
            for s in date_df['sentiment_dict'].iloc[:]:
                if s is not None:
                    for key in keys:
                        s_val = s.get(key)
                        if s_val is not None:
                            sentiment[key] += s_val['compound']
                            key_count[key] += 1
            for key in keys:
                sentiment[key] /= key_count[key]
        daily_sentiment[date] = sentiment
    return daily_sentiment

keys=['ukraine', 'russia','putin', 'zelenskyy']
daily_sentiment = get_daily_sentiment(df, keys=keys)                     
# %%

setup_plot()

def sentiment_plot(sentiment_dict, keys, title=None):
    fig, ax = plt.subplots(figsize=(22,10),dpi=400)
    plt.xticks(rotation=90,fontsize=15)
    plt.yticks(fontsize=15)
    x, sentiment_values = zip(*sentiment_dict.items())
    for key in keys:
        ax.plot(x, [s[key] for s in sentiment_values])

    ax.plot(x, np.zeros(len(x)), color='black', linestyle=(0,(5,15)))
    # Maybe not 0 line?
    ax.legend(labels=keys+['0 line'])
    plt.title('Sentiment values over time' if title is None else title)

    plt.show()
    plt.close()

sentiment_plot(daily_sentiment, keys)
# %%
sentiment_plot(get_daily_sentiment(df_uk, keys), keys)
sentiment_plot(get_daily_sentiment(df_ru, keys), keys)

# %%

def president_conversion(presidents):
    """
    0 -> No presidents
    1 -> putin
    2 -> zelenskyy
    3 -> putin and zelenskyy
    """
    return ('putin' in presidents) + ('zelenskyy' in presidents) * 2

    

# %%

df_user = pd.read_pickle('../data/dataframes/user_trans_senti_ru_uk.pkl')
df_user['overall_sentiment'] = df_user['overall_sentiement']
df_user['word_wise_sentiment'] = df_user['word_wise_sentiement']
# %%

def president_conversion(presidents):
    """
    0 -> No presidents
    1 -> putin
    2 -> zelenskyy
    3 -> putin and zelenskyy
    """
    return ('putin' in presidents) + ('zelenskyy' in presidents) * 2

def get_anti_war_score(df):
    anti_war_score = []
    for i in range(len(df)):
        user_data = df.iloc[i]
        score = 0
        count = 0
        for s in user_data['word_wise_sentiment']:
            if s is not None:
                score += s['ukraine']['compound'] + s['zelenskyy']['compound'] - (s['russia']['compound'] + s['putin']['compound'])
                count += 1
        score = score/count if count != 0 else None
        anti_war_score.append(score)
    return anti_war_score

def classify_anti_war_score(aws):
    """
    1 -> Russia Supporter
    2 -> Ukraine Supporter
    3 -> Neutral
    """
    return (aws < 0) + (aws > 0) * 2 + (aws == 0) * 3 if aws is not None else None


if 'anti-war' not in df_user.columns:
    anti_war_score = get_anti_war_score(df_user)
    df_user['anti-war'] = anti_war_score
    print('added anti war')
    df_user['anti-war-class'] = [classify_anti_war_score(aws) for aws in anti_war_score]

# %%
df_user.to_pickle('../data/dataframes/user_trans_senti_ru_uk.pkl')
# %%

df_user_uk = get_nationality(df_user, 'uk') 
df_user_ru = get_nationality(df_user, 'ru') 

# %%
df_user['date'] = pd.to_datetime(df_user['created_time'])
df_user.index = df_user['date']
                    
# %%

setup_plot()

def anti_war_score_plot(sentiment_dict, keys, title=None):
    fig, ax = plt.subplots(figsize=(22,10),dpi=400)
    plt.xticks(rotation=90,fontsize=15)
    plt.yticks(fontsize=15)
    x, sentiment_values = zip(*sentiment_dict.items())
    ax.plot(x, [(s['ukraine'] + s['zelenskyy'] - (s['russia'] + s['putin'])) for s in sentiment_values])

    ax.plot(x, np.zeros(len(x)), color='black', linestyle=(0,(5,15)))
    # Maybe not 0 line?
    #ax.legend(labels=['Russia Support','0 line'])
    #plt.title('Support for Russia over time' if title is None else title)
    ax.legend(labels=['Ukraine Support','0 line'])
    plt.title('Support for Ukraine over time' if title is None else title)
    plt.show()
    plt.close()

anti_war_score_plot(daily_sentiment, keys)
# %%
