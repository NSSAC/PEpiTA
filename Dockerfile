FROM python:3.11

# RUN apt-get update \
# 	&& apt-get install -y --no-install-recommends \
# 		postgresql-client \
# 	&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py migrate

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
