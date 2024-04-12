import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

def cat_counts(cat_ts):
    return cat_ts.value_counts()

def single_ts_analyze(cat_ts,bin_bounds,freq):
    summ_df = cat_ts.value_counts().sort_index().reset_index().rename({'value':'category','count':'number_of_occurrences'},axis=1)
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

def get_csq_str(c,p):
    if np.isnan(c):
        cstr = '-'
    else:
        cstr = str(np.round(c,2))
        if p<0.05:cstr+='*'
        if p<0.01:cstr+='*'
        if p<0.001:cstr+='*'
    return cstr

def multi_ts_analyze(cat_df):
    signals = list(cat_df.columns)
    N = len(signals)
    chisq = np.zeros((N,N))
    pval = np.zeros((N,N))
    for i1 in range(N):
        for i2 in range(N):
            s1 = signals[i1]; s2 = signals[i2]
            if s1==s2:
                chisq[i1,i2] = np.nan
                pval[i1,i2] = np.nan
                continue
            val_counts = cat_df[[s1,s2]].value_counts().unstack().fillna(0)
            res = chi2_contingency(val_counts, correction=False)

            chisq[i1,i2] = res[0]
            pval[i1,i2] = res[1]

    chi_df = pd.DataFrame(chisq,index=signals,columns=signals)
    pval_df = pd.DataFrame(pval,index=signals,columns=signals)
    
    csq_str_df = pd.DataFrame(index=signals,columns=signals)
    for s1 in signals:
        for s2 in signals:
            csq_str_df.loc[s1,s2] = get_csq_str(chi_df.loc[s1,s2], pval_df.loc[s1,s2])
            
    return(chi_df,pval_df,csq_str_df)


