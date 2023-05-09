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

file_directory = ''
input_ts = pd.DataFrame()
pp_ts = pd.DataFrame()

def index(request):
    context = {}
    cat_ts= pd.Series
    global attribute, file_directory, input_ts, pp_ts
    if request.method == 'POST' and 'uploadbutton' in request.POST:
        print(request.POST)
        uploaded_file = request.FILES['document']
        if uploaded_file.name.endswith('.csv'):
            savefile = FileSystemStorage()
            name = savefile.save(uploaded_file.name, uploaded_file)
            d = os.getcwd() 
            file_directory = d+'/media/'+name 
            messages.info(request, 'File upload Success!')
            readfile(file_directory)
        else:
            messages.warning(request, 'Please use .csv file extension!')
    
    if request.method == 'POST' and 'methodsbutton' in request.POST:
        if exists(file_directory):
            methods=request.POST.getlist('datapreprocess')
            for method in methods:
                if method == 'fill_dates':
                    pp_ts = preprocess.fill_dates(input_ts)
                if method == 'fill_values':
                    fill_method = 'linear'
                    if pp_ts.empty:
                         pp_ts = input_ts
                    pp_ts = preprocess.fill_values(pp_ts, fill_method)
                if method == 'smoothing':
                    if pp_ts.empty:
                         pp_ts = input_ts
                    pp_ts = preprocess.smoothing(pp_ts, 7)

            #data categorize
            cat_method=request.POST.getlist('datacategorize')
            num_bins = 5
            if pp_ts.empty:
                pp_ts = input_ts    
            cat_ts, bin_bounds = categorize.level_categorize(pp_ts, cat_method[0], num_bins)
            
            timestr = time.strftime("%Y%m%d-%H%M%S")
            name=timestr+'.csv' 
            save_path = os.getcwd() +'/media/categorize_output/'+name
            cat_ts.to_csv(save_path) 
            context= {'catdownload': name} 

            #data analyze
            context.update( {'d': analyze.cat_counts(cat_ts)} )
            df = pd.DataFrame( analyze.cat_counts(cat_ts))
            data = []
            data = json.loads(df.reset_index().to_json(orient='records'))
            context.update({'qdata': data})

            #data visualize
            name = visualize.dual_plot(pp_ts, cat_ts, bin_bounds)
            context.update({'graphfile': name})
            return render(request, 'pages/index.html', context)
        else:
            messages.warning(request, 'Please upload a .csv file first!')

    return render(request, 'pages/index.html')


def readfile(filename):
    global input_ts
    input_ts = pd.read_csv(filename,parse_dates=['date'])
