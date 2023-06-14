import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import os
import time

plt.rcParams.update({'font.size': 16})

def dual_plot(pp_ts,cat_ts,bin_bounds):     ##levels
    f = plt.figure(figsize=(20,8),facecolor='white')
    ax = plt.gca()
    ax2 = ax.twinx()
    pp_ts.plot(x='date',y='value',ax=ax,legend=False)
    cat_ts.apply(lambda x: int(x[1:])).astype(int).plot(ax=ax2,color='k')
    for b in bin_bounds:
        ax.axhline(b,color='#dbdbdb',ls='--')
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
    
    timestr = time.strftime("%Y%m%d-%H%M%S")
    name = timestr+'.png'
    save_path = os.getcwd() +'/media/figures/'+name 
    f.savefig(save_path)
    plt.close(f)  
    return name 

def triple_plot(pp_ts,trend_ts,cat_ts,bin_bounds):  ## trends
    f = plt.figure(figsize=(20,8),facecolor='white')
    ax = plt.gca()
    ax2 = ax.twinx()
    ax3 = ax.twinx()
    pp_ts.plot(x='date',y='value',ax=ax,legend=False)
    trend_ts.plot(x='date',y='value',ax=ax2,legend=False,linestyle='--')
    cat_ts.apply(lambda x: int(x[1:])).astype(int).plot(ax=ax3,color='k')
    for b in bin_bounds:
        ax2.axhline(b,color='#dbdbdb',ls='--')
    ax3.spines["right"].set_position(("axes", 1.1))
    ax3.yaxis.set_major_locator(MaxNLocator(integer=True))

    timestr = time.strftime("%Y%m%d-%H%M%S")
    name = timestr+'.png'
    save_path = os.getcwd() +'/media/figures/'+name 
    f.savefig(save_path)
    plt.close(f)  
    return name 