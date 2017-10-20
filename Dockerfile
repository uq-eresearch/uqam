FROM debian:9

RUN DEBIAN_FRONTEND=noninteractive && \
  apt-get update && \
  apt-get install -y \
    curl \
    git \
    libboost-python-dev \
    libgraphicsmagick++1-dev \
    libjpeg62-turbo-dev \
    libldap2-dev \
    libpq-dev \
    libsasl2-dev \
    nginx \
    postgresql \
    postgresql-contrib \
    python-dev \
    python-pip

# Install S6 to do process management
RUN curl -L https://github.com/just-containers/s6-overlay/releases/download/v1.21.0.2/s6-overlay-amd64.tar.gz | tar xzv -C /
ENTRYPOINT ["/init"]

ADD requirements/ /app/requirements/

RUN pip install -r /app/requirements/prod.txt

ADD . /app/

WORKDIR /app/

ADD etc/services.d/ /etc/services.d/

VOLUME /srv/uqam-media
VOLUME /app/deploy

RUN useradd -d /app -s /usr/sbin/nologin django && \
  (cd /app && ./manage.py collectstatic --noinput) && \
  rm -f /etc/nginx/nginx.conf /etc/nginx/conf.d/* && \
  ln -s /app/etc/nginx.conf /etc/nginx/nginx.conf && \
  ln -s /app/etc/nginx-gunicorn.conf /etc/nginx/conf.d/gunicorn.conf