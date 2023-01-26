#! /usr/bin/python

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

"""Script for tailing the logs specified in the configuration file."""

import os
import sys
from subprocess import call
import argparse
from argparse import RawTextHelpFormatter


# =========> Argument Parsing -- starts <========= #

# Command line argument validation functions...
def is_valid_file(parser, arg):
    "Function for checking file exists or not."
    if not os.path.isfile(arg):
        parser.error('\n\n\tThe file {} does not exist!'.format(arg))
    return arg


# Command line option
PARSER = argparse.ArgumentParser(
    description='Log tailing script: '\
                  'For tailing logs specified in the config file.',
    formatter_class=RawTextHelpFormatter)

PARSER.add_argument('-c', '--config_file',
                    help='Path of the configuration file.',
                    required=True, metavar='<Config File>',
                    type=lambda x: is_valid_file(PARSER, x))
ARGS = PARSER.parse_args()

# =========> Argument Parsing -- ends <========= #

INPUT_CONFIG_FILE = os.path.abspath(ARGS.config_file)


def build_string(sequence, seprator=' '):
    """Function for joining existing log files."""
    return seprator.join(str(i) for i in sequence if os.path.isfile(i))


# Function for building the command
def cmnd_builder():
    """Function for building the part of the command"""
    with open(INPUT_CONFIG_FILE, 'r') as config:
        return build_string(config.read().splitlines())
    config.close()


# Start execution of the main program
def main():
    """Main function to call the tail command"""
    cmd = str(cmnd_builder()).strip()
    if not cmd:
        print("Warning: Either the config file is empty " \
                "or the paths specified in the config file is/are incorrect!")
        sys.exit()
    else:
        call(['tail -F ' + cmd], shell=True)


# Executing the script.
if __name__ == "__main__":
    main()
