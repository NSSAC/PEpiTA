import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import os
import time

plt.style.use('fast')
plt.rcParams.update({'font.size': 16, 'font.family': 'sans-serif','font.sans-serif':'Verdana'})

def single_ts_level_plot(pp_ts,cat_ts,bin_bounds):  ## use for trends
    f,ax = plt.subplots(figsize=(20,8),facecolor='white')
    plt.title('Single time series - Level-based categories',fontsize=20)
    ax = plt.gca()
    
    pp_ts.plot(x='date',y='value',ax=ax,label='Preprocessed time series',color='C0',legend=False)
    for b in bin_bounds:
        ax.axhline(b,color='C0',alpha=0.3,ls='--')
    ax.spines['left'].set_color('C0') 
    ax.tick_params(axis='y', colors='C0')
    ax.set_ylabel('Time series values',color='C0')

    ax2 = ax.twinx()
    cat_ts.apply(lambda x: int(x[1:])).astype(int).plot(ax=ax2,color='k',label='Categorical time series')
    ax2.spines['left'].set_color('C0')
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax2.set_ylabel('Categorical time series')

    # First get the handles and labels from the axes
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    # Add the first legend to the second axis so it displaysys 'on top'
    first_legend = plt.legend(handles1, labels1, loc=2,labelcolor='linecolor')
    ax2.add_artist(first_legend)

    # Add the second legend as usual
    ax2.legend(handles2, labels2,loc=1)

    timestr = time.strftime("%Y%m%d-%H%M%S")
    name = timestr+'.png'
    save_path = os.getcwd() +'/media/figures/'+name 
    f.savefig(save_path)
    plt.close(f)  
    return name 


def single_ts_trend_plot(pp_ts,trend_ts,cat_ts,bin_bounds):  ## use for trends
    f,ax = plt.subplots(figsize=(20,8),facecolor='white')
    plt.title('Single time series - Trend-based categories',fontsize=20)
    
    ax = plt.gca()
    pp_ts.plot(x='date',y='value',ax=ax,label='Preprocessed time series',color='C0',legend=False)
    ax.spines['left'].set_color('C0') 
    ax.tick_params(axis='y', colors='C0')
    ax.set_ylabel('Time series values',color='C0')
    
    
    ax2 = ax.twinx()
    trend_ts.plot(x='date',y='value',ax=ax2,label='Trend time series',color='C1',legend=False)
    for b in bin_bounds:
        ax2.axhline(b,color='C1',alpha=0.3,ls='--')
    ax2.spines['right'].set_color('C1')
    ax2.tick_params(axis='y', colors='C1')
    ax2.set_ylabel('Trend time series',color='C1')
    
    ax3 = ax.twinx()
    cat_ts.apply(lambda x: int(x[1:])).astype(int).plot(ax=ax3,color='k',label='Categorical time series')
    ax3.spines["right"].set_position(("axes", 1.1))
    ax3.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax3.spines['right'].set_color('k')
    ax3.set_ylabel('Categorical time series',color='k')
    
    
    # First get the handles and labels from the axes
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles3, labels3 = ax3.get_legend_handles_labels()

    # Add the first and second legends to the third axis so it displaysys 'on top'
    first_legend = plt.legend(handles1, labels1, loc=2,labelcolor='linecolor')
    second_legend = plt.legend(handles2, labels2, loc=4,labelcolor='linecolor')
    ax3.add_artist(first_legend)
    ax3.add_artist(second_legend)
    
    # Add the second legend as usual
    ax3.legend(handles3, labels3,loc=1)

    timestr = time.strftime("%Y%m%d-%H%M%S")
    name = timestr+'.png'
    save_path = os.getcwd() +'/media/figures/'+name 
    f.savefig(save_path)
    plt.close(f)  
    return name 


def triplePlot(pp_ts,trend_ts,cat_ts,bin_bounds):  ## trends
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

def dualPlot(pp_ts,cat_ts,bin_bounds):     ##levels
    f = plt.figure(figsize=(20,8),facecolor='white')
    ax = plt.gca()
    ax2 = ax.twinx()
    pp_ts.plot(x='date',y='value',ax=ax,legend=False)
    cat_ts.apply(lambda x: int(x[1:])).astype(int).plot(ax=ax2,color='k')
    for b in bin_bounds:
        ax.axhline(b,color='#dbdbdb',ls='--')
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))