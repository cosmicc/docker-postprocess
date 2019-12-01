# docker-postprocess
Docker image for remote postprocessing downloaded videos from Deluge and PlexDVR

This image is different from other postprocessors, it does NOT have any downloaders built in.  It is made to run and transcode in a seperate docker container (from your downloaders and media managers).
It polls a directory for trigger files left by the scripts to postprocess videos.
It will remove commercials from Plex DVR videos and Transcode all videos (from PlexDVR and Deluge) to x264 suitable for Plex Direct Play. You must use Sonarr and Radarr's Drone factory processing for now (to pick up the completed post processed videos)

Docker Volumes:
    /config - used to store all config files and logs (MP4_Automator, Comskip)
    /downloads - location where deluge stores all completed downloads (must be same path as downloader)
    /transcode - used as temporary directory for transcoding and de-commercialing video files.
    /poll - directory it will watch for trigger files created by deluge completion script and Plex postprocess script.

* The downloaded video locations on your downloader and media manager docker containers must have the same path to the video files that this images has.

* Post Processing trigger scripts included must be added to Deluge and Plex

* PlexDVR postprocess script waits 24 hours for the completed post-processed video to appear from the transcoder before it fails.
