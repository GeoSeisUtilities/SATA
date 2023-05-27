# -*- coding: utf-8 -*-
"""
Created on Tue May 16 19:45:25 2023

@author: GeoSeisUtilities
"""

## Importing modules
import time
import tkinter as tk
from tkinter import filedialog
import os
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import shutil
from plyer import notification

## Define functions for GUI
def First_download():
    notification.notify(title = 'SATA', message = 'First download has started. It need some minutes please be patient...')
    It_lat=[35,49]
    It_lon=[5,20]
    pt=os.getcwd()+'/temp/'
    with open(pt+'path') as o:
        path=o.readline()
    path_e=path+'Earthquakes/'
    path_p=path+'Plots/'
    act_tm=time.strftime("%Y-%m-%d")
    dt = datetime.strptime(act_tm, "%Y-%m-%d")
    st = dt - timedelta(days=7)
    st=st.strftime("%Y-%m-%d")
    url = 'http://terremoti.ingv.it/events?starttime=2023-05-12+00%3A00%3A00&endtime=2023-05-19+23%3A59%3A59&last_nd=7&minmag=-1&maxmag=10&mindepth=-10&maxdepth=1000&minlat=-90&maxlat=90&minlon=-180&maxlon=180&minversion=100&limit=30&orderby=ot-desc&lat=0&lon=0&maxradiuskm=-1&wheretype=area'
    st_time=url[42:52]
    end_time=url[74:84]
    url=url.replace(st_time,st)
    url=url.replace(end_time,act_tm)
    # Read url page
    response = requests.get(url)
    html = BeautifulSoup(response.text, 'html.parser')
    earthquake_list=list()
    header=['Id','Time_or','Time_err','Lat','Lat_err','Lon','Lon_err','Depth','Dep_err','Mag_type','Mag','Mag_err','Az_gap','Phases','RMS','Act_st','ID_loc']
    header='\t'.join(header)
    earthquake_list.append(header+'\n')
    header_gmt=['Year','Mo','Da','HH','mm','ss','Lat','Lon','Dep','Mag']
    ev_gmt=list()
    header_gmt='\t'.join(header_gmt)
    ev_gmt.append(header_gmt+'\n')
    ev_gmt_w=list()
    ev_gmt_w.append(header_gmt+'\n')
    tot_ev = int(html.find('span', class_="badge").get_text())
    # Extract links
    url_l = list()
    for link in html.find_all('a'):
        url_l.append(link.get('href'))
    st=62
    en=242
    while True:
        try:
            int(url_l[st].split('/')[-1])
            break
        except:
            st+=1
            en+=1
    url_e=url_l[st:en:6]
    # Read number of pages
    try:
        n_pg = int(url_l[-11].split('=')[-1])
    except:
        n_pg=0
    if n_pg!=0:
        # Find next page link
        next_pg = url_l[-10]
        #Find all event links
        for i in range(n_pg-2):
            # Read html
            response1 = requests.get(next_pg)
            html1 = BeautifulSoup(response1.text, 'html.parser')
            # Get all links
            url_l = list()
            for link in html1.find_all('a'):
                url_l.append(link.get('href'))
            # Get event links
            st=66
            en=242
            while True:
                try:
                    int(url_l[st].split('/')[-1])
                    break
                except:
                    st+=1
                    en+=1
            url_e1=url_l[st:en:6]
            for u in url_e1:
                url_e.append(u)
            # Find link of next page
            next_pg = url_l[-10]
        response1 = requests.get(next_pg)
        html1 = BeautifulSoup(response1.text, 'html.parser')
        # Get all links
        url_l = list()
        for link in html1.find_all('a'):
            url_l.append(link.get('href'))
        # Get event links
        st=62
        while True:
            try:
                int(url_l[st].split('/')[-1])
                break
            except:
                st+=1
                en+=1
        n_last_pg=tot_ev-(n_pg-1)*30
        url_e1=url_l[st:st+n_last_pg*6:6]
        for u in url_e1:
            url_e.append(u)
    # Remove wrong links
    url1=url_e[:]
    url_e=list()
    for u in url1:
        try:
            int(u.split('/')[-1])
            url_e.append(u)
        except:
            continue
    url_e.reverse()
    # Read eqs pages and extrapolate information
    for u in url_e:
        ev_id=u.split('/')[-1]
        event = requests.get(u)
        html = BeautifulSoup(event.text, 'html.parser')
        eqs_info=html.findAll('div', class_="panel panel-primary")[5].get_text()
        mag_info=html.findAll('div', class_="panel panel-primary")[6].get_text()
        # clear spurius characters
        eqs_info=eqs_info.replace('	',' ')
        while '  ' in eqs_info:
            eqs_info=eqs_info.replace('  ',' ')
        while '\n\n' in eqs_info:
            eqs_info=eqs_info.replace('\n\n','\n')
        while '\n \n' in eqs_info:
            eqs_info=eqs_info.replace('\n \n','\n')
        mag_info=mag_info.replace('	',' ')
        while '  ' in mag_info:
            mag_info=mag_info.replace('  ',' ')
        while '\n\n' in mag_info:
            mag_info=mag_info.replace('\n\n','\n')
        while '\n \n' in mag_info:
            mag_info=mag_info.replace('\n \n','\n')
        # extract info and add to list
        eqs_info=eqs_info.split('\n')
        try:
            eqs_time=eqs_info[eqs_info.index('Tempo (UTC)')+1]
            try:
                float(eqs_info[eqs_info.index('Tempo (UTC)')+2].replace(' ± ',''))
                eqs_time_un=eqs_info[eqs_info.index('Tempo (UTC)')+2].replace(' ± ','')
            except:
                eqs_time_un='-'
            eqs_lat=eqs_info[eqs_info.index('Latitudine')+1]
            try:
                float(eqs_info[eqs_info.index('Latitudine')+2].replace(' ± ',''))
                eqs_lat_un=eqs_info[eqs_info.index('Latitudine')+2].replace(' ± ','')
            except:
                eqs_lat_un='-'
            eqs_lon=eqs_info[eqs_info.index('Longitudine')+1]
            try:
                float(eqs_info[eqs_info.index('Longitudine')+2].replace(' ± ',''))
                eqs_lon_un=eqs_info[eqs_info.index('Longitudine')+2].replace(' ± ','')
            except:
                eqs_lon_un='-'
            eqs_dep=eqs_info[eqs_info.index('Profondità (km)')+1]
            try:
                float(eqs_info[eqs_info.index('Profondità (km)')+2].replace(' ± ',''))
                eqs_dep_un=eqs_info[eqs_info.index('Profondità (km)')+2].replace(' ± ','')
            except:
                eqs_dep_un='-'
            try:
                int(eqs_info[eqs_info.index('ID localizzazione')+1])
                eqs_id_loc=eqs_info[eqs_info.index('ID localizzazione')+1]
            except:
                eqs_id_loc='-'
            try:
                float(eqs_info[eqs_info.index('Maggiore gap azimutale nella distribuzione delle stazioni all\'epicentro')+1])
                eqs_gap=eqs_info[eqs_info.index('Maggiore gap azimutale nella distribuzione delle stazioni all\'epicentro')+1]
            except:
                eqs_gap='-'
            try:
                int(eqs_info[eqs_info.index('Numero di fasi')+1])
                eqs_ph=eqs_info[eqs_info.index('Numero di fasi')+1]
            except:
                eqs_ph='-'
            try:
                float(eqs_info[eqs_info.index('Scarto quadratico medio dei residui di tempo risultanti dal calcolo del tempo origine (Origin) della localizzazione (sec)')+1])
                eqs_rms=eqs_info[eqs_info.index('Scarto quadratico medio dei residui di tempo risultanti dal calcolo del tempo origine (Origin) della localizzazione (sec)')+1]
            except:
                eqs_rms='-' 
            try:
                int(eqs_info[eqs_info.index('Numero di stazioni in cui l’evento e’ stato osservato')+1])
                eqs_st=eqs_info[eqs_info.index('Numero di stazioni in cui l’evento e’ stato osservato')+1]
            except:
                eqs_st=eqs_info[49] 
            mag_info=mag_info.split('\n')
            mag_type=mag_info[mag_info.index('Tipo di magnitudo')+1]
            mag_val=mag_info[mag_info.index('Valore')+2]
            try:
                float(mag_info[mag_info.index('Incertezza')+1])
                mag_unc=mag_info[mag_info.index('Incertezza')+1]
            except:
                mag_unc='-'
        except:
            eqs_time=eqs_info[eqs_info.index('Time (UTC)')+1]
            try:
                float(eqs_info[eqs_info.index('Time (UTC)')+2].replace(' ± ',''))
                eqs_time_un=eqs_info[eqs_info.index('Time (UTC)')+2].replace(' ± ','')
            except:
                eqs_time_un='-'
            eqs_lat=eqs_info[eqs_info.index('Latitude')+1]
            try:
                float(eqs_info[eqs_info.index('Latitude')+2].replace(' ± ',''))
                eqs_lat_un=eqs_info[eqs_info.index('Latitude')+2].replace(' ± ','')
            except:
                eqs_lat_un='-'
            eqs_lon=eqs_info[eqs_info.index('Longitude')+1]
            try:
                float(eqs_info[eqs_info.index('Longitude')+2].replace(' ± ',''))
                eqs_lon_un=eqs_info[eqs_info.index('Longitude')+2].replace(' ± ','')
            except:
                eqs_lon_un='-'
            eqs_dep=eqs_info[eqs_info.index('Depth (km)')+1]
            try:
                float(eqs_info[eqs_info.index('Depth (km)')+2].replace(' ± ',''))
                eqs_dep_un=eqs_info[eqs_info.index('Depth (km)')+2].replace(' ± ','')
            except:
                eqs_dep_un='-'
            try:
                int(eqs_info[eqs_info.index('Origin ID')+1])
                eqs_id_loc=eqs_info[eqs_info.index('Origin ID')+1]
            except:
                eqs_id_loc='-'
            try:
                float(eqs_info[eqs_info.index('Largest azimuthal gap in station distribution as seen from epicenter (degree)')+1])
                eqs_gap=eqs_info[eqs_info.index('Largest azimuthal gap in station distribution as seen from epicenter (degree)')+1]
            except:
                eqs_gap='-'
            try:
                int(eqs_info[eqs_info.index('Number of defining phases')+1])
                eqs_ph=eqs_info[eqs_info.index('Number of defining phases')+1]
            except:
                eqs_ph='-'
            try:
                float(eqs_info[eqs_info.index('RMS of the travel time residuals of the arrivals used for the origin computation (sec)')+1])
                eqs_rms=eqs_info[eqs_info.index('RMS of the travel time residuals of the arrivals used for the origin computation (sec)')+1]
            except:
                eqs_rms='-' 
            try:
                int(eqs_info[eqs_info.index('Number of stations at which the event was observed')+1])
                eqs_st=eqs_info[eqs_info.index('Number of stations at which the event was observed')+1]
            except:
                eqs_st=eqs_info[49] 
            mag_info=mag_info.split('\n')
            mag_type=mag_info[mag_info.index('Type of magnitude')+1]
            mag_val=mag_info[mag_info.index('Value')+2]
            try:
                float(mag_info[mag_info.index('Uncertainty')+1])
                mag_unc=mag_info[mag_info.index('Uncertainty')+1]
            except:
                mag_unc='-'
        nl=[ev_id,eqs_time,eqs_time_un,eqs_lat,eqs_lat_un,eqs_lon,eqs_lon_un,eqs_dep,eqs_dep_un,mag_type,mag_val,mag_unc,eqs_gap,eqs_ph,eqs_rms,eqs_st,eqs_id_loc]
        nl='\t'.join(nl)
        earthquake_list.append(nl+'\n')
        eqs_time_s=eqs_time.split(' ')
        try:
            eqs_time_s.remove('')
            data_=eqs_time_s[0]
            ora_=eqs_time_s[1]
        except:
            data_=eqs_time_s[0]
            ora_=eqs_time_s[1]
        data_=data_.split('-')
        ora_=ora_.split(':')
        gmt_line=[data_[0],data_[1],data_[2],ora_[0],ora_[1],ora_[2],eqs_lat,eqs_lon,eqs_dep,mag_val]
        gmt_line='\t'.join(gmt_line)
        gmt_line=gmt_line.replace(' ','')
        if float(eqs_lat)>It_lat[1] or float(eqs_lat)<It_lat[0] or float(eqs_lon)>It_lon[1] or float(eqs_lon)<It_lon[0]:
            ev_gmt_w.append(gmt_line+'\n')
        else:
            ev_gmt.append(gmt_line+'\n')
    earthquake_list_end_yesterday=earthquake_list[:]
    earthquake_list_today=earthquake_list[:]
    for i in range(1,len(earthquake_list)):
        eqs_time=earthquake_list[i].split('\t')[1]
        eqs_time_s=eqs_time.split(' ')
        try:
            eqs_time_s.remove('')
            data_=eqs_time_s[0]
            ora_=eqs_time_s[1]
        except:
            data_=eqs_time_s[0]
            ora_=eqs_time_s[1]
        dt2=datetime.strptime(data_,"%Y-%m-%d")
        if dt2!=dt:
            earthquake_list_today.remove(earthquake_list[i])
        else:
            earthquake_list_end_yesterday.remove(earthquake_list[i])
    st3=dt-timedelta(days=7)
    st3=st3.strftime("%Y-%m-%d")
    st2=dt-timedelta(days=1)
    st2=st2.strftime("%Y-%m-%d")
    new_name_eqs_list='Earthquakes_list_with_complete_header_from'+str(st3)+'_to'+str(st2)+'.txt'
    with open(path_e+'Earthquakes_list_with_complete_header.txt','w') as o:
        for e in earthquake_list_today:
            o.write(e)
    with open(path_e+new_name_eqs_list,'w') as o:
        for e in earthquake_list_end_yesterday:
            o.write(e)    
    with open(path_p+'Eqs_gmt.txt','w') as o:
        for e in ev_gmt:
            o.write(e)
    with open(path_p+'Eqs_gmt_world.txt','w') as o:
        for e in ev_gmt_w:
            o.write(e)
    eqs_id_list=earthquake_list[-51:]
    with open(pt+'last_30_id','w') as o:
        for e in eqs_id_list:
            ee=e.split('\t')[0]+'\n'
            o.write(ee)
    
