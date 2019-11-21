#!/usr/bin/env python

import os

sonarr_eventtype = os.environ['sonarr_eventtype']
sonarr_isupgrade = os.environ['sonarr_isupgrade']
sonarr_series_id = os.environ['sonarr_series_id']
sonarr_series_title = os.environ['sonarr_series_title']
sonarr_series_path = os.environ['sonarr_series_path']
sonarr_series_tvdbid = os.environ['sonarr_series_tvdbid']
sonarr_series_tvmazeid = os.environ['sonarr_series_tvmazeid']
sonarr_series_imdb = os.environ['sonarr_series_imdb']
sonarr_series_type = os.environ['sonarr_series_type']
sonarr_episodefile_id = os.environ['sonarr_episodefile_id']
sonarr_episodefile_relativepath = os.environ['sonarr_episodefile_relativepath']
sonarr_episodefile_path = os.environ['sonarr_episodefile_path']
sonarr_episodefile_episodecount = os.environ['sonarr_episodefile_episodecount']
sonarr_episodefile_seasonnumber = os.environ['sonarr_episodefile_seasonnumber']
sonarr_episodefile_episodenumbers = os.environ['sonarr_episodefile_episodenumbers']
sonarr_episodefile_episodeairdates = os.environ['sonarr_episodefile_episodeairdates']
sonarr_episodefile_episodeairdatesutc = os.environ['sonarr_episodefile_episodeairdatesutc']
sonarr_episodefile_episodetitles = os.environ['sonarr_episodefile_episodetitles']
sonarr_episodefile_quality = os.environ['sonarr_episodefile_quality']
sonarr_episodefile_qualityversion = os.environ['sonarr_episodefile_qualityversion']
sonarr_episodefile_releasegroup = os.environ['sonarr_episodefile_releasegroup']
sonarr_episodefile_scenename = os.environ['sonarr_episodefile_scenename']
sonarr_episodefile_sourcepath = os.environ['sonarr_episodefile_sourcepath']
sonarr_episodefile_sourcefolder = os.environ['sonarr_episodefile_sourcefolder']
sonarr_deletedrelativepaths = os.environ['sonarr_deletedrelativepaths']
sonarr_deletedpaths = os.environ['sonarr_deletedpaths']
sonarr_download_id = int(os.environ['sonarr_download_id'])

with open('/downloads/process/poll/n%s.sonarr' % (sonarr_episodefile_id,), 'w') as f:
    f.write('%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s' % (sonarr_eventtype, sonarr_isupgrade, sonarr_series_id, sonarr_series_title, sonarr_series_path, sonarr_series_tvdbid, sonarr_series_tvmazeid, sonarr_series_imdb, sonarr_series_type, sonarr_episodefile_id, sonarr_episodefile_relativepath, sonarr_episodefile_path, sonarr_episodefile_episodecount, sonarr_episodefile_seasonnumber, sonarr_episodefile_episodenumbers, sonarr_episodefile_episodeairdates, sonarr_episodefile_episodeairdatesutc, sonarr_episodefile_episodetitles, sonarr_episodefile_quality, sonarr_episodefile_qualityversion, sonarr_episodefile_releasegroup, sonarr_episodefile_scenename, sonarr_episodefile_sourcepath, sonarr_episodefile_sourcefolder, sonarr_deletedrelativepaths, sonarr_deletedpaths, sonarr_download_id))
