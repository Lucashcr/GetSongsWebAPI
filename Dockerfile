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
RUN pip install --no-cache-dir poetry

# copy whole project to your docker home directory.
COPY pyproject.toml $APP_DIR
COPY poetry.lock $APP_DIR

# run this command to install all dependencies
RUN poetry install

COPY . $APP_DIR

# port where the Django app runs
EXPOSE 8000

# start server
CMD [ "poetry", "run", "gunicorn", "-b", "[::]", "-w", "4", "mysite.wsgi" ]
