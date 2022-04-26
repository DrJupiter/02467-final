#%%
import pandas as pd

df = pd.DataFrame(columns=["ged","fisk","alder"])

df
#%%

df.at[1,["ged","fisk"]] = 2
df.at[2,["alder","fisk"]] = 42

df
#%%