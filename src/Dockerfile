FROM python:3.7-alpine

EXPOSE 5000

RUN mkdir /opt/app
WORKDIR /opt/app

COPY requirements.txt /opt/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /opt/app

CMD python -m mtg-ml --help