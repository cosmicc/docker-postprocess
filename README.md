# docker-postprocess
Docker image for remote postprocessing downloaded videos with MP4_Automator and nzbToMedia

This is a Alpine linux base docker image with MP4_Automator and nzbToMedia to be executed over SSH from your downloader (Deluge, Qbittorrent, etc..)

This image is different from other postprocessors, it does NOT have any downloaders built in.  It is made to run as a seperate docker image (from your downloaders and media managers) that will recieve completed download postprocess command over SSH to process the completed download.  It will then (built into MP4_automator and nzbToMedia) after transcoding, notify and complete the video to your media manager (Sonarr, Sickrage, Radarr, etc).
