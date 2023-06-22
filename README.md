# PEpiTA
Phase-based Epidemic Time series Analyzer.

### 1. Install required packages
#### ***Required a python version>=3.8***
>pip install -r requirements.txt
*******************************************************************
### 2. Running Server on localhost
Open a terminal on the PEpiTA folder and follow these commands:<br>
1. > cd webdesign <be>

<code> _# If deploying the webApp for the first time, please run the below command as well_<br></code>

<code>2. python manage.py migrate</code>

3. >python manage.py runserver
*******************************************************************
### 2. After executing all the above commands you will be able to see a message like this
_Django version 4.2, using settings 'webdesign.settings'<br>
Starting development server at http://127.0.0.1:8000/<br>
Quit the server with CONTROL-C._
*******************************************************************
### 3. Now open a browser and go to http://localhost:8000/ or http://127.0.0.1:8000/
*******************************************************************
### 4.  Headless Implementation
workflow_notebook.ipynb shows the implementation of all the python scripts in a Jupyter Notebook.
