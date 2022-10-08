#!/usr/bin/python3

import os
import logging
import argparse
import subprocess
from argparse import RawTextHelpFormatter

# =========> Argument Parsing -- starts <========= #

# Command line argument validation functions...
def is_valid_file(parser, arg):
    "Function for checking file exists or not."
    if not os.path.isfile(arg):
        parser.error('The file {} does not exist!'.format(arg))
    return arg


def is_valid_directory(parser, arg):
    "Function for checking specfied directory exists or not."
    if not os.path.isdir(arg):
        parser.error('The directory {} does not exist!'.format(arg))
    return arg


def is_valid_logging_status(parser, arg):
    "Function for checking logging status is valid or not."
    if not arg in ('on', 'off'):
        parser.error('{} is not a valid input for turning logging on or off! \
                      Please specify \"on\" for turning logging on and \"off\" for \
                      turning logging off.'.format(arg))
    return arg


# Command line option
PARSER = argparse.ArgumentParser(
    description='Repository cloning and keyword grepping utility.',
    formatter_class=RawTextHelpFormatter)

PARSER.add_argument('-f', '--repo_list_file',
                    help='Path of the repository file.',
                    required=True, metavar='<Repository File>',
                    type=lambda x: is_valid_file(PARSER, x))
PARSER.add_argument('-s', '--cloning_directory',
                    help='Directory to read input files.',
                    required=True, metavar='<Cloning Directory>',
                    type=lambda x: is_valid_directory(PARSER, x))
PARSER.add_argument('-l', '--log_file',
                    help='Path of the log file.', metavar='<Log File>')
PARSER.add_argument('-ls', '--logging_onoff',
                    help='Logging status On/Off', metavar='<Logging on/off>',
                    type=lambda x: is_valid_logging_status(PARSER, x))

ARGS = PARSER.parse_args()

# =========> Argument Parsing -- ends <========= #

## =========> Logging Configurations -- starts <========= ##
LOGGER_FILE = ARGS.log_file
LOGGING_STATUS = ARGS.logging_onoff

if not LOGGER_FILE:
    LOG_FILE = '/tmp/repo_keyword_grepper.log'
else:
    LOG_FILE = LOGGER_FILE + ".log"

# create logger
LOGGER = logging.getLogger('repo_keyword_grepper')
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
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',\
                              datefmt='%m/%d/%Y %I:%M:%S %p')

# add formatter to handlers
FILE_HANDLER.setFormatter(FORMATTER)
CONSOLE_HANDLER.setFormatter(FORMATTER)

# add ch to logger
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)

## =========> Logging Configurations -- ends <========= ##

REPOS_FILE_PATH = ARGS.repo_list_file
CLONING_DIRECTORY = ARGS.cloning_directory
ORG_NAME = (os.path.basename(CLONING_DIRECTORY).strip())
DEVNULL = open('/dev/null', 'w')
subprocess.call(['clear'])

def clone_repos():
    '''Function for cloning all the repos.'''
    count = 0
    with open(REPOS_FILE_PATH, 'r') as open_repo_file:
        repos_name = open_repo_file.readlines()
        for repo in repos_name:
            count += 1
            print("\n==================================================\n")
            LOGGER.info("Cloning Repo {}: {}\n".format(count, repo.strip()))
            if ORG_NAME == 'Zimbra':
                subprocess.call(['git', '-C', CLONING_DIRECTORY, 'clone', 'git@github.com:Zimbra/'
                                  + repo.strip() + '.git'])
            elif ORG_NAME == 'ZimbraOS':
                subprocess.call(['git', '-C', CLONING_DIRECTORY, 'clone', 'git@github.com:ZimbraOS/' + repo.strip() + '.git'])


def keyword_grepper():
    '''Function to find the keyword in the repos.'''
    with open(REPOS_FILE_PATH, 'r') as open_repo_file:
        repos_name = open_repo_file.readlines()
        for repo in repos_name:
            print("\n============================================================================")
            LOGGER.info("Processing repo {}".format(repo.strip()))
            keywords_list = ['Master', 'Slave', 'Blacklist', 'Whitelist', 'White hat', 'Black hat']
            for keyword in keywords_list:
                LOGGER.info('\nGrepping keyword - {} in the repo {}'.format(keyword, repo.strip()))
                subprocess.call(['grep', '-inR', keyword, os.path.abspath(CLONING_DIRECTORY) + '/'
                                  + repo.strip()])


def main():
    '''Start execution of the main program.'''
    clone_repos()
    keyword_grepper()


# Executing the script.
if __name__ == "__main__":
    main()
