import pandas as pd
import numpy as np

def level_categorize(ts, cat_method, num_bins):
    str_format = ':0{}d'.format(len(str(num_bins)))

    if cat_method=='L-cut':
        cat_ts = pd.cut(ts.set_index('date')['value'], num_bins,
               labels=[('C{'+str_format+'}').format(i+1) for i in range(num_bins)],
               retbins=True)
        
    if cat_method=='L-qcut':
        cat_ts = pd.qcut(ts.set_index('date')['value'], num_bins,
               labels=[('Q{'+str_format+'}').format(i+1) for i in range(num_bins)],
               retbins=True) 
    return cat_ts

def trend_categorize(ts, cat_method, win_size, num_bins):
    str_format = ':0{}d'.format(len(str(num_bins)))

    trend_ts = ts.set_index('date').diff(periods=win_size).shift(-win_size).dropna()['value']
    if cat_method=='T-percent':
        trend_ts = trend_ts.divide(ts.set_index('date').loc[trend_ts.index]['value'])*100
        
    range_bound = np.maximum(np.abs(trend_ts.min()),trend_ts.max())  
    if cat_method=='T-rate':
        cat_ts = pd.cut(trend_ts,bins=np.linspace(-range_bound,range_bound,num_bins+1),labels=[('R{'+str_format+'}').format(i+1) for i in range(num_bins)],
               retbins=True)
        
    if cat_method=='T-percent':        
        cat_ts = pd.cut(trend_ts,bins=np.linspace(-range_bound,range_bound,num_bins+1),labels=[('P{'+str_format+'}').format(i+1) for i in range(num_bins)],
               retbins=True)
    
    return trend_ts, cat_ts
