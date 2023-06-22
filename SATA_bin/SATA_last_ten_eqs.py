#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 19:53:32 2023

@author: GeoSeisUtilities
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
# Extract last 10 events
new_table=list()
nl=ev_gmt[0][0:-1].split('\t')[0:-1]
nl='\t'.join(nl)
new_table.append(nl)
for l in ev_gmt[-10:]:
    l=l[0:-1].split('\t')[0:-1]
    l='\t'.join(l)
    new_table.append(l)
new_table='\n'.join(new_table)
new_table=new_table.replace('\t', ' ')
new_table=new_table.split('\n')
reform_table=list()
# Create figure
ll=new_table[0].split(' ')
line='{:<2}-{:<2}-{:<2}  {:<2}:{:<2}:{:<2}{:^5} {:^5}  {:^5}{:>4} - {:>3}'
line=line.format(ll[2],ll[1],ll[0][0:2],ll[3],ll[4],ll[5],'-',ll[6][:5],ll[7][:5],ll[8],ll[9])
line='1.4\t11\t'+line
reform_table.append(line)
y=10
for l in new_table[1:]:
    ll=l.split(' ')
    line='{:<2}-{:<2}-{:<2}   {:<2}:{:<2}:{:<2}{:^7}{:>5} {:>5} {:>3}  -  {:>3}'
    line=line.format(ll[2],ll[1],ll[0][-2:],ll[3],ll[4],ll[5],'-',ll[6][:5],ll[7][:5],ll[8],ll[9])
    line=f'1\t{y}\t'+line
    reform_table.append(line)
    y-=1
with open(pt+'table_ten_eqs','w') as o:
    for l in reform_table:
        o.write(l+'\n')
