#!/usr/bin/python

#    Copyright (C) <2022>  <Akshat Singh>
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

'''Script for taking Screenshots in Linux.'''

import subprocess

def main():
    '''Call for taking Screenshots'''
    subprocess.call(['eog'])
    subprocess.call(['sleep', '2'])
    subprocess.call(['gnome-screenshot'])


# Executing the script.
if __name__ == "__main__":
    main()
