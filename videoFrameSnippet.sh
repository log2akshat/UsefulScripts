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
# This Shell Script is useful in a situation when you have a thermal camera which
# is genrating frames out of a video when the temprature is out of range and sim-
# ultaneously there is a video camera shooting video and both the cameras are syn-
# chronized and you need video snippet of time corresponding to the failed frame 
# of the thermal camera. So, based on the failed frames timing this script will 
# snip the video from the video camera directory with the duration as specified by
# the user ussing ffmeg.
#
# NOTE: 1. You need to have ffmpeg pre installed on your machine.
#       2. This script is tailored for CentOS as in some of the distribution it will
#          not work as expected. FEEL FREE TO EDIT AND ENHANCE IT FOR CROSS PLATFORM.

#Colors
Red_Color='\033[01;31m'
Blue_Color='\033[01;34m'
Green_Color='\033[07;32m'
Green_Blink='\033[05;32m'
Reset_Color='\033[00;00m'
Magenta_Color='\033[01;35m'

echo ""
echo "${Blue_Color}*********************************************************************${Reset_Color}"
echo "${Blue_Color}|                       Failed Frames Sniping Script.               |${Reset_Color}"
echo "${Blue_Color}*********************************************************************${Reset_Color}"

# Lag time variable.
Lagtime=1

# First we define the function
ConfirmOrExit() {
	while true
	do
	echo ""
	read -p 'Please confirm (yes or no) : ' CONFIRM
	case $CONFIRM in
		y|Y|yes|YES|Yes) break ;;
		n|N|no|NO|No)
			echo -e "${Red_Color}Aborting - you entered $CONFIRM...${Reset_Color}"
			exit
			;;
		*) echo -e "${Red_Color}Please answer yes or no.${Reset_Color}";;
		esac
	done
	echo -e "You entered ${Green_Blink}$CONFIRM${Reset_Color}. Continuing..."
}

# Options:
# Option 1 : Path of the Inspection file.
echo -e "${Blue_Color}-------------------------------------------${Reset_Color}"
echo -e "${Blue_Color}| Option 1 of 5 [Path of Inspection File] |${Reset_Color}"
echo -e "${Blue_Color}-------------------------------------------${Reset_Color}"
echo""

while true
do
#while read -e -p "Please enter the path of the Inspection file : " -i "/home/akshat/Desktop/ProtoScript/Data/InspectionResults" INSPECTION_FILEPATH; do
while read -e -p "Please enter the path of the Inspection file : " -i "Data/InspectionResults" INSPECTION_FILEPATH; do
echo ""
	if [[ -z "${INSPECTION_FILEPATH}" ]]; then #Checking for empty string.
	echo -e "${Red_Color}You have not entered the inspection file path, Please re-enter it..${Reset_Color}"
else
	echo "You have entred the path : " $INSPECTION_FILEPATH
	break
fi
	done
ConfirmOrExit

# Checking the inspection file path is valid or not.
if [[ -f $INSPECTION_FILEPATH ]]; then # FILE exists and is a regular file.
	echo -e "${Green_Color}Inspection File path is valid${Reset_Color}"
	break
else
	echo -e "${Red_Color}Inspection file path provided by you is invalid!!${Reset_Color}"
fi
done

# Option 2 : Path of the Video .avi file
echo""
echo -e "${Blue_Color}--------------------------------------${Reset_Color}"
echo -e "${Blue_Color}| Option 2 of 5 [Path of Video File] |${Reset_Color}"
echo -e "${Blue_Color}--------------------------------------${Reset_Color}"
echo""

while true
do
#while read -e -p "Please enter the path of the video .avi file : " -i "/home/akshat/Desktop/ProtoScript/Data/Video/Video10.wmv" VIDEO_FILEPATH; do
while read -e -p "Please enter the path of the video .avi file : " -i "Data/Video/Video10.wmv" VIDEO_FILEPATH; do
echo ""
        if [[ -z "${VIDEO_FILEPATH}" ]]; then #Checking for empty string.
        echo -e "${Red_Color}You have not entered the video file path, Please re-enter it..${Reset_Color}"
