import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import MaxNLocator
import os
from datetime import datetime
matplotlib.use('agg')
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm

plt.style.use('fast')
plt.rcParams.update({'font.size': 16, 'font.family': 'sans-serif','font.sans-serif':'Verdana'})

def multi_signal_plot(cat_df, cat_method):
    label = [x[0] for x in cat_df.values.flatten()][0]
    
    f,ax = plt.subplots(figsize=(20,8),facecolor='white')
    if cat_method[0]=='categorizetypelevel':
        cat_label = 'Level-based'
    else:
        cat_label = 'Trend-based'
    plt.title('Multi signal - {} categories'.format(cat_label))
    plt.ylabel('Categorical time series ({})'.format(label))
    
    cat_df.applymap(lambda x: int(x[1:])).plot(ax=ax,lw=2,drawstyle='steps')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    timestr = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    name = timestr+'.png'
    save_path = os.getcwd() +'/media/figures/'+name 
    f.savefig(save_path)
    plt.close(f)  
    return name 

def single_ts_level_plot(pp_ts,cat_ts,bin_bounds, title=None):  ## use for levels
    label = cat_ts.values[0][0]
    
    f,ax = plt.subplots(figsize=(20,8),facecolor='white')
    if title:
        plt.title(title+' - Level-based categories',fontsize=20)
    else:
        plt.title('Single time series - Level-based categories',fontsize=20)
    ax = plt.gca()
    
    pp_ts.plot(x='date',y='value',ax=ax,label='Preprocessed time series',color='C0',legend=False)
    for b in bin_bounds:
        ax.axhline(b,color='C0',alpha=0.3,ls='--')
    ax.spines['left'].set_color('C0') 
    ax.tick_params(axis='y', colors='C0')
    ax.set_ylabel('Time series values',color='C0')

    ax2 = ax.twinx()
    cat_ts.apply(lambda x: int(x[1:])).astype(int).plot(ax=ax2,color='k',lw=2,drawstyle='steps',label='Categorical time series')
    ax2.spines['left'].set_color('C0')
    ax2.spines['right'].set_linewidth(2)
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax2.set_ylabel('Categorical time series ({})'.format(label))
    
    # First get the handles and labels from the axes
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    # Add the first legend to the second axis so it displaysys 'on top'
    first_legend = plt.legend(handles1, labels1, loc=2,labelcolor='linecolor')
    ax2.add_artist(first_legend)

    # Add the second legend as usual
    ax2.legend(handles2, labels2,loc=1)
    timestr = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    name = timestr+'.png'
    save_path = os.getcwd() +'/media/figures/'+name 
    f.savefig(save_path)
    plt.close(f)  
    return name 


def single_ts_trend_plot(pp_ts,trend_ts,cat_ts,bin_bounds, title=None):  ## use for trends  
    label = cat_ts.values[0][0]
    
    f,ax = plt.subplots(figsize=(20,8),facecolor='white')
    if title:
        plt.title(title+' - Level-based categories',fontsize=20)
    else:
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
    cat_ts.apply(lambda x: int(x[1:])).astype(int).plot(ax=ax3,color='k',lw=2,drawstyle='steps',label='Categorical time series')
    ax3.spines["right"].set_position(("axes", 1.1))
    ax3.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax3.spines['right'].set_linewidth(2)
    ax3.set_ylabel('Categorical time series ({})'.format(label),color='k')
    
    
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

    timestr = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    name = timestr+'.png'
    save_path = os.getcwd() +'/media/figures/'+name 
    f.savefig(save_path)
    plt.close(f)  
    return name 

def multi_signal_plot_nosave(cat_df, cat_method):
    label = [x[0] for x in cat_df.values.flatten()][0]
    
    f,ax = plt.subplots(figsize=(20,8),facecolor='white')
    if cat_method[0]=='categorizetypelevel':
        cat_label = 'Level-based'
    else:
        cat_label = 'Trend-based'
    plt.title('Multi signal - {} categories'.format(cat_label))
    plt.ylabel('Categorical time series ({})'.format(label))
    
    cat_df.applymap(lambda x: int(x[1:])).plot(ax=ax,lw=2,drawstyle='steps')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

