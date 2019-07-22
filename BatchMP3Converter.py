#    Copyright (C) <2016>  <Akshat Singh>
#    <akshat-pg8@iiitmk.ac.in>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Script for converting mp4 to mp3 in batch mode."""

import os
import sys
import logging
import argparse
import subprocess

# Command line argument validation functions...
def is_valid_directory(parser, arg):
    "Function for checking specfied directory exists or not."
    if not os.path.isdir(arg):
        parser.error('The directory {} does not exist!'.format(arg))
    else:
        # File exists so return the directory
        return arg

def is_target_directory(arg):
    "Function for checking specfied directory exists or not."
    if not os.path.isdir(arg):
        print('The directory %s does not exist!, so creating it for you..' % arg)
        try:
        	subprocess.call(['mkdir', '-p', arg])
        	return arg
        except:
        	parser.error('The directory {} does not exist and unable to create for you, please create it manually!'.format(arg))
    else:
        # File exists so return the directory
        return arg

def is_valid_logging_status(parser, arg):
    "Function for checking logging status is valid or not."
    if not (arg == 'on' or arg == 'off'):
        parser.error('{} is not a valid input for turning logging on or off! Please specify \"on\" for turning logging on and \"off\" for turning logging off.'.format(arg))
    return arg


## =========> Command line arguments parsing -- starts <========= ##
parser = argparse.ArgumentParser(description='Batch mp4 to mp3 conversion utility. For running this program you need to have FFMPEG with mp3 codecs installed on your machine.')
parser.add_argument('-s', '--source_directory', help='Directory to read input video files.', required=True, metavar='<Source Directory>', type=lambda x: is_valid_directory(parser, x))
parser.add_argument('-t', '--target_directory', help='Directory to save output converted mp3 files.', required=True, metavar='<Target Directory>', type=lambda x: is_target_directory(x))
parser.add_argument('-l', '--log_file', help='Path of the log file.', metavar='<Log File>')
parser.add_argument('-ls', '--logging_onoff', help='Logging status On/Off', metavar='<Logging on/off>', type=lambda x: is_valid_logging_status(parser, x))
ARGS = parser.parse_args()

## =========> Command line arguments parsing -- ends <========= ##


## =========> Logging Configurations -- starts <========= ##
loggerFile = ARGS.log_file
loggingStatus = ARGS.logging_onoff

if not loggerFile:
    LOG_FILE = '/tmp/BatchMP3Converter.log'
else:
    LOG_FILE = loggerFile + ".log"

# create logger
logger = logging.getLogger('BMP3C')
logger.setLevel(logging.DEBUG)

# Turning logging on or off
if loggingStatus:
    logger.disabled = bool(loggingStatus == 'off')
else:
    logger.disabled = False

# add a file handler
fileHandler = logging.FileHandler(LOG_FILE)
fileHandler.setLevel(logging.DEBUG)

# create console handler and set level to debug
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# add formatter to handlers
fileHandler.setFormatter(formatter)
consoleHandler.setFormatter(formatter)

# add ch to logger
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

## =========> Logging Configurations -- ends <========= ##

SRC_DIR = os.path.join(ARGS.source_directory, '')
TARGET_DIR = ARGS.target_directory


def mp3_conversion(song_path, conversion_path, song_name):
    '''Function to convert the mp4 song to a mp3 file.'''
    song = conversion_path + "/" +  song_name + ".mp3"
    logger.info("Going to convert %s song.." % song)
    cmd = subprocess.Popen(['ffmpeg', '-i', song_path, '-codec:a', 'libmp3lame', '-qscale:a', '2', conversion_path + "/" + song_name + '.mp3'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    tee = subprocess.Popen(['tee', '-a', LOG_FILE], stdin=cmd.stdout)
    cmd.stdout.close()
    tee.communicate()


def all_file_paths():
    '''Function to get list of all the files in the source directories.'''
    file_paths = []
    for root, directories, files in os.walk(SRC_DIR):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths


def main():
    '''Main function'''
    slash_count = 0
    conversion_path = ""
    src_dir_modified = SRC_DIR
    for audio_song_path in all_file_paths():
        song_name = os.path.basename(audio_song_path).split(".mp4")[0]
        #print os.path.dirname(audio_song_path)
        if SRC_DIR.endswith('/'):
            src_dir_modified = SRC_DIR[:-1]
            slash_count = src_dir_modified.count('/')
            groups = os.path.dirname(audio_song_path).split('/') # Retrieving the full path from a path except filename
            # Comparing and removing the source directory path.
            conversion_path = TARGET_DIR + "/" + '/'.join(groups[slash_count:])
            if not os.path.exists(conversion_path): # Create conversion path directory if it doesn't exists.
                logger.info("Going to create %s subdirectory.." % conversion_path)
                os.makedirs(conversion_path)
        mp3_conversion(audio_song_path, conversion_path, song_name)


if __name__ == "__main__":
    main()
