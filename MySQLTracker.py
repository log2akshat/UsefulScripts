#!/usr/bin/python

## MySQL Status Script.
## Date : 06 February 2017
## Author : Akshat Singh
##          akshat-pg8@iiitmk.ac.in

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
#

import os
import time
import logging
import argparse
import subprocess
from argparse import RawTextHelpFormatter

# MySQL Credentials
DB_HOST = 'localhost'
DB_USER = 'root'
DBHOST = "localhost"
DB_USER_PASSWORD = 'topSecret'

TIMESTAMP = time.strftime('%d-%m-%Y_%H:%M:%S')

def is_valid_logging_status(parser, arg):
    "Function for checking logging status is valid or not."
    if not (arg == 'on' or arg == 'off'):
        parser.error('{} is not a valid input for turning logging on or off! Please specify \"on\" for turning logging on and \"off\" for turning logging off.'.format(arg))
    return arg

## =========> Command line arguments parsing -- starts <========= ##
parser = argparse.ArgumentParser(description='*********************************************************************************************************\n********************** |MySQLTracker - MySQL Tracking Utility.| **********************\n*********************************************************************************************************\n\n* This script will do the following task.\n\n* It will list the status of the MySQL and shows the processlist of the given database.', formatter_class=RawTextHelpFormatter)
parser.add_argument('-d', '--database_name', help='MANDATORY : Name of the database.', required=True, metavar='<Database Name>')
parser.add_argument('-l', '--log_file', help='Path of the log file.', metavar='<Log File>')
parser.add_argument('-ls', '--logging_onoff', help='Logging status On/Off', metavar='<Logging on/off>', type=lambda x: is_valid_logging_status(parser, x))
ARGS = parser.parse_args()

## =========> Command line arguments parsing -- ends <========= ##

dbName = ARGS.database_name

## =========> Logging Configurations -- starts <========= ##
LOGGER_FILE = ARGS.log_file
LOGGING_STATUS = ARGS.logging_onoff

LOG_DIRECTORY = "/var/log/"

if not LOGGER_FILE:
    if not os.path.exists(LOG_DIRECTORY):
        os.makedirs(LOG_DIRECTORY)
    LOG_FILE = LOG_DIRECTORY + 'MySQLTracker.log'
else:
    LOG_FILE = LOGGER_FILE + ".log"

# create logger
LOGGER = logging.getLogger('MySQLTracker')
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

subprocess.call(["clear"])

# Function to show the processes of the given database.
def showProcessList():
    LOGGER.debug("Showinng current connections on MySQL..")
    mysqlCmd = subprocess.Popen(["mysqladmin -u " + DB_USER + " -h" + DBHOST + " -p'" + DB_USER_PASSWORD + "' processlist"], shell=True, stdout=subprocess.PIPE,)
    grepCmd = subprocess.Popen(['grep', dbName], stdin=mysqlCmd.stdout, stdout=subprocess.PIPE,)
    mysqlCmd.stdout.close()
    currentProcesses = str(grepCmd.communicate()[0]).strip()
    print("+-----+------+-------------------+----------+---------+-------+-------+------------------+----------+")
    print("| Id  | User | Host              | db       | Command | Time  | State | Info             | Progress |")
    print("+-----+------+-------------------+----------+---------+-------+-------+------------------+----------+")
    print currentProcesses + "\n"
    


# Start taking the databases backup..
def MySQLStatus():
    # Function for taking the database backups.
    #dumpcmd = "mysqladmin -u " + DB_USER + " -h" + DBHOST + " -p'" + DB_USER_PASSWORD + "' status extended-status "
    dumpcmd = "mysqladmin -u " + DB_USER + " -h" + DBHOST + " -p'" + DB_USER_PASSWORD + "' status "
    print("\n\n+----------+------+-------------------+------------- MySQL STATUS - STARTS ---------+------------+------------+------------------+----------+")
    os.system(dumpcmd)
    print("+----------+------+-------------------+------------- MySQL STATUS - ENDS -----------+------------+------------+------------------+----------+\n\n")
    showProcessList()


# Executing the script. 
if __name__ == "__main__":
    MySQLStatus()
