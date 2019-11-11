# docker-postprocess
Docker image for remote postprocessing with MP4_Automator and nzbToMedia

This is a Alpine linux base docker image with MP4_Automator and nzbToMedia to be executed over SSH from your downloader (Deluge, Qbittorrent, etc..)

This does NOT have any downloaders built in.  It is ment to run as a seperate docker image that will recieve completed downloads to process over SSH from your existing downloader.
