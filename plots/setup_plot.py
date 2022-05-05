#%%
import matplotlib as mpl
import matplotlib.pylab as plt
import matplotlib.dates as mdates
import seaborn as sns

def setup_plot():
    mpl.rcParams['lines.linewidth'] = 1
    mpl.rcParams['font.family'] = 'Microsoft Sans Serif'
    
    #these don't work for some reason
    #mpl.rcParams['axes.titleweight'] = 'bold'
    #mpl.rcParams['axes.titlesize'] = '90'
    
    
    sns.set_theme(style="white", palette='pastel', font = 'Microsoft Sans Serif', font_scale=2)
    myFmt = mdates.DateFormatter('%b #Y')
    
    print("Plot settings applied")



setup_plot()
# %%
