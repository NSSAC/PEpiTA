from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.forms import URLField
from django.core.exceptions import ValidationError

import os
import pandas as pd
from os.path import exists
from pathlib import Path
import json
from datetime import datetime
from .scripts import preprocess
from .scripts import analyze
from .scripts import categorize
from .scripts import visualize
import numpy as np
import zipfile

from plotly.offline import plot
import plotly.express as px

file_path = ''
input_ts = pd.DataFrame()
pp_ts = pd.DataFrame()
csvname=''
freq='D'
csvtime=''
context={}
csvtype=''
datamindate=''
datacurmindate=''
datamaxdate=''
datacurmaxdate=''

media_path = Path(__file__).resolve().parent.parent / "media"
# make sure output paths are created
fig_path = media_path / "figures"
fig_path.mkdir(exist_ok=True, parents=True)

analytical_summary_path = media_path / "analytical_summary"
analytical_summary_path.mkdir(exist_ok=True, parents=True)

categorize_output_path = media_path / "categorize_output"
categorize_output_path.mkdir(exist_ok=True, parents=True)

zip_path = media_path / "zip"
zip_path.mkdir(exist_ok=True, parents=True)


def index(request):
    cat_ts = pd.Series
    trend_ts = pd.Series
    bin_bounds = np.ndarray

    global file_path, input_ts, pp_ts, csvname, freq, csvtime, context, csvtype, media_path, analytical_summary_path, categorize_output_path, zip_path, datamindate, datamaxdate, datacurmindate, datacurmaxdate
    context={}
    if request.method == 'POST' and 'uploadapibutton' in request.POST:
        dataurl = request.POST.get('apiurltext')
        if validate_url(dataurl):
            if 'W' in request.POST.getlist('csvfrequency'):
                freq='W'
            else:
                freq='D'
            # if 'Multitime' in request.POST.getlist('uploadtype'):
            #     csvtype='Multitime'
            # else:
            #     csvtype='Singletime'

            readapi(dataurl)
            
            csvtime=datetime.utcnow()
            csvname='API URL'
            datamindate=input_ts.index.min()
            datamaxdate=input_ts.index.max()
            datacurmindate=datamindate
            datacurmaxdate=datamaxdate
            context= {'csvname': csvname} 
            context.update({'csvtype': csvtype} )
            context.update({'csvtime': csvtime} )
            context.update( {'csvdata':input_ts.reset_index().to_dict('records')}) 
            context.update({'datamindate': datamindate} )
            context.update({'datamaxdate': datamaxdate} )
            context.update({'datacurmindate': datacurmindate} )
            context.update({'datacurmaxdate': datacurmaxdate} )
            headers=[]
            for col in input_ts.reset_index().columns:
                headers.append({'column': col})
            context.update( {'csvdataheaders':headers}) 
        else:
            messages.warning(request, 'Please enter a valid url')

    if request.method == 'POST' and 'uploadbutton' in request.POST:
        uploaded_file = request.FILES['document']

        if uploaded_file.name.endswith('.csv'):
            savefile = FileSystemStorage()
            csvname = savefile.save(uploaded_file.name, uploaded_file)
            file_path = str(media_path / csvname)
            messages.info(request, 'File upload Success!')
            loc = csvname.rfind("_")
            csvname = uploaded_file.name
            csvtime = datetime.utcfromtimestamp(os.path.getmtime(file_path))
            if 'W' in request.POST.getlist('csvfrequency'):
                freq='W'
            else:
                freq='D'
            # if 'Multitime' in request.POST.getlist('uploadtype'):
            #     csvtype='Multitime'
            # else:
            #     csvtype='Singletime'
            
            readfile(file_path)
            context= {'csvname': csvname} 
            context.update({'csvtype': csvtype} )
            context.update({'csvtime': csvtime} )
            context.update( {'csvdata':input_ts.reset_index().to_dict('records')}) 
            if 'Multitime' in csvtype:
                datamindate=input_ts.index.min()
                datamaxdate=input_ts.index.max()
            elif 'Singletime' in csvtype:
                datamindate=input_ts['date'].min()
                datamaxdate=input_ts['date'].max()
            datacurmindate=datamindate
            datacurmaxdate=datamaxdate
            context.update({'datamindate': datamindate} )
            context.update({'datamaxdate': datamaxdate} )
            context.update({'datacurmindate': datacurmindate} )
            context.update({'datacurmaxdate': datacurmaxdate} )
            headers=[]
            for col in input_ts.reset_index().columns:
                headers.append({'column': col})
            context.update( {'csvdataheaders':headers}) 

        elif not uploaded_file.name.endswith('.csv'):
            messages.warning(request, 'Please use .csv file extension!')
        
        elif len(type)==0:
            messages.warning(request, 'Please select csv type!')
        
        else:
            messages.warning(request, 'Upload failed. Please try again!')
    
    if request.method == 'POST' and 'runbutton' in request.POST:
        if not input_ts.empty:
            formdata = {}
            # formdata['csvfrequency'] = freq
            methods=request.POST.getlist('datapreprocess')
            smoothing_window = request.POST.get('smoothingwindow')
            cat_method=request.POST.getlist('categorizetype')
            num_bins = request.POST.get('binsize')
            win_size = request.POST.get('trendsize')
            fill_method=request.POST.getlist('fillmethod')
            datacurmindate=request.POST.getlist('min_date')
            datacurmaxdate=request.POST.getlist('max_date')

            datacurmindate = datetime.strptime(datacurmindate[0], '%Y-%m-%d')
            datacurmaxdate = datetime.strptime(datacurmaxdate[0], '%Y-%m-%d')

            if(not smoothing_window):
                smoothing_window = 7
            else:
                smoothing_window = int(smoothing_window)
            if(not num_bins):
                num_bins = 5
            else:
                num_bins = int(num_bins)
            if(not win_size):
                win_size = 5
            else:
                win_size = int(win_size)
            if('forward' in fill_method):
                fill_method = 'forward'
            else:
                fill_method = 'linear'
            minval=0
            maxval=50
            custom_range=()
            if request.POST.getlist('custombin'):
                if request.POST.get('mincustomsize'):
                    minval=int(request.POST.get('mincustomsize'))
                if request.POST.get('maxcustomsize'):
                    maxval=int(request.POST.get('maxcustomsize'))
            custom_range = (minval,maxval)
            

            context= {'csvname': csvname} 
            context.update({'csvtime': csvtime} )
            
            formdata['smoothingwindow'] = smoothing_window
            formdata['binsize'] = num_bins  

            imagelist = []
            multidf=[]
            multidflist=[]
            headers=[]
            if(csvtype=='Singletime'):
                workflow_type='single'
                input_df = input_ts.loc[(input_ts['date'] >= datacurmindate ) & (input_ts['date'] <= datacurmaxdate)]
                name, cat_ts, df ,formdata = single_ts_workflow(input_df,request, fill_method, formdata, methods, freq, cat_method, workflow_type, smoothing_window, win_size, num_bins, custom_range)
                
                context.update({'graphfile': name})
                context.update({'qdata': json.loads(df.reset_index().to_json(orient='records'))})
                timestr = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
                name=timestr+'_analyticalsummary.csv' 
                save_path = str(analytical_summary_path / name)
                df.to_csv(save_path) 
                context.update( {'analyticalsummary': name} )

                timestr = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
                name=timestr+'_catdownload.csv' 
                save_path = str(categorize_output_path / name)
                cat_ts.to_csv(save_path) 
                context.update( {'catdownload': name} )
                context.update( {'csvtype':'Singletime'})
                for col in input_ts.columns:
                    headers.append({'column': col})
                context.update( {'csvdataheaders':headers})
                context.update( {'csvdata':input_ts.to_dict('records')}) 
                
                fig = px.line(pp_ts, x='date', y="value")
                graph_plotly = plot(fig, output_type="div")
                # context.update( {'graph_plotly':graph_plotly})

            
            elif(csvtype=='Multitime'):
                workflow_type='multi-signal'
                cat_df = pd.DataFrame()
                input_tstmp=pd.DataFrame()
                if input_ts[datacurmindate:datacurmaxdate].empty:
                    input_tstmp=input_ts[datacurmaxdate:datacurmindate]
                else:
                    input_tstmp=input_ts[datacurmindate:datacurmaxdate]
           
                for column in input_tstmp.columns:
                    signal_ts = input_tstmp[[column]]
                    signal_ts.columns = ['value']

                    input_df = signal_ts.reset_index()
                    name, cat_tss, df ,formdata = single_ts_workflow(input_df, request, fill_method, formdata, methods, freq, cat_method, 'single', smoothing_window, win_size, num_bins, custom_range, title=column)
                    cat_ts = single_ts_workflow(input_df, request, fill_method, formdata, methods, freq, cat_method, workflow_type, smoothing_window, win_size, num_bins, custom_range)
                    cat_df = pd.concat([cat_df,cat_ts],axis=1)
                    imagelist.append({'name': name})
                    multidf.append({'eachdf':json.loads(df.reset_index().to_json(orient='records')),'name':column})
                    
                    timestr = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
                    name=timestr+'_analyticalsummary_'+column+'.csv'
                    save_path = str(analytical_summary_path / name)
                    df.to_csv(save_path) 
                    multidflist.append({'name': name})
                    
                cat_df.columns = input_ts.columns
                name = visualize.multi_signal_plot(cat_df, cat_method)
                imagelist.insert(0, {'name': name})
                multiimagezip=zipfiles(imagelist,'images','media/figures/')
                context.update( {'multiimagezip':multiimagezip})

                context.update({'qdata': multidf})
                multicsvzip=zipfiles(multidflist,'csv','media/analytical_summary/')
                context.update( {'multicsvzip':multicsvzip})
                
                context.update( {'csvtype':'Multitime'})
                context.update({'imagelist':imagelist})
                timestr = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
                name=timestr+'_catdownload.csv' 
                save_path = str(categorize_output_path / name)
                cat_df.to_csv(save_path) 
                context.update( {'catdownload': name} )
                for col in input_ts.reset_index().columns:
                    headers.append({'column': col})
                context.update( {'csvdataheaders':headers}) 
                context.update( {'csvdata':input_ts.reset_index().to_dict('records')}) 

                fig = px.line(input_ts.reset_index(), x='date', y=input_ts.columns.to_list())
                graph_plotly = plot(fig, output_type="div")
                # context.update( {'graph_plotly':graph_plotly})
                
            context.update({'datamindate': datamindate} )
            context.update({'datamaxdate': datamaxdate} )
            context.update({'datacurmindate': datacurmindate} )
            context.update({'datacurmaxdate': datacurmaxdate} )
            context.update( {'formdata': json.dumps(formdata)} )
            
        else:
            messages.warning(request, 'No data in the memory')
    context.update( {'currentpath':'index'})
    return render(request, 'pages/index.html',context)

