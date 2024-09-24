FROM debian:bookworm

RUN apt-get update
RUN apt-get install -y \
uwsgi uwsgi-plugin-python3 nginx \
python3 python3-pip libtiff5-dev libjpeg62-turbo-dev libopenjp2-7-dev zlib1g-dev \
libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
libharfbuzz-dev libfribidi-dev libxcb1-dev

ADD default /etc/nginx/sites-enabled/default

RUN mkdir /app
COPY src /app
ADD startup.sh /app/startup.sh

CMD [ "/app/startup.sh" ]


