#!/usr/bin/env python3

'''
GalaxyMedia PlexDVR commercial detection and removal.
https://github.com/cosmicc/docker-postprocess
Modified from original: https://github.com/ekim1337/PlexComskip
'''

import argparse
import configparser
import os
import shutil
import subprocess
import sys
import tempfile
import uuid

from loguru import logger as logging

__name__ = 'COMSKIP'

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--ini', action='store', help='config file to use')
parser.add_argument('-i', '--input', action='store', help='input file')
args = parser.parse_args()

# Config stuff.
config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'PlexComskip.conf')
if not os.path.exists(config_file_path):
    print('Config file not found: %s' % config_file_path)
    print('Make a copy of PlexConfig.conf.example named PlexConfig.conf, modify as necessary, and place in the same directory as this script.')
    sys.exit(1)

config = configparser.SafeConfigParser({
    'temp-root': tempfile.gettempdir(),
    'comskip-root': tempfile.gettempdir(),
    'nice-level': '0'
})
config.read(config_file_path)

COMSKIP_PATH = os.path.expandvars(os.path.expanduser(config.get('Helper Apps', 'comskip-path')))

COMSKIP_INI_PATH = args.ini

FFMPEG_PATH = os.path.expandvars(os.path.expanduser(config.get('Helper Apps', 'ffmpeg-path')))
LOG_FILE_PATH = os.path.expandvars(os.path.expanduser(config.get('Logging', 'logfile-path')))
CONSOLE_LOGGING = config.getboolean('Logging', 'console-logging')
TEMP_ROOT = os.path.expandvars(os.path.expanduser(config.get('File Manipulation', 'temp-root')))
COMSKIP_ROOT = os.path.expandvars(os.path.expanduser(config.get('File Manipulation', 'comskip-root')))
COPY_ORIGINAL = config.getboolean('File Manipulation', 'copy-original')
SAVE_ALWAYS = config.getboolean('File Manipulation', 'save-always')
SAVE_FORENSICS = config.getboolean('File Manipulation', 'save-forensics')
NICE_LEVEL = config.get('Helper Apps', 'nice-level')
LOG_LEVEL = config.get('Logging', 'log-level')

# Exit states
CONVERSION_SUCCESS = 0
CONVERSION_DID_NOT_MODIFY_ORIGINAL = 1
CONVERSION_SANITY_CHECK_FAILED = 2
EXCEPTION_HANDLED = 3
COMSKIP_FAILED = 4

# Logging.
session_uuid = str(uuid.uuid4())
fmt = '%%(asctime)-15s [%s] %%(message)s' % session_uuid[:6]
if not os.path.exists(os.path.dirname(LOG_FILE_PATH)):
    os.makedirs(os.path.dirname(LOG_FILE_PATH))

logging.remove()

logformat = "{time:YYYY-MM-DD HH:mm:ss.SSS}|{name: <8}|{level: <7}| {message: <72}"
debuglogformat = "{time:YYYY-MM-DD HH:mm:ss.SSS}|{name}:{line}:{function}|{level: <7}| {message: <72}"

if LOG_LEVEL == "TRACE":
    lev = 5
    logf = debuglogformat
elif LOG_LEVEL == "DEBUG":
    lev = 10
    logf = debuglogformat
elif LOG_LEVEL == "INFO":
    lev = 20
    logf = logformat
elif LOG_LEVEL == "WARNING":
    lev = 30
    logf = logformat
else:
    lev = 40
    logf = logformat

logging.add(sys.stderr, level=lev, backtrace=True, diagnose=True, format=logf)
logging.add(sink=LOG_FILE_PATH, level=lev, buffering=1, enqueue=True, backtrace=True, diagnose=True, serialize=False, colorize=False, delay=False, format=logf)


# Human-readable bytes.
def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)


if len(sys.argv) < 2:
    print('Usage: PlexComskip.py input-file.mkv')
    os._exit(1)


