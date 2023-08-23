Bootstrap: docker
From: python:3.11

%files
LICENSE
pepita.scif
requirements.txt
webdesign

%post
pip install -r requirements.txt
pip install scif ipython
scif install /pepita.scif

%runscript
exec scif "$@"
