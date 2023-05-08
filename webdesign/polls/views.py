from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import os
import pandas as pd
from os.path import exists
import json
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
            methods=request.POST.getlist('methods')
            for method in methods: 
                if method == 'datapreprocess':
                    pp_ts = preprocess.fill_dates(input_ts)
                    fill_method = 'linear'
                    pp_ts = preprocess.fill_values(pp_ts, fill_method)
                    pp_ts = preprocess.smoothing(pp_ts, 7)
                elif method == 'datacategorize':
                    cat_method = 'L-qcut'
                    num_bins = 5
                    if pp_ts.empty:
                        pp_ts = input_ts    
                    cat_ts, bin_bounds = categorize.level_categorize(pp_ts, cat_method, 5)
                elif method == 'dataanalyze':
                    if not cat_ts.empty :
                        context = {'d': analyze.cat_counts(cat_ts)}  
                        df = pd.DataFrame( analyze.cat_counts(cat_ts))
                        data = []
                        data = json.loads(df.reset_index().to_json(orient='records'))
                        context = {'qdata': data}
                elif method == 'datavisualize': 
                    if not cat_ts.empty :
                        name = visualize.dual_plot(pp_ts, cat_ts, bin_bounds)
                        context.update({'graphfile': name})
                        print(context) 
            return render(request, 'pages/index.html', context)
        else:
            messages.warning(request, 'Please upload a .csv file first!')

    return render(request, 'pages/index.html')


def readfile(filename):
    global input_ts
    input_ts = pd.read_csv(filename,parse_dates=['date'])