# Clean up after ourselves and exit.
def cleanup_and_exit(temp_dir, keep_temp=False, exit_code=CONVERSION_SUCCESS):
    if keep_temp:
        logging.info('Leaving temp files in: %s, %s' % (temp_dir, comskip_out))
    else:
        try:
            shutil.rmtree(temp_dir)
            if temp_dir != comskip_out:
                shutil.rmtree(comskip_out)
        except:
            logging.exception('Problem whacking temp dirs: %s, %s' % (temp_dir, comskip_out))
            exit_code = EXCEPTION_HANDLED

    # Exit cleanly.
    logging.info('Finished comskip processing')
    os._exit(exit_code)


# On to the actual work.
try:
    video_path = os.path.abspath(args.input)
    temp_dir = os.path.join(TEMP_ROOT, session_uuid)
    comskip_out = os.path.join(COMSKIP_ROOT, session_uuid)
    os.makedirs(temp_dir)
    if temp_dir != comskip_out:
        os.makedirs(comskip_out)
    os.chdir(temp_dir)

    logging.debug('Using session ID: %s' % session_uuid)
    logging.debug('Using temp dir: %s' % temp_dir)
    logging.debug('Using comskip dir: %s' % comskip_out)
    logging.info('Using input file: %s' % video_path)

    output_video_dir = os.path.dirname(video_path)

    video_basename = os.path.basename(video_path)
    video_name, video_ext = os.path.splitext(video_basename)

except:
    logging.exception('Something went wrong setting up temp paths and working files:')
    sys.exit(EXCEPTION_HANDLED)

try:
    if COPY_ORIGINAL or SAVE_ALWAYS:
        temp_video_path = os.path.join(temp_dir, video_basename)
        input_size = os.path.getsize(os.path.abspath(video_path))
        logging.info('Copying file to workspace %s: %s' % (sizeof_fmt(input_size), temp_video_path))
        shutil.copy(video_path, temp_dir)
    else:
        temp_video_path = video_path

    # Process with comskip
    logging.info('Starting commercial skip detection and cut-file generation')
    cmd = [COMSKIP_PATH, '--output', comskip_out, '--ini', COMSKIP_INI_PATH, temp_video_path]
    logging.debug('[comskip] Command: %s' % cmd)
    comskip_status = subprocess.call(cmd)
    if comskip_status != 0:
        logging.warning('Comskip did not exit properly with code: %s' % comskip_status)
        cleanup_and_exit(temp_dir, False, COMSKIP_FAILED)
        # raise Exception('Comskip did not exit properly')

except:
    logging.exception('Something went wrong during comskip analysis:')
    cleanup_and_exit(temp_dir, SAVE_ALWAYS or SAVE_FORENSICS, EXCEPTION_HANDLED)