def readapi(dataurl):
    global input_ts, csvtype
    csvtype='Multitime'
    dateflag=False
    mainurl=dataurl[0:dataurl.index('.json')+5]
    suffix="?$select=count(*)"
    maxlimit=pd.read_json(mainurl+suffix)['count'][0]
    
    if('$query' in dataurl):
        suffix="%20LIMIT%20"+str(maxlimit)
    else:
        suffix="?$limit="+str(maxlimit)+"&$offset=0"
    dataurl=dataurl+suffix
    
    results_df = pd.read_json(dataurl)
    results_df=results_df.dropna() 
    for col in results_df.columns:
        if "date" in col.lower() and not dateflag:
            results_df[col] = pd.to_datetime(results_df[col])
            results_df = results_df.rename(columns={col: 'date'})
            dateflag=True
        elif not results_df[col].dtype==np.int64 or  not results_df[col].dtype==np.float64 and not dateflag:
            results_df = results_df.drop(col, axis=1) 
            
    results_df=results_df.drop_duplicates(subset=['date'])
    results_df=results_df.set_index('date')
    input_ts = results_df
    print(input_ts.columns.tolist())

def readfile(filename):
    global input_ts, csvtype
    csvFile = pd.read_csv(filename)
    if(len(csvFile.columns.tolist())==2 and 'date' in csvFile.columns.tolist() and 'value' in csvFile.columns.tolist()):
        csvtype='Singletime'
    else:
        csvtype='Multitime'

    if(csvtype=='Singletime'):
        input_ts = pd.read_csv(filename,parse_dates=['date'])
    elif(csvtype=='Multitime'):
        input_ts = pd.read_csv(filename,parse_dates=['date'], index_col=0)
    

