FROM archlinux
MAINTAINER GalaxyMedia

VOLUME /config
VOLUME /poll
VOLUME /downloads
VOLUME /transcode


# Update Pacman
RUN pacman --noconfirm -Syu

# Install Git & Curl
RUN pacman --noconfirm -S git curl

# Install MP4 Automator
RUN git clone https://github.com/mdhiggins/sickbeard_mp4_automator.git /opt/mp4_automator
RUN pacman --noconfirm -S python python-setuptools python-pip gcc ffmpeg

RUN pip install --upgrade pip setuptools requests requests[security] requests-cache babelfish "guessit<2" "subliminal<2" qtfaststart pthon-qbittorrent deluge-client wheel loguru
# As per https://github.com/mdhiggins/sickbeard_mp4_automator/issues/643
ONBUILD RUN pip uninstall stevedore
ONBUILD RUN pip install stevedore==1.19.1
RUN ln -s /config/autoProcess.ini /opt/mp4_automator/autoProcess.ini
RUN ln -s /config/logs/mp4_automator /var/log/sickbeard_mp4_automator

# Install nzbToMedia
RUN pacman --noconfirm -S p7zip unrar wget unzip tar
RUN git clone https://github.com/clinton-hall/nzbToMedia.git /opt/nzbtomedia
RUN ln -s /config/autoProcessMedia.cfg /opt/nzbtomedia/autoProcessMedia.cfg

# Install poller preqs
# RUN pacman --noconfirm -S python python-pip
# RUN pip3 install --upgrade pip setuptools wheel loguru

COPY poller /
RUN chmod +x /poller

COPY post_sickrage.py /config/post_sickrage.py

RUN (crontab -l 2>/dev/null; echo "*/1 * * * * /poller") | crontab -

RUN pacman --noconfirm -Scc

#Adding Custom files
#ADD init/ /etc/my_init.d/
#RUN chmod -v +x /etc/my_init.d/*.sh

ENTRYPOINT ["/poller"]