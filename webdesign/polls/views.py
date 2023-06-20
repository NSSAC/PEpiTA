from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import os
import pandas as pd
from os.path import exists
import json
from datetime import datetime
from .scripts import preprocess
from .scripts import analyze
from .scripts import categorize
from .scripts import visualize
import altair as alt 
import numpy as np
import zipfile


file_directory = ''
input_ts = pd.DataFrame()
pp_ts = pd.DataFrame()
csvname=''
freq='D'
csvtime=''
context={}
csvtype='Singletime'

def index(request):
    cat_ts = pd.Series
    trend_ts = pd.Series
    bin_bounds = np.ndarray

    global file_directory, input_ts, pp_ts, csvname, freq, csvtime, context, csvtype
    context={}

    if request.method == 'POST' and 'uploadbutton' in request.POST:
        uploaded_file = request.FILES['document']

        if uploaded_file.name.endswith('.csv'):
            savefile = FileSystemStorage()
            csvname = savefile.save(uploaded_file.name, uploaded_file)
            d = os.getcwd() 
            file_directory = d+'/media/'+csvname 
            messages.info(request, 'File upload Success!')
            loc = csvname.rfind("_")
            csvname = csvname[0:len(csvname)-12]+'.csv'
            csvtime= os. path. getmtime(file_directory)
            if 'W' in request.POST.getlist('csvfrequency'):
                freq='W'
            else:
                freq='D'
            if 'Multitime' in request.POST.getlist('uploadtype'):
                csvtype='Multitime'
            else:
                csvtype='Singletime'
            
            readfile(file_directory)
            context= {'csvname': csvname} 
            context.update({'csvtime': datetime.utcfromtimestamp(csvtime)} )
            context.update( {'csvdata':input_ts.to_dict('records')}) 
        elif not uploaded_file.name.endswith('.csv'):
            messages.warning(request, 'Please use .csv file extension!')
        
        elif len(type)==0:
            messages.warning(request, 'Please select csv type!')
        
        else:
            messages.warning(request, 'Upload failed. Please try again!')
    
    if request.method == 'POST' and 'runbutton' in request.POST:
        if exists(file_directory):
            formdata = {}
            # formdata['csvfrequency'] = freq

            csvtime= os.path.getmtime(file_directory)
            methods=request.POST.getlist('datapreprocess')
            smoothing_window = request.POST.get('smoothingwindow')
            cat_method=request.POST.getlist('categorizetype')
            num_bins = request.POST.get('binsize')
            win_size = request.POST.get('trendsize')

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
            context.update({'csvtime': datetime.utcfromtimestamp(csvtime)} )
            
            formdata['smoothingwindow'] = smoothing_window
            formdata['binsize'] = num_bins  

            imagelist = []
            if(csvtype=='Singletime'):
                workflow_type='single'
                input_df = input_ts
                name, cat_ts, df ,formdata = single_ts_workflow(input_df,request, formdata, methods, freq, cat_method, workflow_type, smoothing_window, win_size, num_bins, custom_range)
                
                context.update({'graphfile': name})
                context.update({'qdata': json.loads(df.reset_index().to_json(orient='records'))})
                timestr = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
                name=timestr+'_analyticalsummary.csv' 
                save_path = os.getcwd() +'/media/analytical_summary/'+name
                df.to_csv(save_path) 
                context.update( {'analyticalsummary': name} )

                timestr = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
                name=timestr+'_catdownload.csv' 
                save_path = os.getcwd() +'/media/categorize_output/'+name
                cat_ts.to_csv(save_path) 
                context.update( {'catdownload': name} )
                context.update( {'csvtype':'Singletime'})
            
            elif(csvtype=='Multitime'):
                workflow_type='multi-signal'
                cat_df = pd.DataFrame()
                for column in input_ts.columns:
                    signal_ts = input_ts[[column]]
                    signal_ts.columns = ['value']

                    input_df = signal_ts.reset_index()
                    print("**"+column+"**")
                    name, cat_tss, df ,formdata = single_ts_workflow(input_df, request, formdata, methods, freq, cat_method, 'single', smoothing_window, win_size, num_bins, custom_range, title=column)
                    cat_ts = single_ts_workflow(input_df, request, formdata, methods, freq, cat_method, workflow_type, smoothing_window, win_size, num_bins, custom_range)
                    cat_df = pd.concat([cat_df,cat_ts],axis=1)
                    imagelist.append({'name': name})
                cat_df.columns = input_ts.columns
                name = visualize.multi_signal_plot(cat_df, cat_method)
                imagelist.insert(0, {'name': name})
                multiimagezip=zipfiles(imagelist)
                
                context.update( {'multiimagezip':multiimagezip})
                context.update( {'csvtype':'Multitime'})
                context.update({'imagelist':imagelist})
           
            context.update( {'formdata': json.dumps(formdata)} )
            context.update( {'csvdata':input_ts.to_dict('records')})
            
        else:
            messages.warning(request, 'Please upload a .csv file first!')
    context.update( {'currentpath':'index'})
    return render(request, 'pages/index.html',context)


def readfile(filename):
    global input_ts
    if(csvtype=='Singletime'):
        input_ts = pd.read_csv(filename,parse_dates=['date'])
    elif(csvtype=='Multitime'):
        input_ts = pd.read_csv(filename,parse_dates=['date'], index_col=0)
    

def csvtables(request):
    global context
    context.update( {'currentpath':'csvtables'})
    if request.method == 'POST':
        index(request)
        return render(request, 'pages/index.html',context)
    else:
        return render(request, 'pages/csvtables.html',context)
    

def single_ts_workflow(input_df, request, formdata, methods, freq, cat_method, workflow_type, smoothing_window, win_size, num_bins, custom_range, title=None):
    global pp_ts
    if 'fill_datesvalues' in methods:
        fill_method = 'linear'
        pp_ts = preprocess.fill_dates(input_df, freq)
        pp_ts = preprocess.fill_values(pp_ts, fill_method)
        formdata['fill_datesvalues'] = 'checked'
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
            name = visualize.single_ts_level_plot(pp_ts, cat_ts, bin_bounds)
        elif(cat_method[0] == 'categorizetypetrend'):
            name = visualize.single_ts_trend_plot(pp_ts,trend_ts,cat_ts,bin_bounds)
        
        return name, cat_ts, pd.DataFrame( analyze.single_ts_analyze(cat_ts, bin_bounds, freq)), formdata
    else:
        return cat_ts
    
def zipfiles(filenames):
    name=datetime.utcnow().strftime('%Y%m%d%H%M%S%f')+'_images.zip'
    spath=os.getcwd() +'/media/zip/'+name

    with zipfile.ZipFile(spath, 'w') as z:
        for i in filenames:
            fpath='media/figures/'+i['name']
            z.write(fpath)
    z.close()
    return name