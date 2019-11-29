FROM alpine:3.8 as build

ARG FFMPEG_VERSION=ffmpeg-snapshot.tar.bz2
ARG AOM_VERSION=master

ARG PREFIX=/opt/ffmpeg
ARG PKG_CONFIG_PATH=/opt/ffmpeg/lib64/pkgconfig
ARG LD_LIBRARY_PATH=/opt/ffmpeg/lib
ARG MAKEFLAGS="-j4"

# FFmpeg build dependencies.
RUN apk add --update build-base cmake freetype-dev lame-dev libogg-dev libass libass-dev libvpx-dev libvorbis-dev libwebp-dev libtheora-dev libtool openssl opus-dev perl pkgconf pkgconfig python rtmpdump-dev wget x264-dev x265-dev yasm

# Install fdk-aac from testing.
RUN echo http://dl-cdn.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories && \
  apk add --update fdk-aac-dev

# Build libaom for av1.
RUN mkdir -p /tmp/aom && cd /tmp/ && \
  wget https://aomedia.googlesource.com/aom/+archive/${AOM_VERSION}.tar.gz && \
  tar zxf ${AOM_VERSION}.tar.gz && rm ${AOM_VERSION}.tar.gz && \
  rm -rf CMakeCache.txt CMakeFiles && \
  mkdir -p ./aom_build && \
  cd ./aom_build && \
  cmake -DCMAKE_INSTALL_PREFIX="${PREFIX}" -DBUILD_SHARED_LIBS=1 .. && \
  make && make install

# Get ffmpeg source.
RUN cd /tmp/ && \
  wget https://ffmpeg.org/releases/${FFMPEG_VERSION} && \
  tar xjvf ${FFMPEG_VERSION} && rm ${FFMPEG_VERSION}

# Compile ffmpeg.
RUN cd /tmp/ffmpeg && \
  ./configure \
  --enable-version3 \
  --enable-gpl \
  --enable-nonfree \
  --enable-small \
  --enable-libaom \
  --enable-libmp3lame \
  --enable-libx264 \
  --enable-libx265 \
  --enable-libvpx \
  --enable-libtheora \
  --enable-libvorbis \
  --enable-libopus \
  --enable-libfdk-aac \
  --enable-libass \
  --enable-libwebp \
  --enable-librtmp \
  --enable-postproc \
  --enable-avresample \
  --enable-libfreetype \
  --enable-openssl \
  --enable-avutil \
  --enable-avformat \
  --enable-avcodec \
  --disable-debug \
  --disable-doc \
  --disable-ffplay \
  --extra-cflags="-I${PREFIX}/include" \
  --extra-ldflags="-L${PREFIX}/lib" \
  --extra-libs="-lpthread -lm" \
  --prefix="${PREFIX}" && \
  make && make install && make distclean

# Cleanup.
RUN rm -rf /var/cache/apk/* /tmp/*

FROM alpine:3.8
ENV PATH=/opt/ffmpeg/bin:$PATH

RUN apk add --update ca-certificates openssl pcre lame libogg libass libvpx libvorbis libwebp libtheora opus rtmpdump x264-dev x265-dev

COPY --from=build /opt/ffmpeg /opt/ffmpeg
COPY --from=build /opt/ffmpeg/lib64/libaom.so.0 /usr/lib/libaom.so.0
COPY --from=build /usr/lib/libfdk-aac.so.2 /usr/lib/libfdk-aac.so.2

# End of ffmpeg

VOLUME /config
VOLUME /poll
VOLUME /downloads
VOLUME /transcode

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