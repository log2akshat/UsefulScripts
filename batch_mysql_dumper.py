#!/usr/bin/python

## MySQL Backup Script.
## Date : 01 Jaunuary 2018
## Author : Akshat Singh
#
#    Copyright (C) <2018>  <Akshat Singh>
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

"""This script will take the databse dump of the databases define in the array and save it in the defined directory."""

import os
import time
import shutil
import logging
import subprocess
import argparse
from argparse import RawTextHelpFormatter
import MySQLdb # pylint: disable=import-error

# MySQL Credentials
DB_HOST = 'localhost'
DB_USER = 'root'
DB_USER_PASSWORD = 'XXXXXXXXXXX'

# Create the connection
CONNECTION = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_USER_PASSWORD)

CURSOR = CONNECTION.cursor()     # get the cursor
CURSOR.execute("SHOW DATABASES")

DB_NAMES = []
for (databaseName,) in CURSOR:
    if not databaseName in ('mysql', 'information_schema', 'performance_schema'):
        DB_NAMES.append(databaseName)

BACKUP_DEST = '/Backup/BACKUPS/MySQLDUMPS/'

TIMESTAMP = time.strftime('%d-%m-%Y_%H:%M:%S')
BACKUPAREA = BACKUP_DEST + TIMESTAMP

def is_valid_logging_status(parser, arg):
    "Function for checking logging status is valid or not."
    if not (arg == 'on' or arg == 'off'):
        parser.error('{} is not a valid input for turning logging on or off! Please specify \"on\" for turning logging on and \"off\" for turning logging off.'.format(arg))
    return arg

## =========> Command line arguments parsing -- starts <========= ##
PARSER = argparse.ArgumentParser(description='*********************************************************************************************************\n********************** |MySQLDumper - MySQL DB Dumping Utility.| **********************\n*********************************************************************************************************\n\n* This script will do the following task.\n\n* It will take the databse dump of the databases define in the array and save it in the defined directory.', formatter_class=RawTextHelpFormatter)
PARSER.add_argument('-l', '--log_file', help='Path of the log file.', metavar='<Log File>')
PARSER.add_argument('-ls', '--logging_onoff', help='Logging status On/Off', metavar='<Logging on/off>', type=lambda x: is_valid_logging_status(PARSER, x))
ARGS = PARSER.parse_args()

## =========> Command line arguments parsing -- ends <========= ##

## =========> Logging Configurations -- starts <========= ##
LOGGER_FILE = ARGS.log_file
LOGGING_STATUS = ARGS.logging_onoff

LOG_DIRECTORY = "/var/log/"

if not LOGGER_FILE:
    if not os.path.exists(LOG_DIRECTORY):
        os.makedirs(LOG_DIRECTORY)
    LOG_FILE = '/tmp/MySQLDumper.log'
else:
    LOG_FILE = LOGGER_FILE + ".log"

# create logger
LOGGER = logging.getLogger('MySQLDumper')
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

# Checking if backup directory already exists or not; if not it will create it.
LOGGER.info("Creating backup directory at %s..", BACKUPAREA)
if not os.path.exists(BACKUPAREA):
    os.makedirs(BACKUPAREA)


# Start taking the databases backup..
def db_dump():
    """Function for taking the database backups."""
    for database in range(len(DB_NAMES)):
        LOGGER.info("Taking Backup of : %s database..", DB_NAMES[database])
        dump_cmd = "mysqldump -u " + DB_USER + " -h" + DB_HOST + " -p'" + DB_USER_PASSWORD + "' " + DB_NAMES[database] + " > " + BACKUPAREA + "/" + DB_NAMES[database] + ".sql"
        try:
            os.system(dump_cmd)
        except MySQLdb.Error as exp:
            LOGGER.error('MySQL Error: %s', exp)
    LOGGER.info("Backup Finished.")
    subprocess.call(['tar', 'zcvf', BACKUPAREA+".tar.gz", BACKUPAREA])
    try:
        shutil.rmtree(BACKUPAREA)
    except shutil.Error as exp:
        LOGGER.error('Error in moving archive : %s', exp)
    except IOError as exp: # If source or destination doesn't exist
        LOGGER.error('IOError : %s', exp.strerror)


# Executing the script.
if __name__ == "__main__":
    db_dump()
