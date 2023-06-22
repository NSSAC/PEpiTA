# PEpiTA
Phase-based Epidemic Time series Analyzer.

## Install required packages
#### Required a python version>=3.8
pip install -r requirements.txt

## Running Server on localhost(http://localhost:8000/)
Open a terminal on the PEpiTA folder and follow these commands:
1. cd webdesign <br/>


#### <code>If deploying the webApp for the first time, please run the below command as well<br>
2. python manage.py migrate<br>
</code>

3. python manage.py runserver

#### After executing all the above commands you will be able to see a message like this
<code>Django version 4.2, using settings 'webdesign.settings'<br>
Starting development server at http://127.0.0.1:8000/<br>
Quit the server with CONTROL-C.<br></code>

#### Now open a browser and go to http://localhost:8000/ or http://127.0.0.1:8000/

## Headless Implementation
workflow_notebook.ipynb shows the implementation of all the python scripts in a Jupyter Notebook.