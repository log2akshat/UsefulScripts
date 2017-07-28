#    Copyright (C) <2017>  <Akshat Singh>
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
import shutil
import logging
import argparse
import platform
import subprocess
from argparse import RawTextHelpFormatter

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

def is_valid_option(parser, arg):
    "Function for checking option is on or off."
    if not (arg == 'on' or arg == 'off'):
        parser.error('{} is not a valid input for turning option on or off! Please specify \"on\" for turning the option on and \"off\" for turning it off.'.format(arg))
    else:
        return arg
    

def is_valid_loggingStatus(parser, arg):
    "Function for checking logging status is valid or not."
    if not (arg == 'on' or arg == 'off'):
        parser.error('{} is not a valid input for turning logging on or off! Please specify \"on\" for turning logging on and \"off\" for turning logging off.'.format(arg))
    else:
        return arg

## =========> Command line arguments parsing -- starts <========= ##
parser = argparse.ArgumentParser(description='[Purpose - This script is useful in a situation where we want to run a compression only on specific camera make but not on others and later want to do some manual image processing using tools like gimp on some camera make images and also at the same time we also want to maintain the sequence of the images based on their capturing time not based on the image modification.]\n\n\n***********************************\n\nBatch Image Manager is an advaced version of the Batch Image Compression utility. For running this program you need to have exif tool and imagemagick installed on your machine. This program is used for mixing the various images taken from different camera make based on their capturing time in ascending order and rename each image on thir unix timestamp if the --filename is not provided on the command line.\n\nIf compression option is selected as OFF then this script wil not create any sub-directories based on camera make just it will arrange the pictures based on their capturing time. \n\n\n\t', formatter_class=RawTextHelpFormatter)
parser.add_argument('-i', '--info', help='Information about the Camera make and Model', metavar='<Camera Information>')
parser.add_argument('-s','--source_directory', help='Directory to read input files.', required=True, metavar='<Source Directory>', type=lambda x: is_valid_directory(parser, x))
parser.add_argument('-t','--target_directory', help='Directory to save output files.', required=True, metavar='<Target Directory>', type=lambda x: is_target_directory(x))
parser.add_argument('-cmp','--compression', help='Compression On/Off', required=True, metavar='<Compression on/off>', type=lambda x: is_valid_option(parser, x))
parser.add_argument('-clq','--compressionQuality', help='Quality of the Image to retain for specific Camera make [Image Quality range is 1-100].', metavar='<CameraMake_#ImageQuality Eg.: Canon100D_#90>')
parser.add_argument('-l','--log_file', help='Path of the log file.', metavar='<Log File>')
parser.add_argument('-ls', '--logging_onoff', help='Logging status On/Off', metavar='<Logging on/off>', type=lambda x: is_valid_loggingStatus(parser, x))
args = parser.parse_args()


## =========> Command line arguments parsing -- ends <========= ##

subprocess.call('clear')

## =========> Logging Configurations -- starts <========= ##
loggerFile = args.log_file
loggingStatus = args.logging_onoff

if not loggerFile:
    Log_File = '/tmp/BatchImageManager.log'
else:
    Log_File = loggerFile + ".log"

# create logger
logger = logging.getLogger('BIMamager')
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

info = args.info
sourceDir = args.source_directory
targetDir = args.target_directory
compression = args.compression
compQuality = args.compressionQuality
tmpFile = '/tmp/batchIMv2.txt'
devnull = open('/dev/null', 'w')



def copyAllImages(srcDir):
    '''Function for copying all the files from the source directory and sub-directories to target directory.'''
    for dirnames, subdirnames, filenames in os.walk(srcDir):
        # Copy all files.
        for filename in filenames:
            imageName = os.path.join(dirnames, filename)
            print imageName
            shutil.copy2(imageName, targetDir)



def main():
    ## Start execution of the main program
    copyAllImages(sourceDir)
    

# Executing the script. 
if __name__ == "__main__":
    main()
