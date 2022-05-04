#%%
import matplotlib as mpl
import matplotlib.pylab as plt
import matplotlib.dates as mdates
import seaborn as sns

def setup_plot():
    mpl.rcParams['lines.linewidth'] = 1
    mpl.rcParams['font.family'] = 'Microsoft Sans Serif'
    mpl.rcParams['axes.titleweight'] = 'bold'
    
    sns.set_theme(style="white", palette='pastel', font = 'Microsoft Sans Serif', font_scale=3)
    myFmt = mdates.DateFormatter('%b #Y')
    
    print("Plot settings applied")



setup_plot()
# %%
