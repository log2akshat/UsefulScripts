#!/usr/bin/python

import subprocess

def main():
    '''Call for taking Screenshots'''
    subprocess.call(['eog'])
    subprocess.call(['sleep', '2'])
    subprocess.call(['gnome-screenshot'])


# Executing the script.
if __name__ == "__main__":
    main()
