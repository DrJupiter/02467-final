#%%
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

if __name__ == "__main__":

    setup_plot()
#SEE available fonts
    import matplotlib.font_manager
    from IPython.core.display import HTML

    def make_html(fontname):
        return "<p>{font}: <span style='font-family:{font}; font-size: 24px;'>{font}</p>".format(font=fontname)

    code = "\n".join([make_html(font) for font in sorted(set([f.name for f in matplotlib.font_manager.fontManager.ttflist]))])


    HTML("<div style='column-count: 2;'>{}</div>".format(code))
# %%
