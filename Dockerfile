FROM alfg/ffmpeg:latest
MAINTAINER GalaxyMedia

VOLUME /config
VOLUME /poll
VOLUME /downloads
VOLUME /transcode


# Install Git & Curl
RUN apk add --no-cache git curl

# Install Alpine packages
RUN apk add --no-cache --virtual=builddeps autoconf automake libtool git wget tar build-base tzdata bash python3 py3-setuptools python3-dev libffi-dev gcc musl-dev openssl-dev curl
# python2 py2-pip py2-setuptools python2-dev

# Install python and packages
RUN pip3 install --no-cache --upgrade pip
# RUN pip install --no-cache --upgrade pip

RUN pip3 install setuptools wheel requests requests[security] requests-cache babelfish "guessit<2" "subliminal<2" qtfaststart gevent python-qbittorrent deluge-client loguru tmdbsimple
# RUN pip install setuptools wheel requests requests[security] requests-cache babelfish "guessit<2" "subliminal<2" qtfaststart gevent python-qbittorrent deluge-client stevedore==1.19.1

# As per https://github.com/mdhiggins/sickbeard_mp4_automator/issues/643
ONBUILD RUN pip3 uninstall stevedore
ONBUILD RUN pip3 install stevedore==1.19.1

# Install MP4 Automator
RUN git clone https://github.com/mdhiggins/sickbeard_mp4_automator.git /opt/mp4_automator

RUN ln -s /config/autoProcess.ini /opt/mp4_automator/autoProcess.ini && rm /opt/mp4_automator/logging.ini && ln -s /config/logging.ini /opt/mp4_automator/logging.ini && ln -s /config/logs/mp4_automator /var/log/sickbeard_mp4_automator

# Install Comskip
RUN cd /tmp && wget http://prdownloads.sourceforge.net/argtable/argtable2-13.tar.gz \
&& tar xzf argtable2-13.tar.gz \
&& cd argtable2-13/ && ./configure && make && make install \
&& cd /tmp && git clone git://github.com/erikkaashoek/Comskip.git \
&& cd Comskip && ./autogen.sh && ./configure && make && make install

# COPY --from=plexinc/pms-docker /usr/lib/plexmediaserver/Resources/comskip.ini /opt/comskip.ini

# Main Scripts
COPY postprocess /
RUN chmod ugo+x /postprocess

COPY completetv.sh /
RUN chmod ugo+x /completetv.sh

COPY completemovies.sh /
RUN chmod ugo+x /completemovies.sh

RUN chown 1000.1000 /opt/mp4_automator -R

# Cleanup
RUN rm -rf /var/cache/apk/* /tmp/* /tmp/.[!.]* && apk del gcc build-base automake builddeps

ENTRYPOINT ["/postprocess"]