edl_file = os.path.join(comskip_out, video_name + '.edl')
logging.info('Generated EDL: ' + edl_file)
try:
    segments = []
    prev_segment_end = 0.0
    if os.path.exists(edl_file):
        with open(edl_file, 'rb') as edl:
            # EDL contains segments we need to drop, so chain those together into segments to keep.
            for segment in edl:
                start, end, something = segment.split()
                if float(start) == 0.0:
                    logging.info('* Start of file is junk, skipping this segment')
                elif float(start) - float(prev_segment_end) >= 3.0:
                    keep_segment = [float(prev_segment_end), float(start)]
                    logging.info('* Keeping segment from %s to %s' % (keep_segment[0], keep_segment[1]))
                    segments.append(keep_segment)
                else:
                    logging.info('* Segment too small to keep %s to %s' % (keep_segment[0], keep_segment[1]))
                prev_segment_end = end

    # Write the final keep segment from the end of the last commercial break to the end of the file.
    keep_last_segment = [float(prev_segment_end), -1]
    logging.info('* Keeping segment from %s to the end of the file.' % keep_last_segment[0])
    segments.append(keep_last_segment)

    segment_files = []
    segment_list_file_path = os.path.join(temp_dir, 'segments.txt')
    with open(segment_list_file_path, 'wb') as segment_list_file:
        for i, segment in enumerate(segments):
            segment_name = 'segment-%s' % i
            segment_file_name = '%s%s' % (segment_name, video_ext)
            if segment[1] == -1:
                duration_args = []
            else:
                duration_args = ['-t', str(segment[1] - segment[0])]
            cmd = [FFMPEG_PATH, '-i', temp_video_path, '-ss', str(segment[0])]
            cmd.extend(duration_args)
            cmd.extend(['-c', 'copy', segment_file_name])
            # cmd.extend([segment_file_name])
            logging.debug('[ffmpeg] Command: %s' % cmd)
            try:
                subprocess.call(cmd)
            except:
                logging.exception('Exception running ffmpeg:')
                cleanup_and_exit(temp_dir, SAVE_ALWAYS or SAVE_FORENSICS, EXCEPTION_HANDLED)

            # If the last drop segment ended at the end of the file, we will have written a zero-duration file.
            if os.path.exists(segment_file_name):
                if os.path.getsize(segment_file_name) < 1000:
                    logging.info('Last segment ran to the end of the file, not adding bogus segment %s for merge.' % (i + 1))
                else:
                    segment_files.append(segment_file_name)
                    sfn = f'file {segment_file_name}\n'.encode()
                    segment_list_file.write(sfn)

except:
    logging.exception('Something went wrong during splitting:')
    cleanup_and_exit(temp_dir, SAVE_ALWAYS or SAVE_FORENSICS, EXCEPTION_HANDLED)

logging.info('Merging %s files from the segment list.' % len(segment_files))
try:
    cmd = [FFMPEG_PATH, '-y', '-f', 'concat', '-i', segment_list_file_path, '-c', 'copy', os.path.join(temp_dir, video_basename)]
    logging.debug('[ffmpeg] Command: %s' % cmd)
    subprocess.call(cmd)

except:
    logging.exception('Something went wrong during concatenation:')
    cleanup_and_exit(temp_dir, SAVE_ALWAYS or SAVE_FORENSICS, EXCEPTION_HANDLED)

logging.info('Sanity checking comskipped file')
try:
    input_size = os.path.getsize(os.path.abspath(video_path))
    output_size = os.path.getsize(os.path.abspath(os.path.join(temp_dir, video_basename)))
    if input_size and 1.01 > float(output_size) / float(input_size) > 0.99:
        logging.warning('Output file size was too similar; we won\'t replace the original: %s -> %s' % (sizeof_fmt(input_size), sizeof_fmt(output_size)))
        cleanup_and_exit(temp_dir, SAVE_ALWAYS, CONVERSION_DID_NOT_MODIFY_ORIGINAL)
    elif input_size and 1.1 > float(output_size) / float(input_size) > 0.3:
        logging.success('Output file size looked good, we\'ll replace the original: %s -> %s' % (sizeof_fmt(input_size), sizeof_fmt(output_size)))
        logging.info('Copying the output: %s -> %s' % (video_basename, output_video_dir))
        shutil.copy(os.path.join(temp_dir, video_basename), output_video_dir)
        cleanup_and_exit(temp_dir, SAVE_ALWAYS)
    else:
        logging.warning('Output file size looked too big or too small; we won\'t replace the original: %s -> %s' % (sizeof_fmt(input_size), sizeof_fmt(output_size)))
        cleanup_and_exit(temp_dir, SAVE_ALWAYS or SAVE_FORENSICS, CONVERSION_SANITY_CHECK_FAILED)
except:
    logging.exception('Something went wrong during sanity check:')
    cleanup_and_exit(temp_dir, SAVE_ALWAYS or SAVE_FORENSICS, EXCEPTION_HANDLED)
