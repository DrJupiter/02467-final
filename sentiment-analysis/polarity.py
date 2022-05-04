# %%

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from googletrans import Translator

# %%

translator = Translator()
analyzer = SentimentIntensityAnalyzer()
#%%
df = pd.read_pickle('/home/klaus/Desktop/DTU Semester 4/DTU-SocialScience/02467-final/data/dataframes/02-27.pkl')
# %%
en_idx = (df['lang'] == 'en').to_numpy()
en_df = df.iloc[en_idx]
# %%

sentiment = analyzer.polarity_scores(en_df['text'][0])

# %% find translation
# pip install googletrans==4.0.0rc1  

translator.translate('안녕하세요.')
# <Translated src=ko dest=en text=Good evening. pronunciation=Good evening.>
translator.translate('안녕하세요.', dest='ja')
# <Translated src=ko dest=ja text=こんにちは。 pronunciation=Kon'nichiwa.>
translator.translate('veritas lux mea', src='la')
# <Translated src=la dest=en text=The truth is my light pronunciation=The truth is my light>

# %% context annotations? sentence structure
und_df = df.iloc[(df['lang'] == 'und').to_numpy()]
analyzer.polarity_scores(und_df['text'][-1])

"""
#StandWithUkraine https://t.co/H0mKKZVHni ->{'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}

find a way to break up hashtags
"""

# %%
