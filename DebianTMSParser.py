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
ARGS = parser.parse_args()

HTMLFile = ARGS.file_path
urlPattern = ARGS.url_path
textFile = ARGS.textFile_path
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
    LOGGER.debug("URL : %s" % str(URL))
    return URL

def textFileLocation():
    textFileLoc = ""
    if textFile != None:
        textFileLoc = textFile
    else:
        textFileLoc = '/tmp/TestingMigrationSummary.txt'
    LOGGER.debug("Temporary File : %s" % str(textFileLoc))
    return textFileLoc

## =========> Command line arguments parsing -- ends <========= ##


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
        except OSError, exception:
            print ("Error : %s - %s." % (exception.filename, exception.strerror))
            LOGGER.error("Error : %s - %s" % (exception.filename, exception.strerror))
 
    cwd = os.getcwd()
    os.chdir(cwd)
    LOGGER.info("Extracting text from the URL / html file.")
    parse_cmd = subprocess.Popen(['python', cwd + '/html2text.py', str(fileAddress())], stdout=subprocess.PIPE,)
    tee_cmd = subprocess.Popen(['tee', '-a', str(textFileLocation())], stdin=parse_cmd.stdout, stdout=devnull)
    parse_cmd.stdout.close()
    tee_cmd.communicate()
    LOGGER.info("Extracting of text completed from the html file.")
    #os.system("%s/html2text.py %s" % (cwd, str(fileAddress())))
    LOGGER.info("Going to parse the text.")
    parseText()


if __name__ == "__main__":
    main()
