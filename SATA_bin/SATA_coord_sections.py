#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 27 17:40:16 2023

@author: GeoSeisUtilities
"""

## Import modules
import os
import numpy as np
from geopy import distance

## Read variables
pt=os.getcwd()+'/temp/'
with open(pt+'path') as o:
    path=o.readline()
path_p=path+'Plots/'
with open(path_p+'Eqs_gmt.txt') as o:
    ev_gmt=o.readlines()
with open(os.getcwd()+'/DISS_gmt/Strike_sez.txt') as o:
    strike=o.readlines()
## Calculate coordinates for GTM
l_ev=ev_gmt[-1]
lat=float(l_ev.split('\t')[-5])
lon=float(l_ev.split('\t')[-4])
dep=float(l_ev.split('\t')[-3])
eq_coord=[lat,lon]
strike_l=list()
coords=list()
for s in strike:
    ls=s.split(',')
    slat=float(ls[1])
    slon=float(ls[0])
    strike_l.append(float(ls[-2]))
    coords.append([slat,slon])
min_distance=np.sqrt((coords[0][0]-eq_coord[0])**2+(coords[0][1]-eq_coord[0])**2)
#Find nearest fault
for l_c in coords:
    act_distance=np.sqrt((l_c[0]-eq_coord[0])**2+(l_c[1]-eq_coord[1])**2)
    if act_distance<=min_distance:
        min_distance=act_distance
        i=coords.index(l_c)
#Calculate section strike
strike_sez=strike_l[i]-90
if strike_sez<0:
    strike_sez=strike_sez+360
elif strike_sez>360:
    strike_sez=strike_sez-360
#Calculate start and end coordinates
if strike_sez>0 and strike_sez<90:
    start_lat=lat-np.abs(np.cos((strike_sez/360)*2*np.pi)*0.50)
    start_lon=lon-np.abs(np.sin((strike_sez/360)*2*np.pi)*0.50)
    end_lat=lat+np.abs(np.cos((strike_sez/360)*2*np.pi)*0.25)
    end_lon=lon+np.abs(np.sin((strike_sez/360)*2*np.pi)*0.25)
elif strike_sez>90 and strike_sez<180:
    start_lat=lat+np.abs(np.cos((strike_sez/360)*2*np.pi)*0.50)
    start_lon=lon-np.abs(np.sin((strike_sez/360)*2*np.pi)*0.50)
    end_lat=lat-np.abs(np.cos((strike_sez/360)*2*np.pi)*0.25)
    end_lon=lon+np.abs(np.sin((strike_sez/360)*2*np.pi)*0.25)
elif strike_sez>180 and strike_sez<270:
    start_lat=lat+np.abs(np.cos((strike_sez/360)*2*np.pi)*0.50)
    start_lon=lon+np.abs(np.sin((strike_sez/360)*2*np.pi)*0.50)
    end_lat=lat-np.abs(np.cos((strike_sez/360)*2*np.pi)*0.25)
    end_lon=lon-np.abs(np.sin((strike_sez/360)*2*np.pi)*0.25)
elif strike_sez>270 and strike_sez<360:
    start_lat=lat-np.abs(np.cos((strike_sez/360)*2*np.pi)*0.50)
    start_lon=lon+np.abs(np.sin((strike_sez/360)*2*np.pi)*0.50)
    end_lat=lat+np.abs(np.cos((strike_sez/360)*2*np.pi)*0.25)
    end_lon=lon-np.abs(np.sin((strike_sez/360)*2*np.pi)*0.25)
elif strike_sez==0:
    start_lat=lat-0.50
    start_lon=lon
    end_lat=lat+0.25
    end_lon=lon
elif strike_sez==90:
    start_lat=lat
    start_lon=lon-0.50
    end_lat=lat
    end_lon=lon+0.25
elif strike_sez==180:
    start_lat=lat+0.50
    start_lon=lon
    end_lat=lat-0.25
    end_lon=lon
elif strike_sez==270:
    start_lat=lat
    start_lon=lon+0.50
    end_lat=lat
    end_lon=lon-0.25
elif strike_sez==360:
    start_lat=lat-0.50
    start_lon=lon
    end_lat=lat+0.25
    end_lon=lon
#Calculate depth of section
if dep<=0:
    end_dep=-5
elif dep>0 and dep<=10:
    end_dep=-15
elif dep>10 and dep<=20:
    end_dep=-30
elif dep>20 and dep<=30:
    end_dep=-40
elif dep>30 and dep<=40:
    end_dep=-50
elif dep>40 and dep<=50:
    end_dep=-60
elif dep>50 and dep<=60:
    end_dep=-750
elif dep>60 and dep<=70:
    end_dep=-80
elif dep>70 and dep<=80:
    end_dep=-90
elif dep>80 and dep<=90:
    end_dep=-100
elif dep>90 and dep<=100:
    end_dep=-150
elif dep>100 and dep<=150:
    end_dep=-200
elif dep>150:
    end_dep=-300
#Calculate length in km
st_p = (start_lat,start_lon)
end_p = (end_lat, end_lon)
sec_l=distance.distance(st_p, end_p).km
# export file for GMT
gmt_line=[str(sec_l),str(end_dep),str(start_lat),str(start_lon),str(end_lat),str(end_lon)]
gmt_line='\t'.join(gmt_line)
gmt_line=gmt_line.replace(' ','')
with open(pt+'sez_gmt','w') as o:
    o.write(gmt_line)
with open(pt+'last_earthquake','w') as o:
    o.write(l_ev)  
with open(pt+'old_earthquakes','w') as o:
    for l in ev_gmt[0:-1]:
        o.write(l)  
with open(pt+'old_earthquake_nohead','w') as o:
    for l in ev_gmt[1:-1]:
        o.write(l)
with open(pt+'start_lat','w') as o:
    o.write(str(start_lat))
with open(pt+'start_lon','w') as o:
    o.write(str(start_lon))
with open(pt+'end_lat','w') as o:
    o.write(str(end_lat))
with open(pt+'end_lon','w') as o:
    o.write(str(end_lon))
with open(pt+'length_sect','w') as o:
    o.write(str(sec_l))
with open(pt+'depth','w') as o:
    o.write(str(end_dep))
l_ev=l_ev.split('\t')
line=f'Last eqs: {l_ev[2]}-{l_ev[1]}-{l_ev[0][-2:]} {l_ev[3]}:{l_ev[4]}:{l_ev[5]} - {l_ev[6]} {l_ev[7]} - {l_ev[8]} km - Mag {l_ev[9]}' 
with open(pt+'all_data','w') as o:
    o.write(str(line))
with open(pt+'coord_section_map_view','w') as o:
    o.write(f'{start_lon}\t{start_lat}\n{end_lon}\t{end_lat}')
with open(pt+'coord_section_start','w') as o:
    o.write(f'{start_lon}\t{start_lat}')
with open(pt+'coord_section_end','w') as o:
    o.write(f'{end_lon}\t{end_lat}')