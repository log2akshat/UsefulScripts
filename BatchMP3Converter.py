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


import os
import sys
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
	
	
## =========> Command line arguments parsing -- starts <========= ##
parser = argparse.ArgumentParser(description='Batch mp4 to mp3 conversion utility. For running this program you need to have FFMPEG with mp3 codecs installed on your machine.')
parser.add_argument('-s','--source_directory', help='Directory to read input video files.', required=True, metavar='<Source Directory>', type=lambda x: is_valid_directory(parser, x))
parser.add_argument('-t','--target_directory', help='Directory to save output converted mp3 files.', required=True, metavar='<Target Directory>', type=lambda x: is_target_directory(x))
parser.add_argument('-l','--log_file', help='Path of the log file.', metavar='<Log File>')
parser.add_argument('-ls', '--logging_onoff', help='Logging status On/Off', metavar='<Logging on/off>', type=lambda x: is_valid_loggingStatus(parser, x))
args = parser.parse_args()

## =========> Command line arguments parsing -- ends <========= ##


## =========> Logging Configurations -- starts <========= ##
loggerFile = args.log_file
loggingStatus = args.logging_onoff

if not loggerFile:
    Log_File = '/tmp/BatchMP3Converter.log'
else:
    Log_File = loggerFile + ".log"

# create logger
logger = logging.getLogger('BMP3C')
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

srcDir = os.path.join(args.source_directory, '')
targetDir = args.target_directory


def mp3Conversion(songPath, conversionPath, songName):
    '''Function to convert the mp4 song to a mp3 file.'''
    song = conversionPath + "/" +  songName + ".mp3"
    logger.info("Going to convert %s song.." % song)
    cmd = subprocess.Popen(['ffmpeg', '-i', songPath, '-codec:a', 'libmp3lame', '-qscale:a', '2', conversionPath + "/" + songName + '.mp3'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    tee = subprocess.Popen(['tee', '-a', Log_File], stdin=cmd.stdout)
    cmd.stdout.close()
    tee.communicate()

    

def allFilePaths():
    '''Function to get list of all the files in the source directories.'''
    filePaths = []
    for root, directories, files in os.walk(srcDir):
        for filename in files:
            filepath = os.path.join(root, filename)
            filePaths.append(filepath)
    return filePaths



def main():
    slashCount = 0
    conversionPath = ""
    srcDirModified = srcDir
    for audioSongPath in allFilePaths():
        songName =  os.path.basename(audioSongPath).split(".mp4")[0]
        #print os.path.dirname(audioSongPath)
        if srcDir.endswith('/'):
            srcDirModified = srcDir[:-1]
            slashCount = srcDirModified.count('/')
            groups =  os.path.dirname(audioSongPath).split('/') # Retrieving the full path from a path except filename
            # Comparing and removing the source directory path.
            conversionPath = targetDir + "/" + '/'.join(groups[slashCount:])
            if not os.path.exists(conversionPath): # Create conversion path directory if it doesn't exists.
                logger.info("Going to create %s subdirectory.." % conversionPath)
                os.makedirs(conversionPath)
        mp3Conversion(audioSongPath, conversionPath, songName)

              
        
if __name__ == "__main__":
    main()
    
