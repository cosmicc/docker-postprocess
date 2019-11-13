# docker-postprocess
Docker image for remote postprocessing downloaded videos with MP4_Automator and nzbToMedia

This is a Alpine linux base docker image with MP4_Automator and nzbToMedia to remotely process files from your downloader (Deluge, Qbittorrent, etc..)

This image is different from other postprocessors, it does NOT have any downloaders built in.  It is made to run as a seperate docker image (from your downloaders and media managers) that will poll for completed downloads to postprocess.  It will then (built into MP4_automator and nzbToMedia) after transcoding, notify and complete the video to your media manager (Sonarr, Sickrage, Radarr, etc).

Volumes: 
    /config - used to store all config files (MP4_Automator, nzbToMedia)
    /downloads - location where your download stores all completed downloads (must be same path as downloader)
    /transcode - used as temporary directory for transcoding video files.
    /poll - directory it will watch for polling process trigger files created by the downloader torrent completion script.

* The downloaded video locations on your downloader and media manager docker containers must have the same path to the video files that this images has.
    
* The completed download script that you add to your downloader (that creates the process trigger file): echo "%L|%T|%R|%F|%N|%I" > "/poll/%N"

nzbToMedia not implimented yet.
