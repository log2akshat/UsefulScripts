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

'''Script for finding the number of files in a given directory and if the source directory is not specified on the CLI then it will give the number of files in the public_html user area and also tells if a user does not have public_html directory.'''

import os
import logging
import platform
import subprocess
import argparse
from argparse import RawTextHelpFormatter
from __future__ import print_function


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
PARSER = argparse.ArgumentParser(description='Purpose - This script is useful for finding the number of files in a given directory and if the source directory is not specified on the CLI then it will give the number of files in the public_html user area and also tells if a user does not have public_html directory.', formatter_class=RawTextHelpFormatter)
PARSER.add_argument('-s', '--source_directory', help='Directory to read input files.', metavar='<Source Directory>', type=lambda x: is_valid_directory(PARSER, x))
PARSER.add_argument('-l', '--log_file', help='Path of the log file.', metavar='<Log File>')
PARSER.add_argument('-ls', '--logging_onoff', help='Logging status On/Off', metavar='<Logging on/off>', type=lambda x: is_valid_logging_status(PARSER, x))
ARGS = PARSER.parse_args()


## =========> Command line arguments parsing -- ends <========= ##

subprocess.call('clear')

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

SOURCE_DIR = ARGS.source_directory


def source_dir():
    '''Function for returning the source directory'''
    src_dir = ""
    if SOURCE_DIR:
        src_dir = SOURCE_DIR
    elif platform.system() == "Darwin":
        LOGGER.info("Operating System detected : Mac")
        src_dir = "/Users"
    elif platform.system() == "Linux":
        LOGGER.info("Operating System detected : Mac")
        src_dir = "/home"
    return src_dir


def num_of_files(source_directory):
    '''Function to return number of files
       and directories in a specified directory.'''
    list_all = os.listdir(source_directory)
    return len(list_all)


def main():
    '''Start execution of the main program.'''
    unused_accounts = []
    active_accounts = []
    inactive_accounts = []
    SOURCE_DIR = source_dir()
    LOGGER.info("Source directory : %s", SOURCE_DIR)
    if (SOURCE_DIR == '/Users' or SOURCE_DIR == '/home'):
        users = os.listdir(SOURCE_DIR)
        for i in range(len(users)):
            if platform.system() == "Darwin":
                scan_dir = "/Users/" + users[i] + "/public_html"
            elif platform.system() == "Linux":
                scan_dir = "/home/" + users[i] + "/public_html"
            if os.path.exists(scan_dir):
                total_files = num_of_files(scan_dir)
                if total_files == 0:
                    inactive_accounts.append(users[i])
                else:
                    active_accounts.append(users[i])
            else:
                LOGGER.info("public_html directory for the user %s does not exists.", users[i])
                unused_accounts.append(users[i])
        print('Unused accounts : %s' % str(unused_accounts))
        print('Inactive accounts : %s' % str(inactive_accounts))
        print('Active accounts : %s' % str(active_accounts))
    else:
        LOGGER.info("Number of directories and files in %s directory is/are : %s\n\n", SOURCE_DIR, num_of_files(SOURCE_DIR))


# Executing the script.
if __name__ == "__main__":
    main()
