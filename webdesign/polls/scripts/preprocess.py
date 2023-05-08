import pandas as pd


def fill_dates(ts):
    ## input ts: source time series with date and value columns
    ## return ts: sorted in time, reindexed daily
    
    pp_ts = ts.copy(deep=True)
    
    date_min = pp_ts['date'].min()
    date_max = pp_ts['date'].max()
    
    
    pp_ts.set_index('date',inplace=True)
    pp_ts = pp_ts.sort_index().reindex(pd.date_range(date_min,date_max))
    pp_ts = pp_ts.reset_index().rename({'index':'date'},axis=1)
    
    return pp_ts

def fill_values(ts,fill_method):
    if fill_method == 'forward':
        pp_ts = ts.set_index('date').fillna(method='ffill').reset_index() ### fillna (forward)
    if fill_method == 'linear':
        pp_ts = ts.set_index('date').interpolate(method='linear').round().reset_index() ### fillna (linear)
    return pp_ts

def smoothing(ts,window):
    pp_ts = ts.set_index('date').rolling(window=window,min_periods=1).mean().reset_index()
    return pp_ts