def browse_folders():
    global filename
    filename = filedialog.askdirectory(initialdir="/home/", title='Please select a directory')
    qk_e.delete(0,)
    qk_e.insert(0,str(filename))
    
def get_variables():
    global path,wd2
    path=qk_e.get()+'/'
    path=path+'SATA_tool_files/'
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    path_e=path+'Earthquakes/'
    path_p=path+'Plots/'
    os.mkdir(path_e)
    os.mkdir(path_p)
    pt=os.getcwd()+'/'
    if os.path.exists(pt+'temp'):
        shutil.rmtree(pt+'temp')
    os.mkdir(pt+'temp')
    pt=pt+'temp/'
    with open(pt+'path','w') as o:
        o.write(path)
    timing=selected.get()
    with open(pt+'timing','w') as o:
        o.write(str(timing))
    with open(pt+'running','w') as o:
        o.write(str(1))
    wd.destroy()

    start_data=time.strftime("%Y-%m-%d")
    with open(pt+'start_data','w') as o:
        o.write(start_data)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    with open(pt+'last_upgrade','w') as o:
        o.write(start_data+' '+current_time)
    First_download()

## Create main window
wd=tk.Tk()
wd.title("SATA")
wd.geometry("670x350")
wd.resizable(width=False, height=False)
wd.configure(background= "#E5E5E5")
# add description and instructions
txt='''This is the starting window for SATA (Seismicity Automatic Tool Analysis).
The tool reads earthquake database from the INGV official site and plots event of the last 7 days
starting from the moment you run it. Until the user does not stop it, the tool make a continous 
monitoring of the earthquake database and updates the seismicity plot displaying a maximum of 
300 events. Last earthquake appears as a star in the map.

SATA automatically creates a folder where store the earthquake list and the plot files. 
The user can set the length (in terms of time) of each list by choosing between daily, weekly 
or monthly. The tool considers a month as 30 consecutive days. After starting it needs few 
minutes to create the first list and plot it. Then a notify will appear each 5 minutes
to comunicate the refresh of the database.
'''
hp = tk.Label(wd, text = str(txt), justify='center',background="#E5E5E5")
hp.pack()
hp.configure(font=("arial", 11))
txt2='''In the panel below select the path where the list will be created and
the time length of earhquakes list. Remember that SATA considers the time starting from 
midnight of today (not from the begin of the current week or of the current month).
'''
hp2 = tk.Label(wd, text = str(txt2), justify='center',background="#E5E5E5")
hp2.pack()
hp2.configure(font=("arial", 10))
# ask for path
qk=tk.Label(wd,text="Storage path: ",background="#E5E5E5")
qk.place(x=10, y=280)
qk_e=tk.Entry()
qk_e.place(x=110, y=280, width=200)
browse = tk.Button(text="Browse",command = browse_folders)
browse.place(x=320, y=280)
# ask for storage time split
tm_spl=tk.Label(wd,text="Length of earthquakes lists: ",background="#E5E5E5")
tm_spl.place(x=410, y=280)
selected=tk.IntVar()
rad1=tk.Radiobutton(wd,text='Daily',value=1,variable=selected,background="#E5E5E5")
rad2=tk.Radiobutton(wd,text='Weekly',value=7,variable=selected,background="#E5E5E5")
rad3=tk.Radiobutton(wd,text='Monthly',value=30,variable=selected,background="#E5E5E5")
rad1.place(x=590, y=260)
rad2.place(x=590, y=280)
rad3.place(x=590, y=300)
# start button
start = tk.Button(text="Start tool",height= 1, width=30, command = get_variables)
start.place(x=240, y=320)
wd.mainloop()