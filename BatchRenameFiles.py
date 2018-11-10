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

"""Batch files renaming script."""

import os
import csv
import logging
import argparse
import subprocess

# Command line argument validation functions...
def is_valid_directory(parser, arg):
    "Function for checking specfied directory exists or not."
    if not os.path.isdir(arg):
        parser.error('The directory {} does not exist!'.format(arg))
    return arg

def is_valid_logging_status(parser, arg):
    "Function for checking logging status is valid or not."
    if not (arg == 'on' or arg == 'off'):
        parser.error('{} is not a valid input for turning logging on or off! Please specify \"on\" for turning logging on and \"off\" for turning logging off.'.format(arg))
    return arg

## =========> Command line arguments parsing -- starts <========= ##
PARSER = argparse.ArgumentParser(description='Batch renaming files utility...')
PARSER.add_argument('-s', '--source_directory', help='Directory to read input files.', required=True, metavar='<Source Directory>', type=lambda x: is_valid_directory(PARSER, x))
PARSER.add_argument('-f', '--filename', help='Desired output file name.', required=True, metavar='<Output file names>')
PARSER.add_argument('-l', '--log_file', help='Path of the log file.', metavar='<Log File>')
PARSER.add_argument('-ls', '--logging_onoff', help='Logging status On/Off', metavar='<Logging on/off>', type=lambda x: is_valid_logging_status(PARSER, x))
ARGS = PARSER.parse_args()
## =========> Command line arguments parsing -- ends <========= ##


## =========> Logging Configurations -- starts <========= ##
LOGGER_FILE = ARGS.log_file
LOGGING_STATUS = ARGS.logging_onoff

if not LOGGER_FILE:
    LOG_FILE = '/tmp/DirStats.log'
else:
    LOG_FILE = LOGGER_FILE + ".log"

# create logger
LOGGER = logging.getLogger('DirStats')
LOGGER.setLevel(logging.DEBUG)

# Turning logging on or off
if LOGGING_STATUS:
    if LOGGING_STATUS == 'off':
        LOGGER.disabled = True
    else:
        LOGGER.disabled = False
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
OUT_FILENAME = ARGS.filename
TMP_FILE = '/tmp/renameIM.txt'
DEVNULL = open('/dev/null', 'w')

# ls | sort --version-sort -f
def tmp_file():
    '''Function for listing and sorting the files.'''
    filter_call = subprocess.Popen(['ls', FILEPATH], stdout=subprocess.PIPE)
    sort_cmd = subprocess.Popen(['sort', '--version-sort', '-f'], stdin=filter_call.stdout, stdout=subprocess.PIPE)
    subprocess.Popen(['tee', TMP_FILE], stdin=sort_cmd.stdout, stdout=DEVNULL)
    sort_cmd.stdout.close()
    subprocess.call(['cat', 'tmpfile'])


def main():
    '''Start execution of the main program.'''
    i = 0
    counter = 1
    file_name = ""
    tmp_file()
    with open(TMP_FILE, 'r') as open_file:
        reader = csv.reader(open_file, delimiter=' ')
        for row in reader:
            path_row = row[0:]
            length = len(path_row)
            if i < length:
                for fpath in path_row:
                    file_name = file_name + " " + path_row[i]
                    i = i + 1
            file_name = file_name.strip()
            ext_name = os.path.basename(file_name).split(".")[1]
            imgpath = FILEPATH + "/" + file_name
            LOGGER.info("Renaming file %s", imgpath)
            os.rename(imgpath, FILEPATH + "/" + OUT_FILENAME + " (" + str(counter) + ")." + ext_name)
            i = 0
            file_name = ""
            counter = counter + 1


# Executing the script.
if __name__ == "__main__":
    main()
