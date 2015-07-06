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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import csv
import argparse
import subprocess

# Command line argument validation functions...
def is_valid_directory(parser, arg):
    "Function for checking specfied directory exists or not."
    if not os.path.isdir(arg):
        parser.error('The directory {} does not exist!'.format(arg))
    else:
        # File exists so return the directory
        return arg

# Command line options
parser = argparse.ArgumentParser(description='Batch renaming files utility...')
parser.add_argument('-s','--source_directory', help='Directory to read input files.', required=True, metavar='<Source Directory>', type=lambda x: is_valid_directory(parser, x))
parser.add_argument('-f','--filename', help='Desired output file name.', required=True, metavar='<Output file names>')
args = parser.parse_args()

filepath = args.source_directory
outfileName = args.filename
tmpFile = '/tmp/renameIM.txt'
devnull = open('/dev/null', 'w')

file = []
# ls | sort --version-sort -f
filterCall = subprocess.Popen(['ls', filepath],stdout=subprocess.PIPE)
sortCmd = subprocess.Popen(['sort', '--version-sort', '-f'], stdin=filterCall.stdout, stdout=subprocess.PIPE)
teeCmd = subprocess.Popen(['tee', tmpFile], stdin=sortCmd.stdout, stdout=devnull)
sortCmd.stdout.close()
subprocess.call(['cat', 'tmpfile'])

i = 0
counter = 1
fileName = ""
pathfile = open(tmpFile, 'r')
file = pathfile.read().splitlines()
with open(tmpFile, 'r') as f:
	reader = csv.reader(f, delimiter=' ')
	for row in reader:
		pathRow = row[0:]
		length = len(pathRow)
		if i < length:
			for x in pathRow:
				fileName = fileName + " " + pathRow[i]
				i = i + 1
		fileName = fileName.strip()
                extName = os.path.basename(fileName).split(".")[1]
		imgpath = filepath + "/" + fileName
		print "Renaming " + imgpath + "..."
                os.rename(imgpath, filepath + "/" + outfileName + " " + str(counter) + "." + extName)
		i = 0
		fileName = ""
		counter = counter + 1
