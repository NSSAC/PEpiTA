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