else
        echo "You have entred the path : " $VIDEO_FILEPATH
        break
fi
        done
ConfirmOrExit

# Checking the video file path is valid or not.
if [[ -f $VIDEO_FILEPATH ]]; then # FILE exists and is a regular file.
        echo -e "${Green_Color}Video File path is valid${Reset_Color}"
	break
else
        echo -e "${Red_Color}Video file path provided by you is invalid!!${Reset_Color}"
fi
done

# Option 3 : Path of the thermal images [.png files]
echo""
echo -e "${Blue_Color}-------------------------------------------------${Reset_Color}"
echo -e "${Blue_Color}| Option 3 of 5 [Path of Failed Thermal Images] |${Reset_Color}"
echo -e "${Blue_Color}-------------------------------------------------${Reset_Color}"
echo""

while true
do
#while read -e -p "Please enter the path of the thermal images : " -i "/home/akshat/Desktop/ProtoScript/Data/" THERMAL_IMAGES_DIRPATH; do
while read -e -p "Please enter the path of the thermal images : " -i "Data/" THERMAL_IMAGES_DIRPATH; do
echo ""
        if [[ -z "${THERMAL_IMAGES_DIRPATH}" ]]; then #Checking for empty string.
        echo -e "${Red_Color}You have not entered the thermal images directory path, Please re-enter it..${Reset_Color}"
else
        echo "You have entred the path : " $THERMAL_IMAGES_DIRPATH
        break
fi
        done
ConfirmOrExit

# Checking the thermal images directory path is valid or not.
if [[ -d $THERMAL_IMAGES_DIRPATH ]]; then # DIRECTORY exists or not.
        echo -e "${Green_Color}Thermal images directory path is valid${Reset_Color}"
	break
else
        echo -e "${Red_Color}Thermal images directory path provided by you is invalid!!${Reset_Color}"
fi
done

# Option 4 : Path of the result directory.
echo""
echo -e "${Blue_Color}-------------------------------------------------${Reset_Color}"
echo -e "${Blue_Color}| Option 4 of 5 [Path of the Results Directory] |${Reset_Color}"
echo -e "${Blue_Color}-------------------------------------------------${Reset_Color}"
echo""

while true
do
#while read -e -p "Please enter the path of the results directory : " -i "/home/akshat/Desktop/ProtoScript/Data/Results/" RESULTS_DIRPATH; do
while read -e -p "Please enter the path of the results directory : " -i "Data/Results/" RESULTS_DIRPATH; do
echo ""
        if [[ -z "${RESULTS_DIRPATH}" ]]; then #Checking for empty string.
        echo -e "${Red_Color}You have not entered the results directory basepath where results will be saved, Please re-enter it..${Reset_Color}"
else
        echo "You have entred the path : " $RESULTS_DIRPATH
        break
fi
        done
ConfirmOrExit

echo ""
if [[ -d $RESULTS_DIRPATH ]]; then # DIRECTORY exists or not.
        echo -e "${Green_Color}Results directory path is valid${Reset_Color}"
	break
else
        echo -e "${Red_Color}Results directory path provided by you is invalid!!${Reset_Color}"
fi
done

# Custom name of the directory from user input.
echo ""
while read -e -p "Please enter the name of the directory : " CUSTOM_DIRNAME; do
echo ""
if [[ -z "${CUSTOM_DIRNAME}" ]]; then #Checking for empty string.
        echo -e "${Red_Color}You have not entered the name of the directory to save results, Please re-enter it..${Reset_Color}"
else
        echo "You have entred the name of the directory : " $CUSTOM_DIRNAME
        break
fi
        done
ConfirmOrExit

# Create custom directory for saving the results.
timestamp=`date +"%F_%Hh%Mm%Ss"`
CustomDirName=$RESULTS_DIRPATH$CUSTOM_DIRNAME
mkdir -pv "$CustomDirName"
ResultsDirName=$CustomDirName/$timestamp
mkdir "$ResultsDirName"

# Option 5 : Snippet section time in seconds.
echo""
echo -e "${Blue_Color}---------------------------------------------------------------------${Reset_Color}"
echo -e "${Blue_Color}| Option 5 of 5 [Snippet section time (in seconds) from Video File] |${Reset_Color}"
echo -e "${Blue_Color}---------------------------------------------------------------------${Reset_Color}"
echo""

