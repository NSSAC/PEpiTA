import pandas as pd
import numpy as np
import sys, os
import pmdarima as pm
from . import categorize
from scipy.interpolate import griddata

def get_gauss_quant(temp):
    temp_ind=temp.index
    loc=temp.loc[temp_ind,'point']
    std=temp.loc[temp_ind,'fct_std']
    return loc, std

def gen_gauss_samp(loc,std):
    N=1000
    g_dist=np.zeros(N)
    for i in range(N):
        g_dist[i]=np.random.normal(loc=loc,scale=std)
    quantiles = np.append(np.append([0.01,0.025],np.arange(0.05,0.95+0.05,0.050)), [0.975,0.99])

    neg_ind=np.where(g_dist<0)
    g_dist[neg_ind]=0


    q_vals=np.quantile(g_dist,q=quantiles)

    qdf=pd.DataFrame.from_dict(data=dict(zip(quantiles,q_vals)),orient='index').T
    return qdf

def conv_quant(temp):
    l,s=get_gauss_quant(temp)
    qdf=gen_gauss_samp(l,s)
    temp_ind=temp.index
    for p in sorted(qdf.columns.astype(float)):
        pr=float(round(p,3))
    
        temp.loc[temp_ind,pr]=qdf[p].values
    return temp

def convert_quant(ff):
    if not ff.columns.str.contains('fct_std').all():
        ff.loc[:,'fct_std']=(ff.loc[:,'fct_ub']-ff.loc[:,'fct_lb'])/3.92
    fmt_df=pd.DataFrame()
    for i in ff.index:
        fmt_df=pd.concat([fmt_df,conv_quant(ff.loc[[i]])])
        id_vars=['point','gt_avl_date','target_end_date','horizon','fct_std','fct_lb','fct_ub']

        out_df=fmt_df.melt(id_vars=id_vars,var_name=['output_type_id'])
    return out_df


def get_qts_prbs(fcts,horizon):
    qnts=fcts[fcts.horizon==horizon].value.values
    probs=fcts[fcts.horizon==horizon].output_type_id.values
    return qnts, probs

def get_cats_bins(y,cat_method,num_bins,win_size=None):
    ts=pd.DataFrame()
    ts.loc[:,'date']=y.index
    ts.loc[:,'value']=y.values
        
    cat_ts, bin_bounds = categorize.level_categorize(ts,cat_method,num_bins)
    return cat_ts, bin_bounds
    

def ARIMA_func(input_ts,cat_method, num_bins, win_size=None, horizon=4, verbose=True,log=False,bias_on=False):
    y = input_ts.set_index('date')['value']
    
    if log:
        y[y<0]=0
        y=np.log(y+1)
    model = pm.auto_arima((y[:]), seasonal=False,error_action="ignore")
    fct,fct_ci=model.predict(horizon,return_conf_int=True)
    
    if log:
        fct=np.exp(fct)
        fct_ci[:,0]=np.exp(fct_ci[:,0])
        fct_ci[:,1]=np.exp(fct_ci[:,1])
    ind=[y.index[-1]+pd.Timedelta(weeks=i) for i in range(1,horizon+1)]
    
    if bias_on:
        bias=(fct[0]-y[-1])
        if bias > 0:
            bias = 0
    else:
        bias=0
    
    yfct=pd.DataFrame(index=ind)
    yfct.index.name='target_end_date'
    yfct.loc[:,'point']=fct-bias
    yfct.loc[:,'fct_lb']=fct_ci[:,0]-bias
    yfct.loc[:,'fct_ub']=fct_ci[:,1]-bias
    yfct.loc[yfct['fct_lb']<0,'fct_lb']=0
    yfct.loc[yfct['fct_ub']<0,'fct_ub']=0
    yfct.loc[yfct['point']<0,'point']=0
    yfct.loc[:,'gt_avl_date']=y.index[-1]
    yfct=yfct.reset_index()
    yfct.loc[:,'horizon']=((yfct.target_end_date-yfct.gt_avl_date).dt.days//7)-1
    qfct=convert_quant(yfct)
    
    
    cat_ts, bin_bounds = get_cats_bins(y,cat_method,num_bins,win_size)
    
    cat_fct=pd.DataFrame()
    cats=sorted(cat_ts.values.unique())
    
    for h in range(0,horizon):
        hrzn_cat=pd.DataFrame()
        qnts,probs=get_qts_prbs(qfct,h)
        
        qnts_app=np.append(np.append(0,qnts),np.inf)
        #qnts_app=np.append(np.append(qnts[0],qnts),qnts[-1])
        probs_app=np.append(np.append(0,probs),1)
        
        
        ##### snippet for converting quantile values to trend_ts (need to be adapted)
        # if cat_method[0]=='T':
        #     trend_ts = ts.set_index('date').diff(periods=win_size).shift(-win_size).dropna()['value']
        #     if cat_method=='T-percent':
        #         trend_ts = trend_ts.divide(ts.set_index('date').loc[trend_ts.index]['value'])*100
        

        cat_cum_probs=griddata(qnts_app,probs_app,bin_bounds)
        cat_probs=np.diff(cat_cum_probs)

        hrzn_cat.loc[:,'output_type_id']=cats
        hrzn_cat.loc[:,'value']=cat_probs
        hrzn_cat.loc[:,'horizon']=h
        cat_fct=pd.concat([cat_fct,hrzn_cat])
    cat_fct=qfct[['gt_avl_date','target_end_date','horizon']].drop_duplicates().merge(cat_fct,on='horizon')
    
    return qfct,cat_fct

def fcast_example():
    loc='US'
    data_cutoff='2024-03-16'
    obs_date=pd.to_datetime(data_cutoff)

    fname='https://raw.githubusercontent.com/cdcepi/FluSight-forecast-hub/main/target-data/target-hospital-admissions.csv'
    df=pd.read_csv(fname,parse_dates=['date'])
    
    input_ts=df.pivot(index='date',columns='location',values='value')[loc].reset_index()
    input_ts.columns = ['date','value']
    
    
    bias_on=False
    cat_method='L-qcut'
    num_bins = 5
    horizon=4
    qfct,cat_fct=ARIMA_func(y,verbose=True,log=False,bias_on=bias_on,horizon=horizon,cat_method=cat_method)
    
    return qfct, cat_fct

