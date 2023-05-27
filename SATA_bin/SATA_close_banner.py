#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 16:12:18 2023

@author: GeoSeisUtilities
"""

## Importing modules
import tkinter as tk
import os
from plyer import notification
import shutil
import time

def Stop_tool():
    pt=os.getcwd()+'/temp/running'
    os.remove(pt)
    notification.notify(title = 'SATA', message = 'Tool has been stopped. Wait the next refresh to completely stop it...')

def Save_plot():
    pt=os.getcwd()+'/'
    with open(pt+'temp/path') as o:
        path=o.readline()
    path_p=path+'Plots/'
    act_tm=time.strftime("%Y-%m-%d_%H-%M-%S")
    os.mkdir(path_p+act_tm)
    shutil.copyfile(pt+'combined_plots.pdf', path_p+act_tm+'/combined_plots.pdf')
    shutil.copyfile(path_p+'Eqs_gmt.txt',path_p+act_tm+'/Eqs_gmt.txt')
    shutil.copyfile(path_p+'Eqs_gmt_world.txt',path_p+act_tm+'/Eqs_gmt_world.txt')
    
    
wd2=tk.Tk()
wd2.title("SATA status")
wd2.geometry("500x170")
wd2.resizable(width=False, height=False)
wd2.configure(background= "#E5E5E5")
txt3='''SATA is now running. You can reduce this window to icon. 
To stop the tool click the botton 'Stop tool' below (after clicking the button
this message will disappeares but the process will stop at next refresh).

SATA offer the opportunity to save the plot displayed by clicking on the
button 'Save plot' below. Plots will be saved in the storage folder 'Plots',
in a sub-folder with the name corrispondig to the time of saving.
'''
hp3 = tk.Label(wd2, text = str(txt3), justify='center',background="#E5E5E5")
hp3.pack()
hp3.configure(font=("arial", 10))
stop = tk.Button(text="Stop tool",height= 1, width=20, command = lambda: [Stop_tool(), wd2.destroy()])
stop.place(x=300, y=130)
save = tk.Button(text="Save plot",height= 1, width=20, command = Save_plot)
save.place(x=30, y=130)
wd2.mainloop()