def csvtables(request):
    context.update( {'currentpath':'csvtables'})
    if request.method == 'POST':
        index(request)
        return render(request, 'pages/index.html',context)
    else:
        return render(request, 'pages/csvtables.html',context)
    

def single_ts_workflow(input_df, request, fill_method, formdata, methods, freq, cat_method, workflow_type, smoothing_window, win_size, num_bins, custom_range, title=None):
    global pp_ts
    pp_ts = pd.DataFrame()
    if 'fill_datesvalues' in methods:
        pp_ts = preprocess.fill_dates(input_df, freq)
        pp_ts = preprocess.fill_values(pp_ts, fill_method)
        formdata['fill_datesvalues'] = 'checked'
        formdata['fill_method'] = fill_method+'fill'
    if 'smoothing' in methods :
        if pp_ts.empty:
                pp_ts = input_df
        pp_ts = preprocess.smoothing(pp_ts, smoothing_window)
        formdata['smoothing'] = 'checked'
    if pp_ts.empty:
        pp_ts = input_df 

    if(cat_method[0] == 'categorizetypelevel'):
        levelbasedtype = request.POST.get('levelbasedtype')
        formdata['categorizetypelevel'] = 'checked'
        formdata['levelbasedtype'] = levelbasedtype
        if request.POST.getlist('custombin') and levelbasedtype=="L-cut" and workflow_type != 'multi-signal':
            cat_ts, bin_bounds = categorize.level_categorize(pp_ts, levelbasedtype, num_bins, custom_range)
            formdata['custombin'] = 'checked'
            formdata['mincustomsize'] = custom_range[0]
            formdata['maxcustomsize'] = custom_range[1]
        else:
            cat_ts, bin_bounds = categorize.level_categorize(pp_ts, levelbasedtype, num_bins)
    elif(cat_method[0] == 'categorizetypetrend'):
        trendbasedtype = request.POST.get('trendbasedtype')
        formdata['categorizetypetrend'] = 'checked'
        formdata['levelbasedtype'] = trendbasedtype
        formdata['trendsize'] = win_size
        if request.POST.getlist('custombin') and workflow_type != 'multi-signal':
            trend_ts, (cat_ts, bin_bounds) = categorize.trend_categorize(pp_ts, trendbasedtype, win_size, num_bins, custom_range)
            formdata['custombin'] = 'checked'
            formdata['mincustomsize'] = custom_range[0]
            formdata['maxcustomsize'] = custom_range[1]
        else:
            trend_ts, (cat_ts, bin_bounds) = categorize.trend_categorize(pp_ts, trendbasedtype, win_size, num_bins)

    if workflow_type == 'single':
        if(cat_method[0] == 'categorizetypelevel'):
            name = visualize.single_ts_level_plot(pp_ts, cat_ts, bin_bounds,title)
        elif(cat_method[0] == 'categorizetypetrend'):
            name = visualize.single_ts_trend_plot(pp_ts,trend_ts,cat_ts,bin_bounds,title)
        
        return name, cat_ts, pd.DataFrame( analyze.single_ts_analyze(cat_ts, bin_bounds, freq)), formdata
    else:
        return cat_ts
    
def zipfiles(filenames, tag, path):
    name=datetime.utcnow().strftime('%Y%m%d%H%M%S%f')+'_'+tag+'.zip'
    spath=str(zip_path / name)

    with zipfile.ZipFile(spath, 'w') as z:
        for i in filenames:
            fpath=path+i['name']
            z.write(fpath)
    z.close()
    return name

def validate_url(url):
    url_form_field = URLField()
    try:
        url = url_form_field.clean(url)
    except ValidationError:
        return False
    return True
    