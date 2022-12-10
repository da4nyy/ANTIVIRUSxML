#!/usr/bin/env python3



"""
File Integrity Monitor with malware detection

@author: DA4NY
"""

# LIBRARIES NEEDED
import subprocess
import os
import sys
import pickle 
import datetime
import hashlib	
import logging
import time 
import signal
from time import sleep
import dictdiffer 
from progress.bar import Bar

#==================
#change here !
#==================


import sys
import getopt


import getopt
import sys

def get_args(argv):
    arg_input = ""
    arg_output = ""

    arg_help = "{0} -i <input directory> -o <output directory> ".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hi:o", ["help", "input=", "output="])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)
            sys.exit(2)
        elif opt in ("-i", "--input"):
            arg_input = arg
            print('input directory:', arg_input)

        elif opt in ("-o", "--output"):
            arg_output = arg
            print('output directory:', arg_output)


    l = [arg_input,arg_output]
    return l




    







#===============
# Colors
#===============
# Normal 
black="\033[0;30m"
red="\033[0;31m"
green="\033[0;32m"
yellow="\033[0;33m"  
blue="\033[0;34m"
purple="\033[0;35m"
cyan="\033[0;36m"
white="\033[0;37m"
# Bold
bblack="\033[1;30m"
bred="\033[1;31m"
bgreen="\033[1;32m"
byellow="\033[1;33m"
bblue="\033[1;34m"
bpurple="\033[1;35m"
bcyan="\033[1;36m"
bwhite="\033[1;37m"


#======================
#printing Banner
#======================

def banner():
    logo='''
'''+byellow+'''                                   
'''''' mmmm     mm      mm  mm   mm     m
'''''' #   "m   ##     m"#  #"m  # "m m" 
'''''' #    #  #  #   #" #  # #m #  "#"  
'''''' #    #  #mm#  #mmm#m #  # #   #   
'''''' #mmm"  #    #     #  #   ##   #   
''''''                                   
                                
'''+byellow+''' ++ File Integrity Monitor ith Malware Detection ++ 

'''+bblue+''' 
*) Creates alerts for:
        - added files
        - removed files
        - changed files

*) detect if the added / changed file is a malware       

*) checks the signature of the file with virustotal api 

'''+red+''' 
@author: DA4NY

'''+bwhite+''''''
    print(logo)



#==========================
#Count all files in the directory and its subdirectories
#we will use it in the progress bar
#=========================

def count(SCAN_DIR):
	var = 0
	for dirName, subdirList, fileList in os.walk(SCAN_DIR):
	            
	            if (list_to_ignore):
	                for ignore in list_to_ignore:
	                    
	                    # if ignore in the list
	                    if (ignore in fileList):
	                        fileList.remove(ignore)
	            var+=1
	return var


#*********************
#scanning files 
#*********************
def scan_files(SCAN_DIR, list_to_ignore, LOG_FILE):
    
    try:
        # hold directories and files
        files = dict()
        
    		
        
        # recursively walk to directory tree and get files
        with Bar('Scanning Files ...',max=count(SCAN_DIR)) as bar:  #using a progress bar while scanning the files  
	        for dirName, subdirList, fileList in os.walk(SCAN_DIR):
	            
	            if (list_to_ignore):
	                for ignore in list_to_ignore:
	                    
	                    # if ignore in the list
	                    if (ignore in fileList):
	                        fileList.remove(ignore)
	                        
	            files[str(dirName)] = fileList
	            sleep(0.02)
	            bar.next()

        return files
            
    except Exception as e:
    	msg="Error in scanning files and dirs !"
    	logging.exception(msg)
        
        


#storing hashes

def save_hash(dictionary, file, LOG_FILE):
    
    try:
        # open the file to use to save the dictionary
        initial_scan_file = open(file, "wb")
        
        # use pickle to save the dictionary
        pickle.dump(dictionary, initial_scan_file)
        
        # close the file
        initial_scan_file.close
        
    except Exception as e:
    	msg="Error while saving the dictionary"
    	logging.exception(msg)




# Load dictionary of hashes

def load_dict(file, LOG_FILE):
    
    try:
        # open the pickle file to load
        infile = open(file, 'rb')
        
        # use pickle to load the dictionary
        loaded_dict = pickle.load(infile)
        
        # close the file
        infile.close()

        return loaded_dict
        
    except Exception as e:
        log(LOG_FILE, \
            "Error while loading the dictionary")
    
    


# Log events

def log(log_dir, message):
    
    # get time
    currentDT = datetime.datetime.now()
    
    # log event
    file = open(log_dir, "a+")
    file.write(str(message) + \
               " --- Time: " + \
               str(currentDT.strftime("%Y-%m-%d %H:%M:%S")) + \
               "\n")
    file.close
    

