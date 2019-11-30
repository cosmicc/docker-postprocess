FROM alfg/ffmpeg:latest
MAINTAINER GalaxyMedia

VOLUME /config
VOLUME /poll
VOLUME /downloads
VOLUME /transcode

# Install apk packages
RUN apk add --no-cache --virtual=builddeps gcc autoconf automake libtool build-base ffmpeg
RUN apk add --no-cache bash git curl wget tar python3 py3-setuptools python3-dev libffi-dev musl-dev openssl-dev ffmpeg-dev tzdata

# Install python and packages
RUN pip3 install --no-cache --upgrade pip setuptools wheel requests requests[security] requests-cache babelfish "guessit<2" "subliminal<2" qtfaststart gevent python-qbittorrent deluge-client loguru tmdbsimple

# As per https://github.com/mdhiggins/sickbeard_mp4_automator/issues/643
RUN pip3 uninstall -y stevedore
RUN pip3 install stevedore==1.19.1

# Install MP4 Automator
RUN git clone https://github.com/mdhiggins/sickbeard_mp4_automator.git /opt/mp4_automator && ln -s /config/autoProcess.ini /opt/mp4_automator/autoProcess.ini && rm /opt/mp4_automator/logging.ini && ln -s /config/logging.ini /opt/mp4_automator/logging.ini && ln -s /config/logs/mp4_automator /var/log/sickbeard_mp4_automator

# Install Argtable
RUN cd /tmp && wget http://prdownloads.sourceforge.net/argtable/argtable2-13.tar.gz \
&& tar xzf argtable2-13.tar.gz \
&& cd argtable2-13/ && ./configure && make && make install

# Install Comskip
RUN cd /tmp && git clone git://github.com/erikkaashoek/Comskip.git \
&& cd Comskip && ./autogen.sh && ./configure && make && make install \
&& ln -s /config/PlexComskip.conf /opt/PlexComskip.conf \
&& ln -s /config/comskip.ini /opt/comskip.ini

# Cleanup
RUN apk del builddeps \
&& rm -rf /var/cache/apk/* /tmp/* /tmp/.[!.]*

# Main Scripts
COPY postprocess /
COPY PlexComskip.py /opt
RUN chown 1000.1000 /opt/mp4_automator -R && chown 1000.1000 /opt/PlexComskip.py && chmod ugo+x /opt/PlexComskip.py && chmod ugo+x /postprocess

ENV PATH="/opt/ffmpeg/bin:/opt/mp4_automator:${PATH}"

ENTRYPOINT ["/postprocess"]