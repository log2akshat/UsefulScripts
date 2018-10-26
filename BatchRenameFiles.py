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
    else:
        # File exists so return the directory
        return arg

## =========> Command line arguments parsing -- starts <========= ##
parser = argparse.ArgumentParser(description='Batch renaming files utility...')
parser.add_argument('-s', '--source_directory', help='Directory to read input files.', required=True, metavar='<Source Directory>', type=lambda x: is_valid_directory(parser, x))
parser.add_argument('-f', '--filename', help='Desired output file name.', required=True, metavar='<Output file names>')
parser.add_argument('-l', '--log_file', help='Path of the log file.', metavar='<Log File>')
parser.add_argument('-ls', '--logging_onoff', help='Logging status On/Off', metavar='<Logging on/off>', type=lambda x: is_valid_loggingStatus(parser, x))
ARGS = parser.parse_args()
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

filepath = ARGS.source_directory
outfileName = ARGS.filename
tmpFile = '/tmp/renameIM.txt'
devnull = open('/dev/null', 'w')

file = []
# ls | sort --version-sort -f
filterCall = subprocess.Popen(['ls', filepath],stdout=subprocess.PIPE)
sortCmd = subprocess.Popen(['sort', '--version-sort', '-f'], stdin=filterCall.stdout, stdout=subprocess.PIPE)
teeCmd = subprocess.Popen(['tee', tmpFile], stdin=sortCmd.stdout, stdout=devnull)
sortCmd.stdout.close()
subprocess.call(['cat', 'tmpfile'])

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
                extName = os.path.basename(fileName).split(".")[1]
		imgpath = filepath + "/" + fileName
		#print "Renaming " + imgpath + "..."
		LOGGER.info("Renaming file %s" % imgpath)
                os.rename(imgpath, filepath + "/" + outfileName + " (" + str(counter) + ")." + extName)
		i = 0
		fileName = ""
		counter = counter + 1
