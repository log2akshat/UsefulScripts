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

import os
import time
import shutil
import MySQLdb
import logging
import datetime
import argparse
import subprocess
from argparse import RawTextHelpFormatter

# MySQL Credentials
DB_HOST = 'localhost'
DB_USER = 'root'
DB_USER_PASSWORD = 'XXXXXXXXXXX'

connection = MySQLdb.connect(
                host = DB_HOST,
                user = DB_USER,
                passwd = DB_USER_PASSWORD)  # create the connection

cursor = connection.cursor()     # get the cursor
cursor.execute("SHOW DATABASES")

DB_NAMES = []
for (databaseName,) in cursor:
    if not (databaseName == 'mysql' or databaseName == 'information_schema' or databaseName == 'performance_schema'):
        DB_NAMES.append(databaseName)

BACKUP_DEST = '/Backup/BACKUPS/MySQLDUMPS/'

TIMESTAMP = time.strftime('%d-%m-%Y_%H:%M:%S')
BACKUPAREA = BACKUP_DEST + TIMESTAMP

def is_valid_loggingStatus(parser, arg):
    "Function for checking logging status is valid or not."
    if not (arg == 'on' or arg == 'off'):
        parser.error('{} is not a valid input for turning logging on or off! Please specify \"on\" for turning logging on and \"off\" for turning logging off.'.format(arg))
    else:
        return arg

## =========> Command line arguments parsing -- starts <========= ##
parser = argparse.ArgumentParser(description='*********************************************************************************************************\n********************** |MySQLDumper - MySQL DB Dumping Utility.| **********************\n*********************************************************************************************************\n\n* This script will do the following task.\n\n* It will take the databse dump of the databases define in the array and save it in the deind directory.', formatter_class=RawTextHelpFormatter)
parser.add_argument('-l','--log_file', help='Path of the log file.', metavar='<Log File>')
parser.add_argument('-ls', '--logging_onoff', help='Logging status On/Off', metavar='<Logging on/off>', type=lambda x: is_valid_loggingStatus(parser, x))
args = parser.parse_args()

## =========> Command line arguments parsing -- ends <========= ##

## =========> Logging Configurations -- starts <========= ##
loggerFile = args.log_file
loggingStatus = args.logging_onoff

logDirectory = "/var/log/"

if not loggerFile:
    if not os.path.exists(logDirectory):
        os.makedirs(logDirectory)
    Log_File = logDirectory + 'MySQLDumper.log'
else:
    Log_File = loggerFile + ".log"

# create logger
logger = logging.getLogger('MySQLDumper')
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


# Checking if backup directory already exists or not; if not it will create it.
logger.info("Creating backup directory at %s..", BACKUPAREA)
if not os.path.exists(BACKUPAREA):
    os.makedirs(BACKUPAREA)


# Start taking the databases backup..
def DBDump():
    # Function for taking the database backups.
    for db in range(len(DB_NAMES)):
        logger.info("Taking Backup of : %s database..", DB_NAMES[db])
        dumpcmd = "mysqldump -u " + DB_USER + " -h" + DB_HOST + " -p'" + DB_USER_PASSWORD + "' " + DB_NAMES[db] + " > " + BACKUPAREA + "/" + DB_NAMES[db] + ".sql"
        try:
            os.system(dumpcmd)
        except MySQLdb.Error as e:
             logger.error('MySQL Error:' % e)
    logger.info("Backup Finished.")
    subprocess.call(['tar', 'zcvf', BACKUPAREA+".tar.gz", BACKUPAREA])
    try:
        shutil.rmtree(BACKUPAREA)
    except shutil.Error as e:
        logger.error('Error in moving archive : %s' % e)
    except IOError as e: # If source or destination doesn't exist
        logger.error('IOError : %s' % e.strerror)


# Executing the script. 
if __name__ == "__main__":
    DBDump()
~                         
