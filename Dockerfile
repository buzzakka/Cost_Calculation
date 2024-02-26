FROM python:3.12.2

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $HOME
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt --no-cache-dir

COPY . .

RUN python3 manage.py makemigrations && python3 manage.py migrate

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]