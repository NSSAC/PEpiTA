import pandas as pd

def level_categorize(ts,cat_method,num_bins):
    if cat_method=='L-cut':
        cat_ts = pd.cut(ts.set_index('date')['value'], num_bins,
               labels=['C{}'.format(i+1) for i in range(num_bins)],
               retbins=True)
        
    if cat_method=='L-qcut':
        cat_ts = pd.qcut(ts.set_index('date')['value'], num_bins,
               labels=['Q{}'.format(i+1) for i in range(num_bins)],
               retbins=True) 
    return cat_ts

def trend_categorize(ts, cat_method, win_size, num_bins):
    if cat_method=='T-rate':
        trend_ts = ts.set_index('date').diff(periods=win_size).shift(-win_size).dropna()['value']
        cat_ts = pd.cut(trend_ts,num_bins,labels=['R{}'.format(i+1) for i in range(num_bins)],
               retbins=True)
        
    if cat_method=='T-percent':
        trend_ts = ts.set_index('date').diff(periods=win_size).shift(-win_size).dropna()['value']
        trend_ts = trend_ts.divide(ts.set_index('date').loc[trend_ts.index]['value'])*100
        cat_ts = pd.cut(trend_ts,num_bins,labels=['P{}'.format(i+1) for i in range(num_bins)],
               retbins=True)
    
    return trend_ts, cat_ts
