# base image  
FROM python:3.11

# setup environment variable  
ENV APP_DIR=/app  

# set work directory  
RUN mkdir -p $APP_DIR  

# where your code lives  
WORKDIR $APP_DIR  

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies  
RUN pip install --upgrade pip

# copy whole project to your docker home directory. 
COPY . $APP_DIR

# run this command to install all dependencies  
RUN pip install -r requirements.txt

# port where the Django app runs
EXPOSE 8000

# start server  
CMD [ "gunicorn", "mysite.wsgi" ]
