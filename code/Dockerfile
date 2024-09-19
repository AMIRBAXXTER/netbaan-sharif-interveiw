FROM python:3.11.4-alpine

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/PY/BIN:$PATH"

RUN pip install --upgrade pip

COPY . /code

RUN pip install -r requirements.txt
