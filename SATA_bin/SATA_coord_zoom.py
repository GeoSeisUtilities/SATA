#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 27 17:40:16 2023

@author: 
"""

## Import modules
import os

## Read variables
pt=os.getcwd()+'/temp/'
with open(pt+'path') as o:
    path=o.readline()
path_p=path+'Plots/'
with open(path_p+'Eqs_gmt.txt') as o:
    ev_gmt=o.readlines()

## Calculate coordinates for GTM
l_ev=ev_gmt[-1]
lat=l_ev.split('\t')[-4]
lon=l_ev.split('\t')[-3]
lat_un=lat.split('.')[0]
lon_un=lon.split('.')[0]
lat_dec=lat.split('.')[-1]
lon_dec=lon.split('.')[-1]
if int(lat_dec)<=2500:
    lat_max=lat_un+'.'+'50'
    lat_min=str(int(lat_un)-1)+'.'+'50'
elif int(lat_dec)>2500 and int(lat_dec)<=5000:
    lat_max=lat_un+'.'+'75'
    lat_min=str(int(lat_un)-1)+'.'+'75'
elif int(lat_dec)>5000 and int(lat_dec)<=7500:
    lat_max=str(int(lat_un)+1)+'.'+'00'
    lat_min=lat_un+'.'+'00'
else:
    lat_max=str(int(lat_un)+1)+'.'+'25'
    lat_min=lat_un+'.'+'25'
if int(lon_dec)<=2500:
    lon_max=lon_un+'.'+'75'
    lon_min=str(int(lon_un)-1)+'.'+'50'
elif int(lon_dec)>2500 and int(lon_dec)<=5000:
    lon_max=str(int(lon_un)+1)+'.'+'00'
    lon_min=str(int(lon_un)-1)+'.'+'75'
elif int(lon_dec)>5000 and int(lon_dec)<=7500:
    lon_max=str(int(lon_un)+1)+'.'+'25'
    lon_min=lon_un+'.'+'00'
else:
    lon_max=str(int(lon_un)+1)+'.'+'50'
    lon_min=lon_un+'.'+'25'
gmt_line=lon_min+'/'+lon_max+'/'+lat_min+'/'+lat_max
with open(pt+'coord_gmt','w') as o:
    o.write(gmt_line)
