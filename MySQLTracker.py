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
parser.add_argument('-d','--database_name', help='MANDATORY : Name of the database.', required=True, metavar='<Database Name>')
parser.add_argument('-l','--log_file', help='Path of the log file.', metavar='<Log File>')
parser.add_argument('-ls', '--logging_onoff', help='Logging status On/Off', metavar='<Logging on/off>', type=lambda x: is_valid_logging_status(parser, x))
args = parser.parse_args()

## =========> Command line arguments parsing -- ends <========= ##

dbName = args.database_name

## =========> Logging Configurations -- starts <========= ##
loggerFile = args.log_file
loggingStatus = args.logging_onoff

logDirectory = "/var/log/"

if not loggerFile:
    if not os.path.exists(logDirectory):
        os.makedirs(logDirectory)
    Log_File = logDirectory + 'MySQLTracker.log'
else:
    Log_File = loggerFile + ".log"

# create logger
logger = logging.getLogger('MySQLTracker')
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

subprocess.call(["clear"])

# Function to show the processes of the given database.
def showProcessList():
    logger.debug("Showinng current connections on MySQL..")
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
