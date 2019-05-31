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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Script to run a compression only on specific camera make but not on others"""

from __future__ import print_function
import os
import time
import errno
import shutil
import logging
import subprocess
from datetime import datetime
import argparse
from argparse import RawTextHelpFormatter

# Command line argument validation functions...
def is_valid_directory(parser, arg):
    "Function for checking specfied directory exists or not."
    if not os.path.isdir(arg):
        parser.error('The directory {} does not exist!'.format(arg))
    return arg


def is_target_directory(parser, arg):
    "Function for checking specfied directory exists or not."
    if not os.path.isdir(arg):
        print('The directory %s does not exist!, so creating it for you..' % arg)
        try:
            subprocess.call(['mkdir', '-p', arg])
            return arg
        except IOError as ioexp:
            parser.error('The directory {} does not exist and unable to create for you, please create it manually!'.format(arg), ioexp)
    return arg


def is_valid_option(parser, arg):
    "Function for checking option is on or off."
    if not (arg == 'on' or arg == 'off'):
        parser.error('{} is not a valid input for turning option on or off! Please specify \"on\" for turning the option on and \"off\" for turning it off.'.format(arg))
    return arg


def is_valid_logging_status(parser, arg):
    "Function for checking logging status is valid or not."
    if not (arg == 'on' or arg == 'off'):
        parser.error('{} is not a valid input for turning logging on or off! Please specify \"on\" for turning logging on and \"off\" for turning logging off.'.format(arg))
    return arg


## =========> Command line arguments parsing -- starts <========= ##
PARSER = argparse.ArgumentParser(description='[Purpose - This script is useful in a situation where we want to run a compression only on specific camera make but not on others and later want to do some manual image processing using tools like gimp on some camera make images and also at the same time we also want to maintain the sequence of the images based on their capturing time not based on the image modification.]\n\n\n**********************************************************************\nThis script will copy the images from the specified directory and all of its sub-directory to the target directory. The target directory will be the provided on the command line argument; but the final destination will be targetDir/CameraManufacurer__CameraModel/unixTimeStamp_CameraMake.JPG\nn**********************************************************************\nBatch Image Manager is an advaced version of the Batch Image Compression utility. For running this program you need to have exif tool and imagemagick installed on your machine. This program is used for mixing the various images taken from different camera make based on their capturing time in ascending order and rename each image on thir unix timestamp.\n\nIf compression option is selected as OFF then this script wil not create any sub-directories based on camera make just it will arrange the pictures based on their capturing time. \n\n\n\t', formatter_class=RawTextHelpFormatter)
PARSER.add_argument('-i', '--info', help='Information about the Camera make and Model', metavar='<Camera Information>')
PARSER.add_argument('-s', '--source_directory', help='Directory to read input files.', required=True, metavar='<Source Directory>', type=lambda x: is_valid_directory(PARSER, x))
PARSER.add_argument('-t', '--target_directory', help='Directory to save output files.', required=True, metavar='<Target Directory>', type=lambda x: is_target_directory(PARSER, x))
PARSER.add_argument('-cmp', '--compression', help='Compression On/Off', required=True, metavar='<Compression on/off>', type=lambda x: is_valid_option(PARSER, x))
PARSER.add_argument('-clq', '--compressionQuality', help='Quality of the Image to retain for specific Camera make [Image Quality range is 1-100].', metavar='<CameraMake_#ImageQuality Eg.: Canon100D_#90>')
PARSER.add_argument('-l', '--log_file', help='Path of the log file.', metavar='<Log File>')
PARSER.add_argument('-ls', '--logging_onoff', help='Logging status On/Off', metavar='<Logging on/off>', type=lambda x: is_valid_logging_status(PARSER, x))
ARGS = PARSER.parse_args()

## =========> Command line arguments parsing -- ends <========= ##

subprocess.call('clear')

## =========> Logging Configurations -- starts <========= ##
LOGGER_FILE = ARGS.log_file
LOGGING_STATUS = ARGS.logging_onoff

if not LOGGER_FILE:
    LOG_FILE = '/tmp/BatchImageManager.log'
else:
    LOG_FILE = LOGGER_FILE + ".log"

# create logger
LOGGER = logging.getLogger('BIMamager')
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

INFO = ARGS.info
SOURCE_DIR = ARGS.source_directory
TARGET_DIR = ARGS.target_directory
COMPRESSION = ARGS.compression
COMP_QUALITY = ARGS.compressionQuality
TMP_FILE = '/tmp/batchIMv2.txt'
DEVNULL = open('/dev/null', 'w')


def timestamp_query(image_name):
    '''Function for returning the Image capturing time unix timestamp'''
    exif_cmd = subprocess.Popen(['exif', '-x', image_name], stdout=subprocess.PIPE)
    grep_cmd = subprocess.Popen(['grep', 'Date_and_Time__Original'], stdin=exif_cmd.stdout, stdout=subprocess.PIPE)
    cut_cmd1 = subprocess.Popen(['cut', '-d', '>', '-f2'], stdin=grep_cmd.stdout, stdout=subprocess.PIPE)
    cut_cmd2 = subprocess.Popen(['cut', '-d', '<', '-f1'], stdin=cut_cmd1.stdout, stdout=subprocess.PIPE)
    cut_cmd1.stdout.close()
    capture_time = cut_cmd2.communicate()[0].split("\n")[0]
    #print captureTime
    format_time = datetime.strptime(capture_time, "%Y:%m:%d %H:%M:%S")
    return int(time.mktime(format_time.timetuple()))


def cam_make_query(image_name):
    '''Function for returning the camera Make and Model'''
    exif_cmd = subprocess.Popen(['exif', '-x', image_name], stdout=subprocess.PIPE)
    grep_cmd = subprocess.Popen(['grep', 'Manufacturer'], stdin=exif_cmd.stdout, stdout=subprocess.PIPE)
    cut_cmd1 = subprocess.Popen(['cut', '-d', '>', '-f2'], stdin=grep_cmd.stdout, stdout=subprocess.PIPE)
    cut_cmd2 = subprocess.Popen(['cut', '-d', '<', '-f1'], stdin=cut_cmd1.stdout, stdout=subprocess.PIPE)
    cut_cmd1.stdout.close()
    cam_manufacturer = cut_cmd2.communicate()[0].split("\n")[0]
    exif_cmd_model = subprocess.Popen(['exif', '-x', image_name], stdout=subprocess.PIPE)
    grep_cmd_model = subprocess.Popen(['grep', 'Model'], stdin=exif_cmd_model.stdout, stdout=subprocess.PIPE)
    cut_cmd1_model = subprocess.Popen(['cut', '-d', '>', '-f2'], stdin=grep_cmd_model.stdout, stdout=subprocess.PIPE)
    cut_cmd2_model = subprocess.Popen(['cut', '-d', '<', '-f1'], stdin=cut_cmd1_model.stdout, stdout=subprocess.PIPE)
    cut_cmd1_model.stdout.close()
    cam_model = cut_cmd2_model.communicate()[0].split("\n")[0]
    cam_dir = cam_manufacturer + "__" + cam_model
    return cam_dir



def copy_all_images(src_dir):
    '''Function for copying all the files from the source directory and sub-directories to target directory.'''
    for dirnames, subdirnames, filenames in os.walk(src_dir):
        # Copy all files.
        for filename in filenames:
            image_name = os.path.join(dirnames, filename)
            unix_time_stamp = timestamp_query(image_name)
            camera = cam_make_query(image_name)
            img_destination = TARGET_DIR + "/" + camera
            ## Create destination directory if not present
            try:
                os.makedirs(img_destination)
            except OSError as exp:
                if exp.errno != errno.EEXIST:
                    raise
            ## Start copying and renaming
            final_image = img_destination + "/" + str(unix_time_stamp) + "_" + camera + ".JPG"
            LOGGER.info("Copying and Renaming Image : %s to %s", image_name, final_image)
            shutil.copy2(image_name, final_image)


INPUT_COMP_STRING = "\n================================================================================================================\nPlease enter which directory images needs to be compressed and the quality level in the following format:\n\n\t\t\t\t*********************************\n\t\t\t\t  <DirectoyName_#qQualityLevel>\n\t\t\t\t*********************************\nEg.: Canon__Canon EOS 100D_#q90\n\nIn case you want to run compression on multiple directories please enter in csv format\nEg.: Canon__Canon EOS 100D_#q90, SAMSUNG__GT-I9100_q81\n\n================================================================================================================\n\nEnter your input: "


def validate_user_compression_input():
    '''Function for validating user input for compressing images inside specific directories.'''
    while True:
        try:
            comp_input = raw_input(INPUT_COMP_STRING)
            if not comp_input:
                raise ValueError("There wasn't any input!")
            else:
                print("You have entered: ", comp_input)
                break
        except ValueError as e:
            print(e)


def main():
    """Start execution of the main program."""
    if COMPRESSION == 'off':
        copy_all_images(SOURCE_DIR)
    else:
        copy_all_images(SOURCE_DIR)
        validate_user_compression_input()


# Executing the script.
if __name__ == "__main__":
    main()
