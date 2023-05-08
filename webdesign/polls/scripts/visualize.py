import matplotlib.pyplot as plt
import os
import time

plt.rcParams.update({'font.size': 16})

def dual_plot(pp_ts,cat_ts,bin_bounds):
    f = plt.figure(figsize=(20,8),facecolor='white')
    ax = plt.gca()
    ax2 = ax.twinx()
    pp_ts.plot(x='date',y='value',ax=ax,legend=False)
    cat_ts.apply(lambda x: int(x[1:])).astype(int).plot(ax=ax2,color='k')
    for b in bin_bounds:
        ax.axhline(b,color='#dbdbdb',ls='--')
    
    timestr = time.strftime("%Y%m%d-%H%M%S")
    name = timestr+'.png'
    save_path = os.getcwd() +'/media/figures/'+name 
    print(save_path)
    f.savefig(save_path)
    plt.close(f)  
    return name 