FROM python:3.11

LABEL version = '1'
LABEL master = 'bet-provider'

RUN mkdir /bet_provider
WORKDIR /bet_provider

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src .

