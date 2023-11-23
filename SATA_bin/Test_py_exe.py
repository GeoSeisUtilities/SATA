# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 15:42:51 2023

@author: GeoSeisUtilities
"""

with open('py_temp') as o:
    path = o.readline()
with open('py','w') as o:
    o.write(path)