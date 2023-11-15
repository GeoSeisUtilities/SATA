# -*- coding: utf-8 -*-
"""
Created on Tue May 16 19:45:25 2023

@author: GeoSeisUtilities
"""

## Import modules
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import os

## Refresh INGV page and upgrade of eartquake list
It_lat=[35,49]
It_lon=[5,20]
pt=os.getcwd()+'/temp/'
with open(pt+'path') as o:
    path=o.readline()
path_e=path+'Earthquakes/'
path_p=path+'Plots/'
with open(pt+'timing') as o:
    timing=int(o.readline())
with open(pt+'last_30_id') as o:
    ids_l=o.readlines()
with open(pt+'running') as o:
    running=int(o.readline())
with open(pt+'start_data') as o:
    start_data=o.readline()
with open(path_e+'Earthquakes_list_with_complete_header.txt') as o:
    earthquake_list=o.readlines()
with open(path_p+'Eqs_gmt.txt') as o:
    ev_gmt=o.readlines()
with open(path_p+'Eqs_gmt_world.txt') as o:
    ev_gmt_w=o.readlines()
act_tm=time.strftime("%Y-%m-%d")
dt = datetime.strptime(act_tm, "%Y-%m-%d")
dt2 = datetime.strptime(start_data, "%Y-%m-%d")
days=int((dt-dt2).days)
if days==timing:
    earthquake_list=list()
    header=['Id','Time_or','Time_err','Lat','Lat_err','Lon','Lon_err','Depth','Dep_err','Mag_type','Mag','Mag_err','Az_gap','Phases','RMS','Act_st','ID_loc']
    header='\t'.join(header)
    earthquake_list.append(header+'\n')
    dt=dt-timedelta(days=1)
    dt=dt.strftime("%Y-%m-%d")
    dt2=dt2.strftime("%Y-%m-%d")
    dt3=datetime.strptime(act_tm, "%Y-%m-%d")
    dt3=dt3.strftime("%Y-%m-%d")
    new_name_eqs_list='Earthquakes_list_with_complete_header_from'+str(dt2)+'_to'+str(dt3)+'.txt'
    os.rename(path_e+'Earthquakes_list_with_complete_header.txt',path_e+new_name_eqs_list)
    start_data=time.strftime("%Y-%m-%d")
    with open(pt+'start_data','w') as o:
        o.write(start_data)
    with open(path_e+'Earthquakes_list_with_complete_header.txt','w') as o:
        for e in earthquake_list:
            o.write(e)
test_val=0
act_tm=time.strftime("%Y-%m-%d")
dt = datetime.strptime(act_tm, "%Y-%m-%d")
st = dt - timedelta(days=7)
st=st.strftime("%Y-%m-%d")
url = 'http://terremoti.ingv.it/events?starttime=2023-05-09+00%3A00%3A00&endtime=2023-05-16+23%3A59%3A59&last_nd=7&minmag=-1&maxmag=10&mindepth=-10&maxdepth=1000&minlat=35&maxlat=49&minlon=5&maxlon=20&minversion=100&limit=30&orderby=ot-desc&lat=0&lon=0&maxradiuskm=-1&wheretype=area&box_search=Italia'
st_time=url[42:52]
end_time=url[74:84]
url=url.replace(st_time,st)
url=url.replace(end_time,act_tm)
response = requests.get(url)
html = BeautifulSoup(response.text, 'html.parser')
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
# Clear spurius links
url1=url_e[:]
url_e=list()
for u in url1:
    try:
        v_temp=u.split('/')[-1]
        v_temp=int(v_temp)
        url_e.append(u)
    except:
        continue
url_e.reverse()
for u in url_e:
    ev_id=u.split('/')[-1]
    # check if there is something new
    if ev_id+'\n' not in ids_l:
        test_val=1
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
        ids_l.append(ev_id+'\n')
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
        eqs_dep_neg='-'+eqs_dep
        gmt_line=[data_[0],data_[1],data_[2],ora_[0],ora_[1],ora_[2],eqs_lat,eqs_lon,eqs_dep,mag_val,eqs_dep_neg]
        gmt_line='\t'.join(gmt_line)
        gmt_line=gmt_line.replace(' ','')
        if float(eqs_lat)>It_lat[1] or float(eqs_lat)<It_lat[0] or float(eqs_lon)>It_lon[1] or float(eqs_lon)<It_lon[0]:
            ev_gmt_w.append(gmt_line+'\n')
        else:
            ev_gmt.append(gmt_line+'\n')
eqs_id_list=ids_l[-51:]
with open(pt+'last_30_id','w') as o:
    for e in eqs_id_list:
        o.write(e)       
# second check and write new lists
if test_val==1:
    with open(path_e+'Earthquakes_list_with_complete_header.txt','w') as o:
        for e in earthquake_list:
            o.write(e)
    if len(ev_gmt)<700:
        with open(path_p+'Eqs_gmt.txt','w') as o:
            for e in ev_gmt:
                o.write(e)
    else:
        while len(ev_gmt)>700:
            ev_gmt.remove(ev_gmt[1])
        with open(path_p+'Eqs_gmt.txt','w') as o:
            for e in ev_gmt:
                o.write(e)
    if len(ev_gmt_w)<700:
        with open(path_p+'Eqs_gmt_world.txt','w') as o:
            for e in ev_gmt_w:
                o.write(e)
    else:
        while len(ev_gmt_w)>700:
            ev_gmt_w.remove(ev_gmt_w[1])
        with open(path_p+'Eqs_gmt_world.txt','w') as o:
            for e in ev_gmt_w:
                o.write(e)
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
with open(pt+'last_upgrade','w') as o:
    o.write(start_data+' '+current_time)
