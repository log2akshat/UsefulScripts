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

"""HTML File parser utility for parsing Debian Testing migration summary packages."""

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


def is_valid_logging_status(parser, arg):
    "Function for checking logging status is valid or not."
    if not (arg == 'on' or arg == 'off'):
        parser.error('{} is not a valid input for turning logging on or off! Please specify \"on\" for turning logging on and \"off\" for turning logging off.'.format(arg))
    return arg

## =========> Command line arguments parsing -- starts <========= ##
PARSER = argparse.ArgumentParser(description='HTML File parser utility for parsing Debian Testing migration summary packages.')
PARSER.add_argument('-f', '--file_path', help='Path of HTML file.', metavar='<HTML File>', type=lambda x: is_valid_file(PARSER, x))
PARSER.add_argument('-u', '--url_path', help='URL of HTML file.', metavar='<URL>', type=lambda x: is_valid_url(PARSER, x))
PARSER.add_argument('-t', '--text_file_path', help='Path of the text file.', metavar='<Text File Path>')
PARSER.add_argument('-l', '--log_file', help='Path of the log file.', metavar='<Log File>')
PARSER.add_argument('-ls', '--logging_onoff', help='Logging status On/Off', metavar='<Logging on/off>', type=lambda x: is_valid_logging_status(PARSER, x))
ARGS = PARSER.parse_args()

HTML_FILE = ARGS.file_path
URL_PATTERN = ARGS.url_path
TEXT_FILE = ARGS.text_file_path
DEV_NULL = open('/dev/null', 'w')

if str(HTML_FILE) == "None" and str(URL_PATTERN) == "None":
    os.system("python " + sys.argv[0] + " -h")
    sys.exit()


def file_address():
    """Function for evaluating the source of url."""
    url = ""
    if HTML_FILE != None:
        url = HTML_FILE
    elif URL_PATTERN != None:
        url = URL_PATTERN
    LOGGER.debug("URL: %s", str(url))
    return url


def text_file_location():
    """Function for evaluating the path of the text file."""
    text_file_loc = ""
    if TEXT_FILE != None:
        text_file_loc = TEXT_FILE
    else:
        text_file_loc = '/tmp/TestingMigrationSummary.txt'
    LOGGER.debug("Temporary File : %s", str(text_file_loc))
    return text_file_loc

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


def parse_text():
    """Function to parse the text."""
    # cat filename | awk 'f;/------/{f=1}' | sed '/--/q' | head -n-2 | awk '{print $1}' | paste -d" " -s
    cat_cmd = subprocess.Popen(['cat', str(text_file_location())], stdout=subprocess.PIPE,)
    awk_cmd = subprocess.Popen(['awk', 'f;/------/{f=1}'], stdin=cat_cmd.stdout, stdout=subprocess.PIPE,)
    sed_cmd = subprocess.Popen(['sed', '/--/q'], stdin=awk_cmd.stdout, stdout=subprocess.PIPE,)
    head_cmd = subprocess.Popen(['head', '-n-2'], stdin=sed_cmd.stdout, stdout=subprocess.PIPE,)
    awk_col = subprocess.Popen(['awk', '{print $1}'], stdin=head_cmd.stdout, stdout=subprocess.PIPE,)
    paste_cmd = subprocess.Popen(['paste', '-d ', '-s'], stdin=awk_col.stdout, stdout=subprocess.PIPE,)
    awk_col.stdout.close()
    parsed_text = paste_cmd.communicate()[0].strip()
    if parsed_text:
        return parsed_text


def main():
    """Main function"""
    # Delete the old file if exists.
    if os.path.exists(str(text_file_location())):
        try:
            os.remove(str(text_file_location()))
        except OSError, exception:
            LOGGER.error("Error : %s - %s", (exception.filename, exception.strerror))

    cwd = os.getcwd()
    os.chdir(cwd)
    LOGGER.info("Extracting text from the URL / html file.")
    parse_cmd = subprocess.Popen(['python', cwd + '/html2text.py', str(file_address())], stdout=subprocess.PIPE,)
    tee_cmd = subprocess.Popen(['tee', '-a', str(text_file_location())], stdin=parse_cmd.stdout, stdout=DEV_NULL)
    parse_cmd.stdout.close()
    tee_cmd.communicate()
    LOGGER.info("Extracting of text completed from the html file.")
    #os.system("%s/html2text.py %s" % (cwd, str(file_address())))
    LOGGER.info("Going to parse the text.")
    parse_text()


if __name__ == "__main__":
    main()
