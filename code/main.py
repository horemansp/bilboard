###############################################################
# Digital billboard advertising on a display using Tkinter
# Media files are imported from a USB device
# Files are presented in full HD 1920 x 1080
# settings configurable in json file on the same USB
#
# v0.1
# Creator: Patrik Horemans
# Copyrights: free to use
################################################################
# default settings
settings_json = [{"default_delay":3,"repeat":0}]
################################################################
from tkinter import *
from PIL import ImageTk, Image
import time
import os.path
import sys
import json
import glob
set_file = "settings.json"
file_exists = os.path.exists(set_file)
files = []
msg_delay = 3 #delay between adverts in seconds, overwritten by json
msg_repeat = 0 # 0 = endless loop
msg_prev_time = time.time() - 5000
msg_curr = 0
msg_to_show = ""


def read_settings(a_json):
    #read settings from json variable
    global msg_delay, msg_repeat
    print("List to read settings from:",a_json)
    msg_delay = a_json['delay']
    msg_repeat = a_json['repeat']

if file_exists:
    #read file content
    print("File exists, so reading settings")
    f = open(set_file, "r")
    settings = f.read()
    settings_json = json.loads(settings)
    f.close

read_settings(settings_json)

#show files with jpeg extension in folder
files = glob.glob("*.png")
print(files)

#create window object
win = Tk()
#win.geometry("800x600")
win.attributes('-fullscreen',True)
#Get the current screen width and height
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()


while True:
    
    if time.time() - msg_prev_time > msg_delay:
        msg_prev_time = time.time()
        print("showing message", msg_curr+1 , "from", len(files))
        image =Image.open(files[msg_curr])
        resize_image =image.resize((screen_width,screen_height))
        msg_to_show = ImageTk.PhotoImage(resize_image)
        lbl_back_picture= Label(win, image = msg_to_show)
        lbl_back_picture.place(x=0,y=0)
        msg_curr += 1
        if msg_curr == len(files):
            msg_curr = 0
    win.update()


