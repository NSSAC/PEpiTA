import numpy as np

def cat_counts(cat_ts):
    return cat_ts.value_counts()

def single_ts_analyze(cat_ts,bin_bounds):
    summ_df = cat_ts.value_counts().sort_index().reset_index().rename({'index':'category','value':'count'},axis=1)
    summ_df['percent'] = summ_df['count'].apply(lambda x: str(np.round(x/summ_df['count'].sum()*100,2))+'%')
    summ_df['bounds'] = summ_df['category'].apply(lambda x: str((np.round(bin_bounds[int(x[1:])-1],2),
                                                             np.round(bin_bounds[int(x[1:])],2))))
    
    return summ_df