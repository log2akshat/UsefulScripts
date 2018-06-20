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
    

def is_valid_loggingStatus(parser, arg):
    "Function for checking logging status is valid or not."
    if not (arg == 'on' or arg == 'off'):
        parser.error('{} is not a valid input for turning logging on or off! Please specify \"on\" for turning logging on and \"off\" for turning logging off.'.format(arg))
    else:
        return arg

## =========> Command line arguments parsing -- starts <========= ##
parser = argparse.ArgumentParser(description='Purpose - This script is useful for finding the number of files in a given directory and if the source directory is not specified on the CLI then it will give the number of files in the public_html user area and also tells if a user does not have public_html directory.', formatter_class=RawTextHelpFormatter)
parser.add_argument('-s','--source_directory', help='Directory to read input files.', metavar='<Source Directory>', type=lambda x: is_valid_directory(parser, x))
parser.add_argument('-l','--log_file', help='Path of the log file.', metavar='<Log File>')
parser.add_argument('-ls', '--logging_onoff', help='Logging status On/Off', metavar='<Logging on/off>', type=lambda x: is_valid_loggingStatus(parser, x))
args = parser.parse_args()


## =========> Command line arguments parsing -- ends <========= ##

subprocess.call('clear')

## =========> Logging Configurations -- starts <========= ##
loggerFile = args.log_file
loggingStatus = args.logging_onoff

if not loggerFile:
    Log_File = '/tmp/DirStats.log'
else:
    Log_File = loggerFile + ".log"

# create logger
logger = logging.getLogger('DirStats')
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

sourceDir = args.source_directory
devnull = open('/dev/null', 'w')
                

def srcDir():
    '''Function for returning the source directory'''
    srcDir = ""
    if args.source_directory:
        srcDir = args.source_directory
    elif platform.system() == "Darwin":
        logger.info("Operating System detected : Mac")
        srcDir = "/Users"
    elif platform.system() == "Linux":
	logger.info("Operating System detected : Mac")
        srcDir = "/home"
    return srcDir


def numOfFiles(srcDir):
    '''Function to return number of directories and files in a given directory.'''
    listAll = os.listdir(srcDir)
    return len(listAll)



def main():
    ## Start execution of the main program
    unusedAccounts = []
    activeAccounts = []
    inactiveAccounts = []
    sourceDir = srcDir()
    logger.info("Source directory : %s", sourceDir)
    if (sourceDir == '/Users' or sourceDir == '/home'):
        users = os.listdir(sourceDir)
        for i in range(len(users)):
	    if platform.system() == "Darwin":
            	scanDir = "/Users/" + users[i] + "/public_html"
	    elif platform.system() == "Linux":
            	scanDir = "/home/" + users[i] + "/public_html"
            if os.path.exists(scanDir):
                 totalFiles = numOfFiles(scanDir)
                 if totalFiles == 0:
                     inactiveAccounts.append(users[i])
                 else:
                     activeAccounts.append(users[i])
            else:
                logger.info("public_html directory for the user %s does not exists.", users[i])
                unusedAccounts.append(users[i]) 
        print "Unused accounts : " + str(unusedAccounts)
        print "Inactive accounts : " + str(inactiveAccounts)
        print "Active accounts : " + str(activeAccounts)
    else:
        logger.info("Number of directories and files in %s directory is/are : %s\n\n", sourceDir, numOfFiles(sourceDir))
        
    

# Executing the script. 
if __name__ == "__main__":
    main()
