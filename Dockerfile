FROM python:3

RUN mkdir /code
WORKDIR /code

ADD . /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
