import numpy as np
import pandas as pd

def cat_counts(cat_ts):
    return cat_ts.value_counts()

def single_ts_analyze(cat_ts,bin_bounds,freq):
    summ_df = cat_ts.value_counts().sort_index().reset_index().rename({'index':'category','value':'number_of_occurrences'},axis=1)
    summ_df['percent_time_spent'] = summ_df['number_of_occurrences'].apply(lambda x: str(np.round(x/len(cat_ts)*100,2))+'%')
    summ_df['bin_boundaries'] = summ_df['category'].apply(lambda x: str((np.round(bin_bounds[int(x[1:])-1],2),
                                                             np.round(bin_bounds[int(x[1:])],2))))
    
    ## get run length of each category
    mask = cat_ts.ne(cat_ts.shift())
    ids = cat_ts[mask].to_numpy()
    counts = cat_ts.groupby(mask.cumsum()).cumcount().add(1).groupby(mask.cumsum()).max().to_numpy()
    runlengths = pd.Series(counts, index=ids, name='counts')
    dur_dict = runlengths.reset_index().groupby('index')['counts'].mean().to_dict()
    
    summ_df['average_duration_spent'] = summ_df['category'].apply(lambda x: np.round(dur_dict[x],1) if x in dur_dict.keys() else 0)
    return summ_df[['category','bin_boundaries','number_of_occurrences','percent_time_spent','average_duration_spent']]