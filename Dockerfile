FROM ubuntu:14.04
MAINTAINER Ryan Ploetz <ryan.ploetz@gmail.com>
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update

RUN apt-get -y install python3-pip python3-dev postgresql postgresql-contrib libpq-dev libxml2-dev libxslt1-dev curl

USER postgres
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
    createdb -O docker SMSSchedulerServer_dev

USER root
ENV PATH /usr/local/bin:$PATH
ENV ALLOWED_HOSTS *
ENV DEBUG True
ENV TWILIO_ACCOUNT_SID AC7089d119fc90cdf546b98867cdb9cbfe
ENV TWILIO_AUTH_TOKEN 2503730ee7a56c4fcdad3aabf889f9ca

COPY ./api /api
COPY ./SMSSchedulerServer /SMSSchedulerServer
COPY ./manage.py /manage.py
COPY ./requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt

RUN python3 ./manage.py syncdb

EXPOSE 3000

CMD python3 ./manage.py runserver [::]:3000