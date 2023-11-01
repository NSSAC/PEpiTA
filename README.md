[![DOI](https://zenodo.org/badge/626968215.svg)](https://zenodo.org/badge/latestdoi/626968215)


# PEpiTA
Phase-based Epidemic Time series Analyzer.

### 1. Install required packages
#### ***Required: Python>=3.11***

```bash
pip install -r requirements.txt
```
*******************************************************************
### 2. Running Server on localhost
Open a terminal in the PEpiTA folder and follow these commands:
```bash
cd webdesign
python manage.py migrate # if running for the first time
python manage.py runserver
```

After executing all the above commands you will be able to see a message like this:

_Django version 4.2, using settings 'webdesign.settings'<br>
Starting development server at http://127.0.0.1:8000/<br>
Quit the server with CONTROL-C._

Now open a browser and go to http://localhost:8000/ or http://127.0.0.1:8000/

You can, alternatively, test how the production webserver runs it, using
[gunicorn](https://gunicorn.org) to handle multiple requests.

```bash
# cd webdesign
gunicorn --bind ":8000" webdesign.wsgi
```

Then connect via [http://0.0.0.0:8000](http://0.0.0.0:8000).
*******************************************************************
### 3.  Headless Implementation
workflow_notebook.ipynb shows the implementation of all the python scripts in a Jupyter Notebook.

### You can also try [running with Docker](docker.md).
