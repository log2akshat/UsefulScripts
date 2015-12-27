#!/bin/bash

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
#
#
# This Shell Script can be used to restrict the mounting of USB in the system
# based on their filesystem. This script will allow ext, exfat and hfsplus file
# system to be mounted and browsable if it is any other filesytem it will get
# unmounted automatically after poping up the error..
# NOTE : The logs from the attached script is generated at the following location:
#		/tmp/USBUdev.log_TIMESTAMP
#        
# This script will create a directory with the name of LABEL_NAME and mount the 
# USB disk at the following location:
# /media/EXTERNAL_DRIVES/USB_LABELNAME
#
# You have to put the udev provided in a seperate file at the following location:
# /etc/udev/rules.d/ and rename it according to the priority.
#
#        FEEL FREE TO EDIT FOR YOUR OWN CUSTOMIZED USAGE.
#
# Dependencies : Zenity
# 
# SCRIPT: USBHack.sh ver 1.0, 19-Nov-15
# AUTHOR: Akshat Singh
# PURPOSE: mounting the usb ext, exfat, hfsplus drives by the udev rules.


logTime=`date +%d%b%Y_%H-%M-%SHRS`
time=`date +%s`
logDirectory="/tmp/USBUdev.log_$logTime"
`/usr/bin/touch $logDirectory`
`/usr/bin/chmod 777 $logDirectory`
echo "Log is saved in the directory : " $logDirectory
`rm -rf /tmp/USBUdev*`

{
echo "udev script started..."
echo "USB Device Node : $1"
echo "Filesystem detected : $2"
echo "Kernel : $3"
echo "USB LABEL : $ID_FS_LABEL"
echo "ID_SERIAL : $ID_SERIAL_SHORT"


# This is needed for notify-send
export DISPLAY=":0"

mountLocation="/media/EXTERNAL_DRIVES"

if [ $2 = "ext3" ] || [ $2 = "ext4" ] || [ $2 = "hfsplus" ] || [ $2 = "exfat" ]; then
  `mkdir -p $mountLocation/$ID_FS_LABEL`
  echo "Going to mount $1 usb device at $mountLocation"
  `/usr/bin/mount -t $2 $1 $mountLocation/$ID_FS_LABEL`

if [ $? -eq 0 ]
then
    echo "Mounted usb drive at $mountLocation/$ID_FS_LABEL."
    username=`who | head -n 1 | cut -d " " -f 1`
    su $username -c "zenity --title='USB Detected' --question --text 'Mounted your usb drive at $mountLocation/$ID_FS_LABEL \n\n Do you want to browse?'"
    ## if condition for browse popup.
    if [ $? -eq 0 ]
    then
	 su $username -c "nautilus $mountLocation/$ID_FS_LABEL/"
    fi
## else condition for mount failed for the supported filesystems.
else
    su $username -c "zenity --error --text 'Error \n\n Mounting your usb drive failed.'"
    echo "'Error - Mounting of usb drive failed."
fi

## else condition for detecting any other filesystem other than ext3, ext4, hfsplus, exfat.
else
  username=`who | head -n 1 | cut -d " " -f 1`
  su $username -c "zenity --error --text 'Error \n\n Unsupported Filesystem - $2'"
  echo "Unsupported Filesystem - $2 drive detected."
  `umount $1`
  su $username -c "zenity --warning --text 'Alert \n\n Unsupported Filesystem - $2 \n Drive $ID_FS_LABEL unmounted.'"
  echo "Unsupported Filesystem - $2. Drive $ID_FS_LABEL unmounted."
fi

} | 2>&1 tee >> $logDirectory
