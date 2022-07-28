# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 20:15:51 2021

@author: Siam
"""

import glob
from netCDF4 import Dataset
import datetime

import pandas as pd

All_Date = []


def date_to_string(srl_no):
    new_date = datetime.datetime(2003,2,1,0,0) + datetime.timedelta(srl_no)
    return new_date.strftime("%Y-%m-%d")

for file in glob.glob('*.nc4'):
    data = Dataset(file,'r')
    
    time = data.variables['time'][:]
    
    date = date_to_string(int(time))
    
    All_Date.append(date)
    
Start_time =  min(All_Date)
End_Time   =  max(All_Date)  

date_range = pd.date_range(start = Start_time,end=End_Time,freq='D')

df = pd.DataFrame(0.0, columns = ['Year','Month','Day','Surface_SM','Rootzone_SM'],index = date_range)

#target coordinate of the station

Lat_cumilla  = 23.43
Lon_cumilla = 91.20



for tm in date_range:
    
    looptime = tm.strftime("%Y%m%d")
    data = Dataset('GLDAS_CLSM025_DA1_D.A'+str(looptime)+'.022.nc4.SUB.nc4','r')
    
    time = data.variables['time'][:]
    
    df.loc[tm]['Year'] = tm.year
    df.loc[tm]['Month'] = tm.month
    df.loc[tm]['Day'] = tm.day
    
     #Defining lat,lon variables
    
    Lat_data = data.variables["lat"][:]
    Lon_data = data.variables["lon"][:]

    #Indexing station co-ordinate
    
    idx_lat_cumilla = abs(Lat_data-Lat_cumilla).argmin()
    idx_lon_cumilla = abs(Lon_data-Lon_cumilla).argmin()
   
    #different predictors    
    
    sm_rootzone    = data.variables['SoilMoist_RZ_tavg']
    sm_surface     = data.variables['SoilMoist_S_tavg']
    
   
    df.loc[tm]['Rootzone_SM'] = sm_rootzone[0,idx_lat_cumilla,idx_lon_cumilla]
    
    df.loc[tm]['Surface_SM'] = sm_surface[0,idx_lat_cumilla,idx_lon_cumilla]
    
    print('finshed extraction')

print('All Done')

df.to_csv('GRACE(GLDAS)_2015_2016_Cumilla_Data.csv')   
    
    
    
    
    


