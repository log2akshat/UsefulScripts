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
#
#    Script for tailing the logs specified in the
#    configuration file.


import os
import sys
import argparse
import ConfigParser
from subprocess import call
from argparse import RawTextHelpFormatter



## =========> Argument Parsing -- starts <========= ##

# Command line argument validation functions...
def is_valid_file(parser, arg):
    "Function for checking file exists or not."
    if not os.path.isfile(arg):
        parser.error('The file {} does not exist!'.format(arg))
    else:
        # File exists so return the filename
        return arg


# Command line option
parser = argparse.ArgumentParser(description='Log tailing script : This script will tail the logs specified in the config file.', formatter_class=RawTextHelpFormatter)
parser .add_argument('-c', '--config_file', help='Path of the configuration file.', required=True, metavar='<Config File>', type=lambda x: is_valid_file(parser, x))
args = parser.parse_args()

## =========> Argument Parsing -- ends <========= ##


InputConfigFile = os.path.abspath(args.config_file)


## Function for building the command
def cmndBuilder():
    configFile = open(InputConfigFile, 'r')
    file = configFile.read().splitlines()
    tailcmnd = ""
    for logfile in file:
        if os.path.isfile(logfile):
            tailcmnd = tailcmnd + " -f " + logfile
    return tailcmnd



## Start execution of the main program
def main():
    cmd = str(cmndBuilder()).strip()
    if not cmd:
        print("Warning: Either the config file is empty or the paths specified in the config file is/are incorrect!")
        sys.exit()
    else:
        call(['tail ' + cmd], shell=True)



# Executing the script.
if __name__ == "__main__":
    main()












    
