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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
##   Script to parse Debian Testing migration summary packages from html file.
##   Date : 17 July 2015 (v1.0)
##   Dependency Needed : html2text (http://www.aaronsw.com/2002/html2text/)

import os
import sys
import urllib2
import logging
import argparse
import subprocess

# Command line argument validation functions...
def is_valid_file(parser, arg):
    "Function for checking file exists or not."
    if not os.path.isfile(arg):
        parser.error('The file {} does not exist!'.format(arg))
    else:
        # File exists so return the filename
        return arg

def is_valid_url(parser, arg):
    "Function for checking url exists or not."
    if True:
        try:
            urllib2.urlopen(arg)
            print("Good : Url is validated!")
            return arg
        except urllib2.HTTPError, err:
            print("Error : %s" % err.code)
            parser.error('The url {} does not exist!'.format(arg))
        except urllib2.URLError, err:
            print("Error : %s" % err.args)
            parser.error('The url {} does not seems to be valid!'.format(arg))
    else:
        # File exists so return the filename
        return arg


def is_valid_loggingStatus(parser, arg):
    "Function for checking logging status is valid or not."
    if not (arg == 'on' or arg == 'off'):
        parser.error('{} is not a valid input for turning logging on or off! Please specify \"on\" for turning logging on and \"off\" for turning logging off.'.format(arg))
    else:
        return arg

## =========> Command line arguments parsing -- starts <========= ##
parser = argparse.ArgumentParser(description='HTML File parser utility for parsing Debian Testing migration summary packages.')
parser.add_argument('-f','--file_path', help='Path of HTML file.', metavar='<HTML File>', type=lambda x: is_valid_file(parser, x))
parser.add_argument('-u','--url_path', help='URL of HTML file.', metavar='<URL>', type=lambda x: is_valid_url(parser, x))
parser.add_argument('-t','--textFile_path', help='Path of the text file.', metavar='<Text File Path>')
parser.add_argument('-l','--log_file', help='Path of the log file.', metavar='<Log File>')
parser.add_argument('-ls', '--logging_onoff', help='Logging status On/Off', metavar='<Logging on/off>', type=lambda x: is_valid_loggingStatus(parser, x))
args = parser.parse_args()

HTMLFile = args.file_path
urlPattern = args.url_path
textFile = args.textFile_path
devnull =  open('/dev/null', 'w')

if str(HTMLFile) == "None" and str(urlPattern) == "None":
    os.system("python " + sys.argv[0] + " -h")
    sys.exit()

def fileAddress():
    URL = ""
    if HTMLFile != None:
        URL = HTMLFile
    elif urlPattern != None:
        URL = urlPattern
    logger.debug("URL : %s" % str(URL))
    return URL

def textFileLocation():
    textFileLoc = ""
    if textFile != None:
        textFileLoc = textFile
    else:
        textFileLoc = '/tmp/TestingMigrationSummary.txt'
    logger.debug("Temporary File : %s" % str(textFileLoc))
    return textFileLoc

## =========> Command line arguments parsing -- ends <========= ##


## =========> Logging Configurations -- starts <========= ##
loggerFile = args.log_file
loggingStatus = args.logging_onoff

if not loggerFile:
    Log_File = '/tmp/HTMLParser.log'
else:
    Log_File = loggerFile + ".log"

# create logger
logger = logging.getLogger('HTMLParser')
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


def parseText():
    # Function to parse the text
    # cat filename | awk 'f;/------/{f=1}' | sed '/--/q' | head -n-2 | awk '{print $1}' | paste -d" " -s
    cat_cmd = subprocess.Popen(['cat', str(textFileLocation())], stdout=subprocess.PIPE,)
    awk_cmd = subprocess.Popen(['awk', 'f;/------/{f=1}'], stdin=cat_cmd.stdout, stdout=subprocess.PIPE,)
    sed_cmd = subprocess.Popen(['sed', '/--/q'], stdin=awk_cmd.stdout, stdout=subprocess.PIPE,)
    head_cmd = subprocess.Popen(['head', '-n-2'], stdin=sed_cmd.stdout, stdout=subprocess.PIPE,)
    awk_col = subprocess.Popen(['awk', '{print $1}'], stdin=head_cmd.stdout, stdout=subprocess.PIPE,)
    paste_cmd = subprocess.Popen(['paste', '-d ', '-s'], stdin=awk_col.stdout, stdout=subprocess.PIPE,)
    awk_col.stdout.close()
    parsed_text = paste_cmd.communicate()[0].strip()
    print parsed_text
    if parsed_text:
        return parsed_text


def main():
    # Delete the old file if exists
    if os.path.exists(str(textFileLocation())):
        try:
            os.remove(str(textFileLocation()))
        except OSError, e:
            print ("Error : %s - %s." % (e.filename, e.strerror))
            logger.error("Error : %s - %s" % (e.filename, e.strerror))
 
    cwd = os.getcwd()
    os.chdir(cwd)
    logger.info("Extracting text from the URL / html file.")
    parseCmd = subprocess.Popen(['python', cwd + '/html2text.py', str(fileAddress())], stdout=subprocess.PIPE,)
    teeCmd = subprocess.Popen(['tee', '-a', str(textFileLocation())], stdin=parseCmd.stdout, stdout=devnull)
    parseCmd.stdout.close()
    teeCmd.communicate()
    logger.info("Extracting of text completed from the html file.")
    #os.system("%s/html2text.py %s" % (cwd, str(fileAddress())))
    logger.info("Going to parse the text.")
    parseText()


if __name__ == "__main__":
    main()
