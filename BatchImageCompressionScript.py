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
parser = argparse.ArgumentParser(description='Batch image conversion utility. For running this program you need to have imagemagick installed om your machine.')
parser.add_argument('-s','--source_directory', help='Directory to read input files.', required=True, metavar='<Source Directory>', type=lambda x: is_valid_directory(parser, x))
parser.add_argument('-t','--target_directory', help='Directory to save output files.', required=True, metavar='<Target Directory>', type=lambda x: is_valid_directory(parser, x))
parser.add_argument('-q','--quality', help='Quality of the Image to reatin.', required=True, metavar='<Image Quality>')
parser.add_argument('-f','--filename', help='Desired output file name.', required=True, metavar='<Output file names>')
args = parser.parse_args()

## =========> Command line arguments parsing -- ends <========= ##


## =========> Logging Configurations -- starts <========= ##
loggerFile = args.log_file
loggingStatus = args.logging_onoff

if not loggerFile:
    Log_File = '/tmp/BatchImageCompression.log'
else:
    Log_File = loggerFile + ".log"

# create logger
logger = logging.getLogger('BIC')
logger.setLevel(logging.DEBUG)

# Turning logging on or off
if loggingStatus:
    if loggingStatus == 'off':
        logger.disabled = True
    else:
        logger.disabled = False
else:
    logger.disabled = False

# add a file handler
fileHandler = logging.FileHandler(Log_File)
fileHandler.setLevel(logging.DEBUG)

# create console handler and set level to debug
consoleHandler = logging.StreamHandler()
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

filepath = args.source_directory
targetDir = args.target_directory
outfileName = args.filename
quality = args.quality
tmpFile = '/tmp/batchIM.txt'
devnull = open('/dev/null', 'w')

file = []
filterCall = subprocess.Popen(['ls', filepath],stdout=subprocess.PIPE)
#tailCmd = subprocess.Popen(['tail', '-n+2'], stdin=filterCall.stdout, stdout=subprocess.PIPE)
sortCmd = subprocess.Popen(['sort', '--version-sort', '-f'], stdin=filterCall.stdout, stdout=subprocess.PIPE)
#awkCmd = subprocess.Popen(['awk', '{print substr($0,index($0,$9))}'], stdin=tailCmd.stdout, stdout=subprocess.PIPE)
#teeCmd = subprocess.Popen(['tee', tmpFile], stdin=awkCmd.stdout, stdout=devnull)
teeCmd = subprocess.Popen(['tee', tmpFile], stdin=sortCmd.stdout, stdout=devnull)
sortCmd.stdout.close()

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
				#print "i : " + str(pathRow[i])
				i = i + 1
		fileName = fileName.strip()
		#print "pathRow : " + str(fileName) + " :: " + str(pathRow) + " :: " + str(length)
		imgpath = filepath + "/" + fileName
		print "Resizing " + imgpath + "..."
		subprocess.call(['convert', imgpath, '-quality', quality, targetDir + '/' + outfileName + ' ' + str(counter) + '.jpg'])
		i = 0
		fileName = ""
		counter = counter + 1