def log_change(log_dir, message):
    
    # get time
    currentDT = datetime.datetime.now()
    
    # log event test
    file = open(log_dir, "a+")
    file.write(str(message) + \
               " --- Time: " + \
               str(currentDT.strftime("%Y-%m-%d %H:%M:%S")) + \
               "\n")
    file.close
    print(red,message,white)




# Take SHA256 of each file
# hash is taken in blocks, this is done to ensure large files doens't fail

def calculate_hash(directory, LOG_FILE):
    
    try:
        # use hash libraries sha 256
        sha256_hash = hashlib.sha256()
        
        # take hash
        with open(directory,"rb") as f:
            
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096),b""):
                sha256_hash.update(byte_block)
                
            # return the hash
            return sha256_hash.hexdigest()
        
    except Exception as e:
        log(LOG_FILE,"Error while taking the hash values")




# integrity FUNCTION

def integrity():                       
    

    #printing the directory to scan 
    print("DIRECTORY TO MONITOR :{} ".format(SCAN_DIRECTORY))

    # start the initial scan
    log(LOG_FILE, "Starting the initial scan...")


    INITIAL_FILE_HASHES = scan()
    
    # save the initial scan dictionary of hashes
    save_hash(INITIAL_FILE_HASHES, \
                           SCAN_STORAGE,\
                           LOG_FILE)
    log(LOG_FILE, "Initial scan completed!")
    
    
    # start the integrity check
    log(LOG_FILE, "Starting the integrity check...")
   	
    while True:
        
        # get the file hashes
        new_hash = scan()
        
        # load the old hash
        old_hash = load_dict(SCAN_STORAGE,\
                                          LOG_FILE)
        
        # compare two dict of hashes
        for diff in list(dictdiffer.diff(old_hash, new_hash)):         
            # ALERT
            
            log_change(ALERT_FILE, diff)
            malware_detection(diff)
        # save the new hash
        save_hash(new_hash, \
                               SCAN_STORAGE,
                               LOG_FILE)
        
        # wait
        sleep(sleep_time_sc)
        



# Scan the directory tree and take hash of the files 
# Return a dictionary of hashes and file paths

def scan():
    
    # get dictonary of directories and files they contain
    directories = scan_files(SCAN_DIRECTORY, \
                                                     list_to_ignore, \
                                                     LOG_FILE)        
    
    # take hash
    file_hashes = dict()
    for path, files in directories.items():
        
        # look at each file at path
        for file in files:
            
            # get the full path name to the file
            file_dir = str(path) + "/" + str(file)
            
            # store the hash of the file
            file_hashes[file_dir] = calculate_hash(file_dir, \
                       LOG_FILE)
            
            
    # return dictionary with files path and hashes
    return file_hashes





def malware_detection(diff):
    with open(ALERT_FILE, "r+") as alert_file:
          for line in alert_file:
              pass
          
          test = line.split("'")
          if test[1]== "change":
              file_to_scan = test[3]
          if test[1]=="add":
              file_to_scan = test[5]
          
          print(bgreen,"[+] Scanning {} ...".format(file_to_scan),bwhite)
          if file_to_scan[0]== ".":
              extention =  file_to_scan[1:] 
          try :   
              if extention.split(".")[1] =="exe":
                  
                  try : 
                      subprocess.call(['python3','Mal-detection.py', file_to_scan])
                  except : 
                      print(bred ,"[x] Failed to run the Malware detection !!!",bwhite )
              else: 
                  print(bred,"[x] The file isn't a windows executable !!! Currently we can only can windows x32 files !")     
                  print(bgreen,"[+] Trying the virus total api ... ",bwhite)
                  api_virus_total(file_to_scan)
          except: 
              print(bred,"[x] The file isn't a windows executable !!! Currently we can only can windows x32 files !")     
              print(bgreen,"[+] Trying the virus total api ... ",bwhite)
              api_virus_total(file_to_scan)
      


 

def api_virus_total(file):
    subprocess.call(['python3','virustotal.py','-m',file])
def hand_sign(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n :")
    if res == 'y':
    	print(red,"[x] Quitting!\n",bgreen,"[+] Saving the results in {} ".format(ALERT_FILE))
    	exit(1)
 
signal.signal(signal.SIGINT, hand_sign)

# execute
if __name__ == "__main__":
    l=[]
    SCAN_DIRECTORY = '.'
    ALERT_FILE = 'alert.log'
    l= get_args(sys.argv)
    if l[0]!="":
        SCAN_DIRECTORY = l[0]
    if l[1]!="":
        ALERT_FILE = l[1]
    


    SCAN_STORAGE = 'hashes.pkl'
    LOG_FILE = 'handler.log'
    list_to_ignore=[SCAN_STORAGE, LOG_FILE, ALERT_FILE]
    sleep_time_sc=4
    print(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+"\n")
    #Starting the integrity monitor
    banner()
    integrity()

    
