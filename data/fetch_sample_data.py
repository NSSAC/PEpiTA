import pandas as pd

hhs = pd.read_csv('https://healthdata.gov/api/views/g62h-syeh/rows.csv',parse_dates=['date'])
hhs = hhs[hhs.state=='VA']
select_cols = ['previous_day_admission_pediatric_covid_confirmed','previous_day_admission_adult_covid_confirmed']
hhs.set_index('date')[select_cols].sum(axis=1).reset_index().rename({0:'value'},axis=1).to_csv('va_covid_admissions.csv',index=None)

vhha = pd.read_csv('https://data.virginia.gov/api/views/28wk-762y/rows.csv',parse_dates=['Date'],usecols=[0,1])
vhha.columns = ['date','value']
vhha.to_csv('va_covid_occupancy.csv',index=None)