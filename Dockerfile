FROM python:3.11

# RUN apt-get update \
# 	&& apt-get install -y --no-install-recommends \
# 		postgresql-client \
# 	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt pepita.scif /
COPY webdesign /webdesign
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install ipython scif
RUN scif install /pepita.scif

# RUN python manage.py migrate

EXPOSE 8000

ENTRYPOINT ["scif"]

CMD ["run", "webapp"]