from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import os
import pandas as pd
from os.path import exists
import json
import time
from .scripts import preprocess
from .scripts import analyze
from .scripts import categorize
from .scripts import visualize
import altair as alt 
import numpy as np


file_directory = ''
input_ts = pd.DataFrame()
pp_ts = pd.DataFrame()
csvname=''
csvfreq='daily'
csvtime=''
context={}

def index(request):
    cat_ts = pd.Series
    trend_ts = pd.Series
    bin_bounds = np.ndarray

    global file_directory, input_ts, pp_ts, csvname, csvfreq, csvtime, context
    context={}

    if request.method == 'POST' and 'uploadbutton' in request.POST:
        uploaded_file = request.FILES['document']
        type = request.POST.getlist('uploadtype')

        if uploaded_file.name.endswith('.csv') and len(type)!=0:
            savefile = FileSystemStorage()
            csvname = savefile.save(uploaded_file.name, uploaded_file)
            d = os.getcwd() 
            file_directory = d+'/media/'+csvname 
            messages.info(request, 'File upload Success!')
            loc = csvname.rfind("_")
            csvname = csvname[0:len(csvname)-12]+'.csv'
            csvtime= os. path. getmtime(file_directory)
            
            context= {'csvname': csvname} 
            context.update({'csvtime': time.ctime(csvtime)} )

            readfile(file_directory)
            csvfreq=request.POST.getlist('csvfrequency')
            
            context.update( {'csvdata':input_ts.to_dict('records')}) 
    
        elif not uploaded_file.name.endswith('.csv'):
            messages.warning(request, 'Please use .csv file extension!')
        
        elif len(type)==0:
            messages.warning(request, 'Please select csv type!')
        
        else:
            messages.warning(request, 'Upload failed. Please try again!')
    
    if request.method == 'POST' and 'methodsbutton' in request.POST:
        if exists(file_directory):
            context= {'csvname': csvname} 
            csvtime= os. path. getmtime(file_directory)
            context.update({'csvtime': time.ctime(csvtime)} );

            formdata = {}
            # formdata['csvfrequency'] = freq
            methods=request.POST.getlist('datapreprocess')
            
            freq = 'D'
            if csvfreq == 'weekly':
                freq = 'W'
            
            smoothing_window = request.POST.get('smoothingwindow')

            if(not smoothing_window):
                smoothing_window = 7
            else:
                smoothing_window = int(smoothing_window)
            
            formdata['smoothingwindow'] = smoothing_window
            
            for method in methods:
                if method == 'fill_datesvalues':
                    pp_ts = preprocess.fill_dates(input_ts, freq)
                    fill_method = 'linear'
                    if pp_ts.empty:
                         pp_ts = input_ts
                    pp_ts = preprocess.fill_values(pp_ts, fill_method)
                    formdata['fill_datesvalues'] = 'checked'
                if method == 'smoothing':
                    if pp_ts.empty:
                         pp_ts = input_ts
                    pp_ts = preprocess.smoothing(pp_ts, smoothing_window)
                    formdata['smoothing'] = 'checked'

            #data categorize
            cat_method=request.POST.getlist('categorizetype')
            num_bins = request.POST.get('binsize')
            win_size = request.POST.get('trendsize')
            if(not num_bins):
                num_bins = 5
            else:
                num_bins = int(num_bins)
            if(not win_size):
                win_size = 5
            else:
                win_size = int(win_size)
            
            formdata['binsize'] = num_bins

            if pp_ts.empty:
                pp_ts = input_ts   
            
            minval=0
            maxval=50
            custom_range=()
            if request.POST.getlist('custombin'):
                if request.POST.get('mincustomsize'):
                    minval=int(request.POST.get('mincustomsize'))
                if request.POST.get('maxcustomsize'):
                    maxval=int(request.POST.get('maxcustomsize'))
            custom_range = (minval,maxval)

            if(cat_method[0] == 'categorizetypelevel'):
                levelbasedtype = request.POST.get('levelbasedtype')
                formdata['categorizetypelevel'] = 'checked'
                formdata['levelbasedtype'] = levelbasedtype
                if request.POST.getlist('custombin') and levelbasedtype=="L-cut":
                    cat_ts, bin_bounds = categorize.level_categorize(pp_ts, levelbasedtype, num_bins, custom_range)
                    formdata['custombin'] = 'checked'
                    formdata['mincustomsize'] = minval
                    formdata['maxcustomsize'] = maxval
                else:
                    cat_ts, bin_bounds = categorize.level_categorize(pp_ts, levelbasedtype, num_bins)
            elif(cat_method[0] == 'categorizetypetrend'):
                trendbasedtype = request.POST.get('trendbasedtype')
                formdata['categorizetypetrend'] = 'checked'
                formdata['levelbasedtype'] = trendbasedtype
                formdata['trendsize'] = win_size

                if request.POST.getlist('custombin'):
                    trend_ts, (cat_ts, bin_bounds) = categorize.trend_categorize(pp_ts, trendbasedtype, win_size, num_bins, custom_range)
                    formdata['custombin'] = 'checked'
                    formdata['mincustomsize'] = minval
                    formdata['maxcustomsize'] = maxval
                else:
                    trend_ts, (cat_ts, bin_bounds) = categorize.trend_categorize(pp_ts, trendbasedtype, win_size, num_bins)

            context.update( {'formdata': json.dumps(formdata)} )
            print(json.dumps(formdata))
            
            timestr = time.strftime("%Y%m%d-%H%M%S")
            name=timestr+'_catdownload.csv' 
            save_path = os.getcwd() +'/media/categorize_output/'+name
            cat_ts.to_csv(save_path) 
            context.update( {'catdownload': name} )

            #data analyze
            df = pd.DataFrame( analyze.single_ts_analyze(cat_ts, bin_bounds, freq))
            data = []
            data = json.loads(df.reset_index().to_json(orient='records'))
            context.update({'qdata': data})

            timestr = time.strftime("%Y%m%d-%H%M%S")
            name=timestr+'_analyticalsummary.csv' 
            save_path = os.getcwd() +'/media/analytical_summary/'+name
            df.to_csv(save_path) 
            context.update( {'analyticalsummary': name} )

            #data visualize
            if(cat_method[0] == 'categorizetypelevel'):
                name = visualize.single_ts_level_plot(pp_ts, cat_ts, bin_bounds)
            elif(cat_method[0] == 'categorizetypetrend'):
                name = visualize.single_ts_trend_plot(pp_ts,trend_ts,cat_ts,bin_bounds)
            context.update({'graphfile': name})

            context.update( {'csvdata':input_ts.to_dict('records')})
            
        else:
            messages.warning(request, 'Please upload a .csv file first!')

    return render(request, 'pages/index.html',context)


def readfile(filename):
    global input_ts
    input_ts = pd.read_csv(filename,parse_dates=['date'])

def csvtables(request):
    global context
    print("yayyy")
    print(request)
    if request.method == 'POST':
        print("inside")
        index(request)
        print("inside111111")
        return render(request, 'pages/index.html',context)
    else:
        return render(request, 'pages/csvtables.html',context)
