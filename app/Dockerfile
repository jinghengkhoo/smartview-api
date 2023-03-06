FROM python:3.8.12-bullseye

WORKDIR /usr/src/app

# install dependencies
#RUN add-apt-repository --remove https://apt.kitware.com/ubuntu
RUN apt-get update
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir /usr/src/app/tmp
COPY ./start_flask.sh .
RUN chmod +x /usr/src/app/start_flask.sh

#COPY . .

# run entrypoint.prod.sh
#ENTRYPOINT ["/home/app/gmtc-vista/start_flask.sh"]