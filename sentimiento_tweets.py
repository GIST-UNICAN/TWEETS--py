# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 08:32:22 2018

@author: Andres
"""
import pandas as pd
import time
import pyproj

ed50= pyproj.Proj("+init=EPSG:23030")
wgs84= pyproj.Proj("+init=EPSG:4326")

df=pd.read_csv(r"D:\Users\Andres\Dropbox\TRABAJO\SETA\posiciones_bus_100\resultado_bus100.csv")
df['long'], df['lat']=pyproj.transform(ed50, wgs84, df['PosX'].tolist(), df['PosY'].tolist())
df.to_csv(r"D:\Users\Andres\Dropbox\TRABAJO\SETA\posiciones_bus_100\sensor_coordinates.csv", index=False)
#writer = pd.ExcelWriter('sensor_coordinates.xlsx')
#df.to_excel(writer,'coord')
#writer.save()