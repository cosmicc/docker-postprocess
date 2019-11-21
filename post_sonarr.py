#!/usr/bin/env python

import os

try:
    sonarr_eventtype = os.environ['sonarr_eventtype']
except KeyError:
    sonarr_eventtype = ''
try:
    sonarr_isupgrade = os.environ['sonarr_isupgrade']
except KeyError:
    sonarr_isupgrade = ''
try:
    sonarr_series_id = os.environ['sonarr_series_id']
except KeyError:
    sonarr_series_id = ''
try:
    sonarr_series_title = os.environ['sonarr_series_title']
except KeyError:
    sonarr_series_title = ''
try:
    sonarr_series_path = os.environ['sonarr_series_path']
except KeyError:
    sonarr_eventtype = ''
try:
    sonarr_series_tvdbid = os.environ['sonarr_series_tvdbid']
except KeyError:
    sonarr_series_tvdbid = ''
try:
    sonarr_series_tvmazeid = os.environ['sonarr_series_tvmazeid']
except KeyError:
    sonarr_series_tvmazeid = ''
try:
    sonarr_series_imdb = os.environ['sonarr_series_imdb']
except KeyError:
    sonarr_series_imdb = ''
try:
    sonarr_series_type = os.environ['sonarr_series_type']
except KeyError:
    sonarr_series_type = ''
try:
    sonarr_episodefile_id = os.environ['sonarr_episodefile_id']
except KeyError:
    sonarr_episodefile_id = ''
try:
    sonarr_episodefile_relativepath = os.environ['sonarr_episodefile_relativepath']
except KeyError:
    sonarr_episodefile_relativepath = ''
try:
    sonarr_episodefile_path = os.environ['sonarr_episodefile_path']
except KeyError:
    sonarr_episodefile_path = ''
try:
    sonarr_episodefile_episodecount = os.environ['sonarr_episodefile_episodecount']
except KeyError:
    sonarr_episodefile_episodecount = ''
try:
    sonarr_episodefile_seasonnumber = os.environ['sonarr_episodefile_seasonnumber']
except KeyError:
    sonarr_episodefile_seasonnumber = ''
try:
    sonarr_episodefile_episodenumbers = os.environ['sonarr_episodefile_episodenumbers']
except KeyError:
    sonarr_episodefile_episodenumbers = ''
try:
    sonarr_episodefile_episodeairdates = os.environ['sonarr_episodefile_episodeairdates']
except KeyError:
    sonarr_episodefile_episodeairdates = ''
try:
    sonarr_episodefile_episodeairdatesutc = os.environ['sonarr_episodefile_episodeairdatesutc']
except KeyError:
    sonarr_episodefile_episodeairdatesutc = ''
try:
    sonarr_episodefile_episodetitles = os.environ['sonarr_episodefile_episodetitles']
except KeyError:
    sonarr_episodefile_episodetitles = ''
try:
    sonarr_episodefile_quality = os.environ['sonarr_episodefile_quality']
except KeyError:
    sonarr_episodefile_quality = ''
try:
    sonarr_episodefile_qualityversion = os.environ['sonarr_episodefile_qualityversion']
except KeyError:
    sonarr_episodefile_qualityversion = ''
try:
    sonarr_episodefile_releasegroup = os.environ['sonarr_episodefile_releasegroup']
except KeyError:
    sonarr_episodefile_releasegroup = ''
try:
    sonarr_episodefile_scenename = os.environ['sonarr_episodefile_scenename']
except KeyError:
    sonarr_episodefile_scenename = ''
try:
    sonarr_episodefile_sourcepath = os.environ['sonarr_episodefile_sourcepath']
except KeyError:
    sonarr_episodefile_sourcepath = ''
try:
    sonarr_episodefile_sourcefolder = os.environ['sonarr_episodefile_sourcefolder']
except KeyError:
    sonarr_episodefile_sourcefolder = ''
try:
    sonarr_deletedrelativepaths = os.environ['sonarr_deletedrelativepaths']
except KeyError:
    sonarr_deletedrelativepaths = ''
try:
    sonarr_deletedpaths = os.environ['sonarr_deletedpaths']
except KeyError:
    sonarr_deletedpaths = ''
try:
    sonarr_download_id = os.environ['sonarr_download_id']
except KeyError:
    sonarr_download_id = ''

with open('/downloads/process/poll/n%s.sonarr' % (sonarr_episodefile_id,), 'w') as f:
    f.write('%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s' % (sonarr_eventtype, sonarr_isupgrade, sonarr_series_id, sonarr_series_title, sonarr_series_path, sonarr_series_tvdbid, sonarr_series_tvmazeid, sonarr_series_imdb, sonarr_series_type, sonarr_episodefile_id, sonarr_episodefile_relativepath, sonarr_episodefile_path, sonarr_episodefile_episodecount, sonarr_episodefile_seasonnumber, sonarr_episodefile_episodenumbers, sonarr_episodefile_episodeairdates, sonarr_episodefile_episodeairdatesutc, sonarr_episodefile_episodetitles, sonarr_episodefile_quality, sonarr_episodefile_qualityversion, sonarr_episodefile_releasegroup, sonarr_episodefile_scenename, sonarr_episodefile_sourcepath, sonarr_episodefile_sourcefolder, sonarr_deletedrelativepaths, sonarr_deletedpaths, sonarr_download_id))
