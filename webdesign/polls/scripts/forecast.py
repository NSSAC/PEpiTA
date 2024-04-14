import pandas as pd
import numpy as np
import sys, os
import pmdarima as pm
from categorize import level_categorize
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
        fmt_df=fmt_df.append(conv_quant(ff.loc[[i]]))
        id_vars=['point','gt_avl_date','target_end_date','horizon','fct_std','fct_lb','fct_ub']

        out_df=fmt_df.melt(id_vars=id_vars,var_name=['output_type_id'])
    return out_df


def get_qts_prbs(fcts,horizon):
    qnts=fcts[fcts.horizon==horizon].value.values
    probs=fcts[fcts.horizon==horizon].output_type_id.values
    return qnts, probs

def get_cats_bins(y,cat_method):
    ts=pd.DataFrame()
    ts.loc[:,'date']=y.index
    ts.loc[:,'value']=y.values

    cat_method='L-qcut'
    num_bins=5
    cat_ts, bin_bounds = level_categorize(ts,cat_method,num_bins)
    return cat_ts, bin_bounds

def ARIMA_func(y,verbose=True,log=False,bias_on=False, horizon=4, cat_method='L-qcut'):
    
    if log:
        y[y<0]=0
        y=np.log(y+1)
    model = pm.auto_arima((y[:]), seasonal=False,error_action="ignore")
    #fct,fct_ci=model.predict(horizon,return_conf_int=True)
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
    
    cat_ts,bin_bounds=get_cats_bins(y,cat_method)
    cat_fct=pd.DataFrame()#qfct[['gt_avl_date','target_end_date','horizon']].drop_duplicates()

    cats=sorted(cat_ts.values.unique())

    for h in range(0,horizon):
        hrzn_cat=pd.DataFrame()
        qnts,probs=get_qts_prbs(qfct,h)

        qnts_app=np.append(np.append(0,qnts),np.inf)
        probs_app=np.append(np.append(0,probs),1)

        cat_cum_probs=griddata(qnts_app,probs_app,bin_bounds)
        cat_probs=np.diff(cat_cum_probs)


        hrzn_cat.loc[:,'output_type_id']=cats
        hrzn_cat.loc[:,'value']=cat_probs
        hrzn_cat.loc[:,'horizon']=h
        # hrzn_cat=hrzn_cat.reset_index()
        cat_fct=cat_fct.append(hrzn_cat)
    cat_fct=qfct[['gt_avl_date','target_end_date','horizon']].drop_duplicates().merge(cat_fct,on='horizon')
    return qfct,cat_fct, model

def fcast_example():
    loc='US'
    hrzn='2024-03-16'
    bias_on=False
    cat_method='L-qcut'
    horizon=4
    #gtlocal = pd.read_csv('/sfs/qumulo/qproject/biocomplexity/forecast/CSTE/data/flu_hosp_weekly_filt_case_data.csv', dtype={'state':str})
    #gtlocal = pd.read_csv('/project/biocomplexity/forecast/CSTE/data/data-truth/flu_hosp_weekly_data.csv',dtype={'state':str})
    data_file='https://raw.githubusercontent.com/cdcepi/FluSight-forecast-hub/main/target-data/target-hospital-admissions.csv'
    df=pd.read_csv(data_file)
    gtlocal=df.pivot(index='location',columns='date',values='value')
    #gtlocal.set_index('location',inplace=True)
    gtlocal.columns = [pd.Timestamp(x) for x in gtlocal.columns]

    obs_date=pd.to_datetime(hrzn)
    y=gtlocal.loc[loc,:obs_date]
    qfct,cat_fct,opt_model=ARIMA_func(y,verbose=True,log=False,bias_on=bias_on,horizon=horizon,cat_method=cat_method)
    print(qfct,cat_fct)
    
    return qfct

