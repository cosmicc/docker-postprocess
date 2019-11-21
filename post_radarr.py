#!/usr/bin/env python

import os

try:
    radarr_eventtype = os.environ['radarr_eventtype']
except KeyError:
    radarr_eventtype = ''
try:
    radarr_isupgrade = os.environ['radarr_isupgrade']
except KeyError:
    radarr_isupgrade = ''
try:
    radarr_movie_id = os.environ['radarr_movie_id']
except KeyError:
    radarr_movie_id = ''
try:
    radarr_movie_title = os.environ['radarr_movie_title']
except KeyError:
    radarr_movie_title = ''
try:
    radarr_movie_path = os.environ['radarr_movie_path']
except KeyError:
    radarr_movie_path = ''
try:
    radarr_movie_imdbid = os.environ['radarr_movie_imdbid']
except KeyError:
    radarr_movie_imdbid = ''
try:
    radarr_moviefile_id = os.environ['radarr_moviefile_id']
except KeyError:
    radarr_moviefile_id = ''
try:
    radarr_moviefile_relativepath = os.environ['radarr_moviefile_relativepath']
except KeyError:
    radarr_moviefile_relativepath = ''
try:
    radarr_moviefile_path = os.environ['radarr_moviefile_path']
except KeyError:
    radarr_moviefile_path = ''
try:
    radarr_moviefile_quality = os.environ['radarr_moviefile_quality']
except KeyError:
    radarr_moviefile_quality = ''
try:
    radarr_moviefile_qualityversion = os.environ['radarr_moviefile_qualityversion']
except KeyError:
    radarr_moviefile_qualityversion = ''
try:
    radarr_moviefile_releasegroup = os.environ['radarr_moviefile_releasegroup']
except KeyError:
    radarr_moviefile_releasegroup = ''
try:
    radarr_moviefile_scenename = os.environ['radarr_moviefile_scenename']
except KeyError:
    radarr_moviefile_scenename = ''
try:
    radarr_moviefile_sourcepath = os.environ['radarr_moviefile_sourcepath']
except KeyError:
    radarr_moviefile_sourcepath = ''
try:
    radarr_moviefile_sourcefolder = os.environ['radarr_moviefile_sourcefolder']
except KeyError:
    radarr_moviefile_sourcefolder = ''
try:
    radarr_download_id = os.environ['radarr_download_id']
except KeyError:
    radarr_download_id = ''

with open('/downloads/process/poll/n%s.radarr' % (radarr_moviefile_id,), 'w') as f:
    f.write('%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s' % (radarr_eventtype, radarr_isupgrade, radarr_movie_id, radarr_movie_title, radarr_movie_path, radarr_movie_imdbid, radarr_moviefile_id, radarr_moviefile_relativepath, radarr_moviefile_path, radarr_moviefile_quality, radarr_moviefile_qualityversion, radarr_moviefile_releasegroup, radarr_moviefile_scenename, radarr_moviefile_sourcepath, radarr_moviefile_sourcefolder, radarr_download_id))
