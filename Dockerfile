FROM alpine
MAINTAINER GalaxyMedia

VOLUME /config
VOLUME /poll
VOLUME /downloads
VOLUME /transcode


# Install Git & Curl
RUN apk add --no-cache \
  git \
  curl

# Install MP4 Automator
RUN git clone https://github.com/mdhiggins/sickbeard_mp4_automator.git /opt/mp4_automator
RUN apk add --no-cache \
  python \
  py-setuptools \
  py-pip \
  python-dev \
  libffi-dev \
  gcc \
  musl-dev \
  openssl-dev \
  ffmpeg

RUN pip install --upgrade PIP
RUN pip install requests
RUN pip install requests[security]
RUN pip install requests-cache
RUN pip install babelfish
RUN pip install "guessit<2"
RUN pip install "subliminal<2"
RUN pip install qtfaststart
RUN pip install gevent
RUN pip install python-qbittorrent
RUN pip install deluge-client
# As per https://github.com/mdhiggins/sickbeard_mp4_automator/issues/643
ONBUILD RUN pip uninstall stevedore
ONBUILD RUN pip install stevedore==1.19.1
RUN ln -s /config/autoProcess.ini /opt/mp4_automator/autoProcess.ini
RUN ln -s /config/logs/mp4_automator /var/log/sickbeard_mp4_automator

# Install nzbToMedia
RUN apk add --no-cache \
    p7zip \
    unrar \
    wget \
    unzip \
    tar
RUN git clone https://github.com/clinton-hall/nzbToMedia.git /opt/nzbtomedia
RUN ln -s /config/autoProcessMedia.cfg /opt/nzbtomedia/autoProcessMedia.cfg

# Install poller preqs
RUN apk add --no-cache python3 && \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel

RUN pip3 install loguru

COPY poller /
RUN chmod +x /poller

COPY post_sickrage.py /config/post_sickrage.py

RUN (crontab -l 2>/dev/null; echo "*/1 * * * * /poller") | crontab -

#Adding Custom files
#ADD init/ /etc/my_init.d/
#RUN chmod -v +x /etc/my_init.d/*.sh

ENTRYPOINT ["/poller"]