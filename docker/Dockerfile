# Pull base image.
FROM python:2.7-slim-buster as base
FROM base as builder

LABEL name="des"
LABEL maintainer="Javier Garcia Gonzalez <javiergarcia@mykolab.com>"

# Install updates to base image
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y apt-utils
RUN apt-get install -y bash libzbar-dev python-pip python nginx-full python-gunicorn systemd vim runit-systemd procps lsof net-tools default-mysql-server default-mysql-client supervisor varnish python-dev default-libmysqlclient-dev libcairo2-dev icu-devtools libgirepository1.0-dev unzip p7zip unrar-free
RUN apt-get install -y tesseract-ocr "tesseract-ocr-*" pkg-config libicu-dev python-mysqldb libglib2.0-dev redis-server rsyslog

WORKDIR /
RUN mkdir -p /var/log/gunicorn /var/log/celery
COPY webapp.tgz .
RUN tar zxvf webapp.tgz 
RUN chown -R www-data:www-data /webapp
COPY nginx.tgz .
COPY supervisordkr.tgz .
COPY varnish.tgz .
COPY cert.tgz .
RUN tar zxvf cert.tgz -C /
RUN tar zxvf supervisordkr.tgz -C /etc/
RUN tar zxvf varnish.tgz -C /etc/
RUN tar zxvf nginx.tgz -C /etc/
RUN rm /*.tgz
RUN update-rc.d -f mysql defaults
RUN update-rc.d -f supervisor defaults
COPY config.sh .
COPY init.sql .
RUN chmod +x config.sh
RUN service mysql start && service supervisor start && bash /config.sh
ENV DJANGO_SETTINGS_MODULE=DataEntry_v2.settings
WORKDIR /
ENV PYTHONPATH=/usr/bin:/usr/local/bin:/usr/lib:/usr/local/lib

RUN python2 -m pip install --upgrade pip
RUN python2 -m pip install mysqlclient
RUN python2 -m pip install -r /webapp/DataEntry_v2/requirements.txt
RUN service mysql start ; service supervisor start ; cd /webapp/DataEntry_v2/ ; python2 manage.py migrate ; python2 manage.py migrate --run-syncdb ; python2 manage.py loaddata user.json 
RUN cd /webapp/DataEntry_v2 ; service mysql start ; sleep 5s ; python2 manage.py dbshell < props.sqldump
RUN service varnish stop ; update-rc.d -f varnish remove ; service nginx stop ; update-rc.d -f nginx remove 
RUN update-rc.d -f redis-server defaults && service redis-server start
RUN touch /var/log/gunicorn/gunicorn.err.log ; touch /var/log/gunicorn/gunicorn.out.log
RUN supervisorctl status
COPY start.sh .
RUN chmod +x start.sh

ENTRYPOINT ["/start.sh"]

