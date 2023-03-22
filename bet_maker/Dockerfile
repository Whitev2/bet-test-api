FROM python:3.10

ENV PYTHONUNBUFFERED=1

LABEL version = '1'
LABEL master = 'bet-maker'

RUN mkdir /bet_maker
WORKDIR /bet_maker



COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# for migrations
COPY migrations .
COPY alembic.ini .

COPY src .

