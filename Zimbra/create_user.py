# !/bin/python

import argparse

# Command line argument validation functions...
def is_valid_directory(parser, arg):
    "Function for checking specfied directory exists or not."
    if not os.path.isdir(arg):
        parser.error('The directory {} does not exist!'.format(arg))
    else:
        # File exists so return the directory
        return arg

## =========> Command line arguments parsing -- starts <========= ##
parser = argparse.ArgumentParser(description='Batch renaming files utility...')
parser.add_argument('-u','--username', help='Pattern of the username.', required=True, metavar='<Username>')
parser.add_argument('-n','--number_of_users', help='Number of users to be created.', required=True, metavar='<Number of Users>')
args = parser.parse_args()
## =========> Command line arguments parsing -- ends <========= ##

username = args.username
num_of_users = int(args.number_of_users)

def create_user():
    for i in range(num_of_users):
        if (i == num_of_users-1):
            print username + str(i) + ",test123," + username + str(0)
        else:
            print username + str(i) + ",test123," + username + str(i+1)


# Start execution of the main program
def main():
   create_user()


# Executing the script.
if __name__ == "__main__":
    main()
