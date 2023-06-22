# PEpiTA
Phase-based Epidemic Time series Analyzer.

## Install required packages
pip install -r requirements.txt

## Running Server on localhost(http://localhost:8000/)
cd webdesign <br/>
### If deploying the webApp for the first time, please run the below command as well<br>
python manage.py migrate<br>

python manage.py runserver

### After executing all the above command you will be able to see a message like this
<code>Django version 4.2, using settings 'webdesign.settings'<br>
Starting development server at http://127.0.0.1:8000/<br>
Quit the server with CONTROL-C.<br></code>

### Then open a browser and go to localhost:8000 or http://127.0.0.1:8000/

## Headless Implementation
workflow_notebook.ipynb shows the implementation of all the python scripts in a Jupyter Notebook.