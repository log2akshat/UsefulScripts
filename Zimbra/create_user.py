# !/bin/python

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

"""Script for creating specified number of users for Zimbra mailbox."""

import os
import argparse

# Command line argument validation functions...
def is_valid_directory(parser, arg):
    "Function for checking specfied directory exists or not."
    if not os.path.isdir(arg):
        parser.error('The directory {} does not exist!'.format(arg))
    return arg

## =========> Command line arguments parsing -- starts <========= ##
PARSER = argparse.ArgumentParser(description='User generation utility...')
PARSER.add_argument('-u', '--username', help='Pattern of the username.', required=True,
                    metavar='<Username>')
PARSER.add_argument('-n', '--number_of_users', help='Number of users to be created.',
                    required=True, metavar='<Number of Users>')
ARGS = PARSER.parse_args()
## =========> Command line arguments parsing -- ends <========= ##

# Arguments parsing
USERNAME = ARGS.USERNAME
NUM_OF_USERS = int(ARGS.number_of_users)

def create_user():
    """Function for creating users"""
    for i in range(NUM_OF_USERS):
        if i == NUM_OF_USERS-1:
            print("%s%s,test123,%s%s" % (USERNAME, str(i), USERNAME, str(0)))
        else:
            print("%s%s,test123,%s%s" % (USERNAME, str(i), USERNAME, str(i+1)))


def main():
    """Main Function"""
    create_user()


# Executing the script.
if __name__ == "__main__":
    main()
