FROM python:3.10

RUN mkdir /app
WORKDIR /app

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

COPY . /app

CMD python main.py
