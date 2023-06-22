# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 23:41:57 2023

@author: GeoSeisUtilities
"""

## Convert elevation from meters to km for the topographic plot
with open('track') as o:
    ll=o.readlines()
new_ll=list()
for l in ll:
    km=str(float(l.split('\t')[-1])/1000)
    new_ll.append(l[0:-1]+'\t'+km+'\n')
with open('output3','w') as o:
    for l in new_ll:
        o.write(l)
