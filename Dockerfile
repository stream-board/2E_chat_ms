FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST "chat-db-1"

RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt
RUN python3.6 manage.py migrate

EXPOSE 4004