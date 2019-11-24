FROM alfg/ffmpeg:latest
MAINTAINER GalaxyMedia

VOLUME /config
VOLUME /poll
VOLUME /downloads
VOLUME /transcode


# Install Git & Curl
RUN apk add --no-cache git curl

# Install MP4 Automator
RUN git clone https://github.com/mdhiggins/sickbeard_mp4_automator.git /opt/mp4_automator

RUN apk add --no-cache \
  python3 \
  py3-setuptools \
  python3-dev \
  libffi-dev \
  gcc \
  musl-dev \
  openssl-dev \
  ffmpeg

# Install python and packages
RUN pip3 install --no-cache --upgrade pip

RUN pip3 install setuptools wheel requests requests[security] requests-cache babelfish "guessit<2" "subliminal<2" qtfaststart gevent python-qbittorrent deluge-client loguru
# As per https://github.com/mdhiggins/sickbeard_mp4_automator/issues/643
ONBUILD RUN pip3 uninstall stevedore
ONBUILD RUN pip3 install stevedore==1.19.1
RUN ln -s /config/autoProcess.ini /opt/mp4_automator/autoProcess.ini
# RUN rm /opt/mp4_automator/logging.ini
# RUN ln -s /config/logging.ini /opt/mp4_automator/logging.ini
RUN ln -s /config/logs/mp4_automator /var/log/sickbeard_mp4_automator

RUN ln -s /usr/bin/python3 /usr/bin/python

# Install nzbToMedia
RUN apk add --no-cache \
    p7zip \
    unrar \
    wget \
    unzip \
    tar
RUN git clone https://github.com/clinton-hall/nzbToMedia.git /opt/nzbtomedia
RUN ln -s /config/autoProcessMedia.cfg /opt/nzbtomedia/autoProcessMedia.cfg

COPY poller /
RUN chmod +x /poller

RUN rm /opt/mp4_automator/post_process/* -r
RUN mkdir /opt/mp4_automator/post_process/resources

COPY post_process.py /opt/mp4_automator/post_process

RUN chmod ugo+x /opt/mp4_automator/post_process/post_process.py

RUN chown 1000.1000 /opt/mp4_automator -R

ENTRYPOINT ["/poller"]