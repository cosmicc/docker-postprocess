# docker-postprocess
Docker image for remote postprocessing downloaded videos with MP4_Automator and nzbToMedia

This is a Alpine linux base docker image with MP4_Automator and nzbToMedia to be executed over SSH from your downloader (Deluge, Qbittorrent, etc..)

This image is different from other postprocessors, it does NOT have any downloaders built in.  It is made to run as a seperate docker image (from your downloaders and media managers) that will recieve completed download postprocess command over SSH to process the completed download.  It will then (built into MP4_automator and nzbToMedia) after transcoding, notify and complete the video to your media manager (Sonarr, Sickrage, Radarr, etc).

Volumes: 
    /config - used to store all config files (MP4_Automator, nzbToMedia) and public ssh key (for passwordless ssh from downloader)
    /downloads - location where your download stores all completed downloads (must be same path as downloader)
    /transcode = used as temporary directory for transcoding video files
    
Ports:
    5100 - cert only SSH port for downloader and media managers to send postprocess commands
    
* You will need to copy the generated Public SSH keyfile to your systems that will SSH commands to this postprocessor.  Keyfile is located in /config/ssh

* The downloaded video locations on your downloader and media manager docker containers must have the same path to the video files that this images has.
    
* The completed download script that you add to your downloader will need the ssh prepended to it: 
ssh root@mydownloader_host -p 5100 /opt/mp4_automator/qBittorrentPostProcess.py "%L" "%T" "%R" "%F" "%N" "%I"
