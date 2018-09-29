# UsefulScripts
This repo contains some useful scripts which are used for easing and automate the day to day tasks.


### 1. BatchImageCompressionScript.py

**usage:** BatchImageCompressionScript.py 
>        [ -h ] 
>        [ -s <Source Directory> ]
>        [ -t <Target Directory> ]
>        [ -q <Image Quality> ]
>        [ -f <Output file names> ]  
>        [ -l <Log File> ]
>        [ -ls <Logging on/off> ]

_Batch image conversion utility. For running this program you need to have_
_imagemagick installed on your machine._

_**optional arguments:**_
*   -h `--help`            show this help message and exit
*   -s `<Source Directory>`, `--source_directory` <Source Directory>
                          Directory to read input files.
*   -t `<Target Directory>`, `--target_directory` <Target Directory>
                         Directory to save output files.
*   -q `<Image Quality>`, `--quality` <Image Quality>
                        Quality of the Image to retain.
*   -f `<Output file names>`, `--filename` <Output file names>
                        Desired output file name.
*   -l `<Log File>`, `--log_file` <Log File>
                        Path of the log file.
*   -ls `<Logging on/off>`, `--logging_onoff` <Logging on/off>
                        Logging status On/Off

*** 

### 4. BatchImageManager.py -h
**usage:** BatchImageManager.py 
>        [ -h ] 
>        [ -i <Camera Information> ]
>        [ -s <Source Directory> ]  
>        [ -t <Target Directory> ]
>        [ -cmp <Compression on/off> ]
>        [ -clq <CameraMake_#ImageQuality Eg.: Canon100D_#90> ]
>        [ -l <Log File> ]
>        [ -ls <Logging on/off> ]

[***Purpose*** - This script is useful in a situation where we want to run a compression only on specific camera make but not on others and later want to do some manual image processing using tools like gimp on some camera make images and also at the same time we also want to maintain the sequence of the images based on their capturing time not based on the image modification.]

This script will copy the images from the specified directory and all of its sub-directory to the target directory. The target directory will be the provided on the command line argument; but the final destination will be targetDir/CameraManufacurer__CameraModel/unixTimeStamp_CameraMake.JPG

Batch Image Manager is an advaced version of the Batch Image Compression utility. For running this program you need to have exif tool and imagemagick installed on your machine. This program is used for mixing the various images taken from different camera make based on their capturing time in ascending order and rename each image on thir unix timestamp.

If compression option is selected as OFF then this script wil not create any sub-directories based on camera make just it will arrange the pictures based on their capturing time. 

_**optional arguments:**_
*   -h `--help`            show this help message and exit
*   -s `<Source Directory>`, `--source_directory` <Source Directory>
                         Directory to read input files.
*   -t `<Target Directory>`, `--target_directory` <Target Directory>
                         Directory to save output files.
*   -cmp `<Compression on/off>`, `--compression` <Compression on/off>
                         Compression On/Off
*   -clq `<CameraMake_#ImageQuality Eg.: Canon100D_#90>`, `--compressionQuality` <CameraMake_#ImageQuality Eg.: Canon100D_#90>
                         Quality of the Image to retain for specific Camera make [Image Quality range is 1-100].
*   -l `<Log File>`, `--log_file` <Log File>
                        Path of the log file.
*   -ls `<Logging on/off>`, `--logging_onoff` <Logging on/off>
                        Logging status On/Off
  
***
  
### 3. BatchMP3Converter.py
**usage:** BatchMP3Converter.py
>        [ -h ] 
>        [  -s <Source Directory> ]
>        [ -t <Target Directory> ]
>        [ -l <Log File> ]
>        [ -ls <Logging on/off> ]

_Batch mp4 to mp3 conversion utility. For running this program you need to have_
_FFMPEG with mp3 codecs installed on your machine._

_**optional arguments:**_
 *   -h `--help`            show this help message and exit
*   -s `<Source Directory>`, `--source_directory` <Source Directory>
                          Directory to read input files.
*   -t `<Target Directory>`, `--target_directory` <Target Directory>
                         Directory to save output files.
*   -l `<Log File>`, `--log_file` <Log File>
                        Path of the log file.
*   -ls `<Logging on/off>`, `--logging_onoff` <Logging on/off>
                        Logging status On/Off
  
  ***

### 4. BatchRenameFiles.py

**usage:** BatchRenameFiles.py
>        [ -h ] 
>        [ -s <Source Directory> ]
>        [ -f <Output file names> ]
>        [ -l <Log File> ]
>        [ -ls <Logging on/off> ]

_Batch renaming files utility_

_**optional arguments:**_
*   -h `--help`            show this help message and exit
*   -s `<Source Directory>`, `--source_directory` <Source Directory>
                          Directory to read input files.
*   -f `<Output file names>`, `--filename` <Output file names>
                        Desired output file name.
*   -l `<Log File>`, `--log_file` <Log File>
                        Path of the log file.
*   -ls `<Logging on/off>`, `--logging_onoff` <Logging on/off>



  ***

### 5. DebianTMSParser.py

**usage:** DebianTMSParser.py 
>        [ -h ]
>        [ -f <HTML File> ]
>        [ -u <URL> ]
>        [ -t <Text File Path> ]
>        [ -l <Log File> ]
>        [ -ls <Logging on/off> ]

_HTML File parser utility for parsing Debian Testing migration 
summary packages._

_**optional arguments:**_
*   -h `--help`            show this help message and exit
*   -f `<HTML File>`, `--file` <HTML File>
                          Path of HTML file.
*   -u `<URL>`, `--url_path` <URL>
                        URL of HTML file.
*   -t `<Text File Path>`, ` --textFile_path` <Text File Path>
                               Path of the text file.
*   -l `<Log File>`, `--log_file` <Log File>
                        Path of the log file.
*   -ls `<Logging on/off>`, `--logging_onoff` <Logging on/off>


  ***

### 6. MySQLTracker.py

**usage:** MySQLTracker.py
>        [ -h ]
>        [ -d <Database Name> ]
>        [ -l <Log File> ]
>        [ -ls <Logging on/off> ]

_List the status of the MySQL and shows the processlist of the given database._

_**optional arguments:**_
*   -h `--help`            show this help message and exit
*   -f `<Database Name>`, `--database_name` <Database Name>
                             MANDATORY : Name of the database..
*   -l `<Log File>`, `--log_file` <Log File>
                        Path of the log file.
*   -ls `<Logging on/off>`, `--logging_onoff` <Logging on/off>


  ***

### 7. UserAreaStats.py

**usage:** UserAreaStats.py
>        [ -h ]
>        [ -s <Source Directory> ]
>        [ -l <Log File> ]
>        [ -ls <Logging on/off> ]

_This script is useful for finding the number of files in a given directory and if the source directory_
_is not specified on the CLI then it will give the number of files in the public__html user area and also_
_tells if a user does not have public__html directory._

_**optional arguments:**_
*   -h `--help`            show this help message and exit
*   -s `<Source Directory>`, `--source_directory` <Source Directory>
                             MANDATORY : Name of the database..
*   -l `<Log File>`, `--log_file` <Log File>
                        Directory to read input files.
*   -ls `<Logging on/off>`, `--logging_onoff` <Logging on/off>


  ***

### 8. zimbra/redeploy.sh

_This script will redeploy all the docker containers of Zimbra_


 ***

### 9. zimbra/create_user.py

_This script will create the required number of users for Zimbra perf harness test with the specified format_

Format:
user1,password,usern

 ***

