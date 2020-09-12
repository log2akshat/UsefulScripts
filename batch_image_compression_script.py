#    Copyright (C) <2015>  <Akshat Singh>
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

"""Batch image compression utility."""

from __future__ import print_function
import os
import csv
import logging
import argparse
import platform
import subprocess

# Command line argument validation functions...
def is_valid_directory(parser, arg):
    "Function for checking specfied directory exists or not."
    if not os.path.isdir(arg):
        parser.error('The directory {} does not exist!'.format(arg))
    # File exists so return the directory
    return arg

def is_target_directory(parser, arg):
    "Function for checking specfied directory exists or not."
    if not os.path.isdir(arg):
        print('The directory %s does not exist!, so creating it for you..' % arg)
        try:
            subprocess.call(['mkdir', '-p', arg])
            return arg
        except:
            parser.error('The directory {} does not exist and unable to create for you, please create it manually!'.format(arg))
    # File exists so return the directory
    return arg

def is_valid_logging_status(parser, arg):
    "Function for checking logging status is valid or not."
    if not arg in ('on', 'off'):
        parser.error('{} is not a valid input for turning logging on or off! Please specify \"on\" for turning logging on and \"off\" for turning logging off.'.format(arg))
    return arg


## =========> Command line arguments parsing -- starts <========= ##
PARSER = argparse.ArgumentParser(description='Batch image compression utility. For running this program you need to have imagemagick installed on your machine.')
PARSER.add_argument('-s', '--source_directory', help='Directory to read input files.', required=True, metavar='<Source Directory>', type=lambda x: is_valid_directory(PARSER, x))
PARSER.add_argument('-t', '--target_directory', help='Directory to save output files.', required=True, metavar='<Target Directory>', type=lambda x: is_target_directory(PARSER, x))
PARSER.add_argument('-q', '--quality', help='Quality of the Image to retain.', required=True, metavar='<Image Quality>')
PARSER.add_argument('-f', '--filename', help='Desired output file name.', metavar='<Output file names>')
PARSER.add_argument('-l', '--log_file', help='Path of the log file.', metavar='<Log File>')
PARSER.add_argument('-ls', '--logging_onoff', help='Logging status On/Off', metavar='<Logging on/off>', type=lambda x: is_valid_logging_status(PARSER, x))
ARGS = PARSER.parse_args()

## =========> Command line arguments parsing -- ends <========= ##

subprocess.call('clear')

## =========> Logging Configurations -- starts <========= ##
LOGGER_FILE = ARGS.log_file
LOGGING_STATUS = ARGS.logging_onoff

if not LOGGER_FILE:
    LOG_FILE = '/tmp/BatchImageCompression.log'
else:
    LOG_FILE = LOGGER_FILE + ".log"

# create logger
LOGGER = logging.getLogger('BIC')
LOGGER.setLevel(logging.DEBUG)

# Turning logging on or off
if LOGGING_STATUS:
    LOGGER.disabled = bool(LOGGING_STATUS == 'off')
else:
    LOGGER.disabled = False

# add a file handler
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)

# create console handler and set level to debug
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)

# create formatter
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# add formatter to handlers
FILE_HANDLER.setFormatter(FORMATTER)
CONSOLE_HANDLER.setFormatter(FORMATTER)

# add ch to logger
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)

## =========> Logging Configurations -- ends <========= ##


FILEPATH = ARGS.source_directory
TARGET_DIR = ARGS.target_directory
OUT_FILENAME = ARGS.filename
QUALITY = ARGS.quality
TMP_FILE = '/tmp/batchIM.txt'
DEV_NULL = open('/dev/null', 'w')


def processing_file():
    '''Function to create a temporary file for processing.'''
    filter_call = subprocess.Popen(['ls', FILEPATH], stdout=subprocess.PIPE)
    #tailCmd = subprocess.Popen(['tail', '-n+2'], stdin=filter_call.stdout, stdout=subprocess.PIPE)
    if platform.system() == "Darwin":
        sort_cmd = subprocess.Popen(['sort', '-f'], stdin=filter_call.stdout, stdout=subprocess.PIPE)
    elif platform.system() == "Linux":
        sort_cmd = subprocess.Popen(['sort', '--version-sort', '-f'], stdin=filter_call.stdout, stdout=subprocess.PIPE)
    #awkCmd = subprocess.Popen(['awk', '{print substr($0,index($0,$9))}'], stdin=tailCmd.stdout, stdout=subprocess.PIPE)
    tee_cmd = subprocess.Popen(['tee', TMP_FILE], stdin=sort_cmd.stdout, stdout=DEV_NULL)
    sort_cmd.stdout.close()
    tee_cmd.communicate()


def main():
    """Main function"""
    processing_file()
    i = 0
    counter = 1
    file_name = ""
    with open(TMP_FILE, 'r') as tmp_file:
        reader = csv.reader(tmp_file, delimiter=' ')
        for row in reader:
            path_row = row[0:]
            length = len(path_row)
            if i < length:
                for elements in path_row:
                    file_name = file_name + " " + path_row[i]
                    i = i + 1
            file_name = file_name.strip()
            imgpath = FILEPATH + file_name
            LOGGER.info("Resizing Image : %s..", imgpath)
            if OUT_FILENAME:
                subprocess.call(['convert', imgpath, '-quality', QUALITY, str(TARGET_DIR) + '/' + str(OUT_FILENAME) + ' ' + str(counter) + '.jpg'])
            else:
                subprocess.call(['convert', imgpath, '-quality', QUALITY, str(TARGET_DIR) + '/' + file_name])
            i = 0
            file_name = ""
            counter = counter + 1


if __name__ == "__main__":
    main()
