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
    if not (arg == 'on' or arg == 'off'):
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


filepath = ARGS.source_directory
targetDir = ARGS.target_directory
outfileName = ARGS.filename
quality = ARGS.quality
tmpFile = '/tmp/batchIM.txt'
devnull = open('/dev/null', 'w')


def processingFile():
    '''Function to create a temporary file for processing.'''
    filterCall = subprocess.Popen(['ls', filepath], stdout=subprocess.PIPE)
    #tailCmd = subprocess.Popen(['tail', '-n+2'], stdin=filterCall.stdout, stdout=subprocess.PIPE)
    if platform.system() == "Darwin":
        sortCmd = subprocess.Popen(['sort', '-f'], stdin=filterCall.stdout, stdout=subprocess.PIPE)
    elif platform.system() == "Linux":
        sortCmd = subprocess.Popen(['sort', '--version-sort', '-f'], stdin=filterCall.stdout, stdout=subprocess.PIPE)
    #awkCmd = subprocess.Popen(['awk', '{print substr($0,index($0,$9))}'], stdin=tailCmd.stdout, stdout=subprocess.PIPE)
    teeCmd = subprocess.Popen(['tee', tmpFile], stdin=sortCmd.stdout, stdout=devnull)
    sortCmd.stdout.close()
    teeCmd.communicate()


def main():
    processingFile()
    i = 0
    counter = 1
    fileName = ""
    pathfile = open(tmpFile, 'r')
    file = pathfile.read().splitlines()
    with open(tmpFile, 'r') as f:
	reader = csv.reader(f, delimiter=' ')
	for row in reader:
            pathRow = row[0:]
            length = len(pathRow)
            if i < length:
                for x in pathRow:
                    fileName = fileName + " " + pathRow[i]
                    i = i + 1
            fileName = fileName.strip()
            imgpath = filepath + fileName
            LOGGER.info("Resizing Image : %s.." % imgpath)
            if outfileName:
                subprocess.call(['convert', imgpath, '-quality', quality, str(targetDir) + '/' + str(outfileName) + ' ' + str(counter) + '.jpg'])
            else:
                 subprocess.call(['convert', imgpath, '-quality', quality, str(targetDir) + '/' + fileName])
            i = 0
            fileName = ""
            counter = counter + 1


if __name__ == "__main__":
    main()
