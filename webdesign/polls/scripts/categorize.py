import pandas as pd
import numpy as np

def trunc_x(x,custom_range):
    if x > custom_range[1]:
        return custom_range[1]
    elif x < custom_range[0]:
        return custom_range[0]
    else:
        return x

def level_categorize(ts,cat_method,num_bins,custom_range=None):
    str_format = ':0{}d'.format(len(str(num_bins)))
    
    if custom_range:
        trunc_ts = ts.set_index('date')['value'].apply(lambda x: trunc_x(x,custom_range))
    else:
        trunc_ts = ts.set_index('date')['value']
        
    if cat_method=='L-cut':
        if custom_range:
            cat_ts = pd.cut(trunc_ts, np.linspace(custom_range[0],custom_range[1],num_bins+1),
                   labels=[('C{'+str_format+'}').format(i+1) for i in range(num_bins)], include_lowest=True,
                   retbins=True)
        else:
            cat_ts = pd.cut(trunc_ts, num_bins,
                   labels=[('C{'+str_format+'}').format(i+1) for i in range(num_bins)], include_lowest=True,
                   retbins=True)

    if cat_method=='L-qcut':
        cat_ts = pd.qcut(trunc_ts, num_bins,
               labels=[('Q{'+str_format+'}').format(i+1) for i in range(num_bins)],
               retbins=True) 
    return cat_ts

def trend_categorize(ts,cat_method,win_size,num_bins,custom_range=None):
    str_format = ':0{}d'.format(len(str(num_bins)))

    trend_ts = ts.set_index('date').diff(periods=win_size).shift(-win_size).dropna()['value']
    if cat_method=='T-percent':
        trend_ts = trend_ts.divide(ts.set_index('date').loc[trend_ts.index]['value'])*100
        
    if custom_range:
        trunc_ts = trend_ts.apply(lambda x: trunc_x(x,custom_range))
    else:
        trunc_ts = trend_ts
        
    range_bound = np.maximum(np.abs(trunc_ts.min()),trunc_ts.max())
    
    if custom_range:
        range_tuple = custom_range
    else:
        range_tuple = (-range_bound,range_bound)
        
    if cat_method=='T-rate':
        cat_ts = pd.cut(trunc_ts,bins=np.linspace(range_tuple[0],range_tuple[1],num_bins+1),
                        labels=[('R{'+str_format+'}').format(i+1) for i in range(num_bins)], include_lowest=True,
                        retbins=True)
        
    if cat_method=='T-percent':        
        cat_ts = pd.cut(trunc_ts,bins=np.linspace(range_tuple[0],range_tuple[1],num_bins+1),
                        labels=[('P{'+str_format+'}').format(i+1) for i in range(num_bins)], include_lowest=True,
                        retbins=True)
    
    return trend_ts, cat_ts