while true
do
while read -e -p "Please enter the time <t> (+/- t seconds) to snip from video file : " SNIP_TIME; do
echo ""
        if [[ -z "${SNIP_TIME}" ]]; then #Checking for empty string.
        echo -e "${Red_Color}You have not entered the snipping time. Please re-enter it..${Reset_Color}"
else
        echo "You have entred : " $SNIP_TIME "seconds."
        break
fi
        done
ConfirmOrExit

# Checkeing the entred snipping time is integer and positive.
if [ -z "$SNIP_TIME" -o -n "`echo $SNIP_TIME | tr -d '[0-9]'`" ]; then
        echo -e "${Red_Color}Entered time is invalid!!${Reset_Color}"
else
        echo -e "${Green_Color}Entered time is correct.${Reset_Color}"
	break	
fi
done

# ***************** All options finished ******************************
# Main Script starts from here.
echo ""
#if grep '\bFail\b' "$INSPECTION_FILEPATH"; then
#   echo "Fail are present."
#fi

IFS_BAK=${IFS}
    IFS=$'\n'

   FailedResults=( $(cat $INSPECTION_FILEPATH | grep Fail | tail -n +2) )
   First_Captured_Frame=`ls -ltrh -g -G --time-style=full-iso $THERMAL_IMAGES_DIRPATH | cut -d" " -f4,5 | tail -n +2 | head -n1`
   FailedResults_SecondsCalibration=( $(ls -ltrh -g -G --time-style=full-iso $THERMAL_IMAGES_DIRPATH | cut -d" " -f4,5,7 | tail -n +2 | grep Fail | sed "s/ /#/g") )
	
	echo ""	
	echo "**************************************************"	
	echo "${FailedResults_SecondsCalibration[@]}"
    	length=${#FailedResults[@]}
	echo "**************************************************"	
	echo "First_Captured_Frame : " $First_Captured_Frame
	echo "**************************************************"	
	echo ""	
	

for (( i=0; i<$length; i++ ));
do
        echo "${FailedResults[$i]}" 
	FailedDirName=`echo "${FailedResults[$i]}" | cut -f1 -s`
	FailedDirName+="-"
        MaxTemp=`echo "${FailedResults[$i]}" | cut -f3 -s`
        FailedDirName+=$MaxTemp
	FailedDirName+="-Fail"
	
	# Creating Directory
	echo "Creating directory $FailedDirName..."
	mkdir "$ResultsDirName/$FailedDirName"
	
	#Failed Image Name
	FailedImageName=`echo "${FailedResults[$i]}" | cut -f1 -s`
	FailedImageName+="-"
	MaxTemp=`echo "${FailedResults[$i]}" | cut -f3 -s`
	FailedImageName+=$MaxTemp
	FailedImageName+="-Fail.PNG"
	
	# Copying failed images to the results directory.
	echo "Copying Image $FailedImageName to the Directory $FailedDirName..."
	cp $THERMAL_IMAGES_DIRPATH/$FailedImageName $ResultsDirName/$FailedDirName
	
	#---------------------------------------------------------------------------------------------------------------------#
	# Calculation of thermal camera calibration.
	# Calculating the milliseconds of the first frame from the epoh time.
        I_Frame_from_EpohTime=`echo $(($(date -d "$First_Captured_Frame" +%s%N)/1000000))`

	# Calculating the milliseconds of subsequent frame from the epoh time.
	FailedResults_ArrayManipulation=`echo ${FailedResults_SecondsCalibration[$i]} | cut -d"#" -f1,2 | sed "s/#/ /g"`
	Next_Frame_from_EpohTime=`echo $(($(date -d "$FailedResults_ArrayManipulation" +%s%N)/1000000))`

	echo "Epoch time is of the first frame is : " $I_Frame_from_EpohTime
	Calibrated_Milliseconds=`echo "$Next_Frame_from_EpohTime-$I_Frame_from_EpohTime" | bc -l`
	Calibrated_Seconds=$(expr $Calibrated_Milliseconds/1000 | bc -l)
	Calibrated_Seconds_rounded=`echo "$Calibrated_Seconds" | awk '{printf("%.1f", $1)}'`
        echo ""
        echo "-----------------------------------------------------------------------------------------------------------------------------"
	echo "Calibrated Milliseconds : " $Calibrated_Milliseconds " AND Calibrated Seconds : " $Calibrated_Seconds_rounded " ALL : " $Calibrated_Seconds
        echo "-----------------------------------------------------------------------------------------------------------------------------"
        echo ""
	#---------------------------------------------------------------------------------------------------------------------#
	
	# Mathematical calculations for snipping time.
        #Snipseconds=`echo "${FailedResults[$i]}" | cut -f1 -s`
        #Sniptime_Multiply=$(expr $Snipseconds*0.1 | bc -l) #`echo $Snipseconds * 0.1 | bc -l` #$(($Snipseconds * 0.1))
        #Sniptime_Start_Subtract=`echo "$Sniptime_Multiply - $SNIP_TIME" | bc -l`
        Sniptime_Start_Subtract=`echo "$Calibrated_Seconds_rounded - $SNIP_TIME" | bc -l`
        Sniptime_Start=`echo "$Sniptime_Start_Subtract - $Lagtime" | bc -l`
        echo "-------------------------------------------------------------------------------"
        echo "Snipping start time is : "$Sniptime_Start "with a lag of " $Lagtime " second(s)."
        Sniptime_End=$(($SNIP_TIME * 2))
        echo "Duration of the Snipping time is : " $Sniptime_End
        echo "-------------------------------------------------------------------------------"

	# Name of the Failed Video Clip
	SnippedVideoName=`echo "${FailedResults[$i]}" | cut -f1 -s`
        SnippedVideoName+="-"
        SnippedVideoName+=$MaxTemp
        SnippedVideoName+="-Fail.wmv"	

	# Running ffmpeg command to snip the video file
	ffmpeg -i $VIDEO_FILEPATH -ss $Sniptime_Start -t $Sniptime_End -acodec copy -vcodec copy -y $ResultsDirName/$FailedDirName/$SnippedVideoName
done
    # Set IFS back to normal..
    IFS=${IFS_BAK}

# Cleaning the Processing directory
echo ""
echo -e "${Red_Color}Do you want to clean up the processing directory?${Reset_Color}"
ConfirmOrExit

echo ""
echo -e "${Blue_Color}---------------------------------------------------${Reset_Color}"
echo -e "${Blue_Color} Cleaning up the processing files and directories. ${Reset_Color}"
echo -e "${Blue_Color}---------------------------------------------------${Reset_Color}"
echo ""
mkdir "$ResultsDirName/"DATA
mv "$INSPECTION_FILEPATH" "$VIDEO_FILEPATH" "$THERMAL_IMAGES_DIRPATH" "$ResultsDirName/"DATA

echo -e "${Red_Color}                                                                       ${Reset_Color}"
echo -e "${Red_Color}████████╗    ██╗  ██╗     █████╗     ███╗   ██╗    ██╗  ██╗    ███████╗${Reset_Color}"
echo -e "${Red_Color}╚══██╔══╝    ██║  ██║    ██╔══██╗    ████╗  ██║    ██║ ██╔╝    ██╔════╝${Reset_Color}"
echo -e "${Red_Color}   ██║       ███████║    ███████║    ██╔██╗ ██║    █████╔╝     ███████╗${Reset_Color}"
echo -e "${Red_Color}   ██║       ██╔══██║    ██╔══██║    ██║╚██╗██║    ██╔═██╗     ╚════██║${Reset_Color}"
echo -e "${Red_Color}   ██║       ██║  ██║    ██║  ██║    ██║ ╚████║    ██║  ██╗    ███████║${Reset_Color}"
echo -e "${Red_Color}   ╚═╝       ╚═╝  ╚═╝    ╚═╝  ╚═╝    ╚═╝  ╚═══╝    ╚═╝  ╚═╝    ╚══════╝${Reset_Color}"
echo -e "${Red_Color}                                                                       ${Reset_Color}"
