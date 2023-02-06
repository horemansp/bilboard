###############################################################
# Digital billboard advertising on a display using Tkinter
# Media files are imported from a USB device (jpeg or png)
# USB stick needs to have bilboard.json in it's root directory
# image files in the root directory will be listed and displayed automatically
# Files will be resized to screen resolution
# Settings configurable in json file on the USB
# Use single display on HDMI0
# v1
# Creator: Patrik Horemans
# Copyrights: free to use
################################################################
# default settings
settings_json = [{"default_delay":3}]
################################################################


import os
import json
from tkinter import *
from PIL import ImageTk, Image
import time
import signal
user_env = "koekoek" #depends on RPI installation. Default this user is Pi
file_types = ["jpeg","png"]
files_to_show = []
files_to_show_exist = False
settings_file = "bilboard.json"
settings_file_found = False
USB_drives_found = False
msg_prev_time = time.time() - 5000
msg_curr = 0
msg_to_show = ""


while not USB_drives_found:
    try:
        drives = os.listdir("/media/" + user_env)
        if len(drives) > 0:
            USB_drives_found = True
            print("USB drive(s) found:")
            print(drives)
        else:
            print("No USB drives found")
        time.sleep(10)
    except:
        print('could not list USB drives')
        time.sleep(10)

if USB_drives_found:
    for drive in drives:
        files = os.listdir("/media/" + user_env + "/" + drive)
        if settings_file in files:
            USB_path = "/media/" + user_env + "/" + drive
            USB_files = files
            print("bilboard usb found on " + USB_path)
            settings_file_found = True
            break
        else:
            print("no bilboard usb found")
        
if settings_file_found:
    for file in USB_files:
        for file_type in file_types:
            if file_type in file:
                if not(file.startswith(".")) and not(file.startswith("koekoek")):
                    files_to_show_exist = True
                    files_to_show.append(file)
            
if files_to_show_exist:
    print("Valid files to show:")
    print(files_to_show)
    
def read_settings(a_json):
    #read settings from json variable
    global msg_delay, msg_repeat
    print("List to read settings from:",a_json)
    msg_delay = a_json['delay']

if settings_file_found:
    #read file content
    print("File exists, so reading settings")
    f = open(USB_path + "/" + settings_file, "r")
    settings = f.read()
    settings_json = json.loads(settings)
    f.close
    read_settings(settings_json)

if files_to_show_exist:
    #create window object
    win = Tk()
    #win.geometry("400x300")
    win.attributes('-fullscreen',True)
    #Get the current screen width and height
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    print("Screenwidth & height:",screen_width,"x",screen_height) 

while files_to_show_exist:
    if time.time() - msg_prev_time > msg_delay:
        msg_prev_time = time.time()
        print("showing message", msg_curr+1 , "from", len(files_to_show))
        image =Image.open(USB_path + "/" + files_to_show[msg_curr])
        resize_image =image.resize((screen_width,screen_height))
        msg_to_show = ImageTk.PhotoImage(resize_image)
        lbl_back_picture= Label(win, image = msg_to_show)
        lbl_back_picture.place(x=0,y=0)
        msg_curr += 1
        if msg_curr == len(files_to_show):
            msg_curr = 0
        win.update()
    