def single_ts_level_plot_nosave(pp_ts,cat_ts,bin_bounds,title=None):  ## use for levels
    label = cat_ts.values[0][0]
    f,ax = plt.subplots(figsize=(20,8),facecolor='white')
    if title:
        plt.title(title+' - Level-based categories',fontsize=20)
    else:
        plt.title('Single time series - Level-based categories',fontsize=20)
        
    ax = plt.gca()
    
    pp_ts.plot(x='date',y='value',ax=ax,label='Preprocessed time series',color='C0',legend=False)
    for b in bin_bounds:
        ax.axhline(b,color='C0',alpha=0.3,ls='--')
    ax.spines['left'].set_color('C0') 
    ax.tick_params(axis='y', colors='C0')
    ax.set_ylabel('Time series values',color='C0')

    ax2 = ax.twinx()
    cat_ts.apply(lambda x: int(x[1:])).astype(int).plot(ax=ax2,drawstyle='steps',color='k',lw=2,label='Categorical time series')
    ax2.spines['left'].set_color('C0')
    ax2.spines['right'].set_linewidth(2)
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax2.set_ylabel('Categorical time series ({})'.format(label))
    
    # First get the handles and labels from the axes
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    # Add the first legend to the second axis so it displaysys 'on top'
    first_legend = plt.legend(handles1, labels1, loc=2,labelcolor='linecolor')
    ax2.add_artist(first_legend)

    # Add the second legend as usual
    ax2.legend(handles2, labels2,loc=1)

def single_ts_trend_plot_nosave(pp_ts,trend_ts,cat_ts,bin_bounds,title=None):  ## use for trends  
    label = cat_ts.values[0][0]
    
    f,ax = plt.subplots(figsize=(20,8),facecolor='white')
    if title:
        plt.title(title+' - Level-based categories',fontsize=20)
    else:
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
    cat_ts.apply(lambda x: int(x[1:])).astype(int).plot(ax=ax3,drawstyle='steps',color='k',lw=2,label='Categorical time series')
    ax3.spines["right"].set_position(("axes", 1.1))
    ax3.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax3.spines['right'].set_linewidth(2)
    ax3.set_ylabel('Categorical time series ({})'.format(label),color='k')
    
    
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
    
def multi_cat_csq(chi_df,csq_str_df):
    f = plt.figure(figsize=(20,8),facecolor='white')
    ax = plt.gca()
    mask = np.triu(np.ones_like(chi_df))
    sns.heatmap(chi_df,annot=csq_str_df,mask=mask,fmt='s',cmap=cm.inferno)
    
    plt.title('Pairwise chi-squared values',fontsize=20)
    timestr = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    name = timestr+'.png'
    save_path = os.getcwd() +'/media/figures/'+name 
    f.savefig(save_path,bbox_inches='tight')
    #plt.close(f)  
    return name 

def fcast_plot(input_ts,qfct):
    f = plt.figure(figsize=(20,8),facecolor='white')
    ax = plt.gca()
    
    input_ts.plot(x='date',y='value',ax=ax,label='input time series')
    qfct_noqnt = qfct.drop_duplicates(['target_end_date'])
    qfct_noqnt.plot(x='target_end_date',y='point',ax=ax,marker='o',markersize=8,ls='--',color='C3',label='median forecast')
    ax.fill_between(qfct_noqnt['target_end_date'].values,qfct_noqnt['fct_lb'].values,qfct_noqnt['fct_ub'].values,color='C3',alpha=0.20)
    
    plt.title('Short-term forecasts',fontsize=20)
    plt.ylabel('Time series values')
    plt.xlabel('date')
    
    timestr = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    name = timestr+'.png'
    save_path = os.getcwd() +'/media/figures/'+name 
    f.savefig(save_path,bbox_inches='tight')
    #plt.close(f)  
    return name

def cat_fcast_plot(cat_fct):
    cat_fct_pvt = cat_fct.pivot(index='output_type_id',columns='target_end_date',values='value')
    cat_fct_pvt.columns = [x.date().isoformat() for x in cat_fct_pvt.columns]
    cat_fct_pvt*=100
    cat_fct_pvt = cat_fct_pvt.iloc[::-1]

    f = plt.figure(figsize=(20,8),facecolor='white')
    ax = plt.gca()
    
    sns.heatmap(cat_fct_pvt,annot=True,fmt='.01f',vmin=0,vmax=100,ax=ax)
    ax = plt.gca()
    for t in ax.texts: t.set_text(t.get_text() + " %")
    plt.title('Short-term categorical forecasts',fontsize=20)
    plt.ylabel('Category')
    plt.xlabel('Forecast date')
    
    timestr = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    name = timestr+'.png'
    save_path = os.getcwd() +'/media/figures/'+name 
    f.savefig(save_path,bbox_inches='tight')
    #plt.close(f)  
    return name