FROM python:3.7-alpine

# build deps to install scrapy
RUN apk --update --no-cache add ca-certificates \
  musl-dev musl-utils musl-dbg gcc libevent-dev \
  libxml2-dev libxslt-dev libffi-dev openssl-dev
# postgres connection libs
RUN apk --update --no-cache add postgresql-dev
RUN pip install --no-cache-dir --upgrade pip

WORKDIR /opt/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./hello.py" ]