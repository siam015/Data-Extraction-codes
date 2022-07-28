# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 01:16:49 2021

@author: Siam
"""



import datetime

from netCDF4 import Dataset

import pandas as pd




def date_to_string(srl_no):
    new_date = datetime.datetime(2014,1,1,0,0) + datetime.timedelta(srl_no)
    return new_date.strftime("%Y-%m-%d")


# read the data

data = Dataset('F:/ACADEMIC/WRE 4-1/Thesis/Soil_Moisture/Data/Grace_DAILY_Data/ITSG-Grace2018_daily_2014.nc','r')

Lat_data = data.variables["lat"][:]
Lon_data = data.variables["lon"][:]

Time =  data.variables['time'][:]

TWSA = data.variables['TWSA']

All_Time = []

for tm in Time:
    time_data = date_to_string(int(tm))
    
    All_Time.append(time_data)
    
    
Start_time =  min(All_Time)
End_Time   =  max(All_Time)  

date_range = pd.date_range(start = Start_time,end=End_Time,freq='D')

df_TWSA = pd.DataFrame(0.0, columns = ['Year','Month','Day','TWSA'],index = date_range)


#target coordinate of the station

Lat_cumilla  = 23.43
Lon_cumilla = 91.20

idx_lat_cumilla = abs(Lat_data-Lat_cumilla).argmin()
idx_lon_cumilla = abs(Lon_data-Lon_cumilla).argmin()


for tm in date_range:
    
    df_TWSA.loc[tm]['Year'] = tm.year
    df_TWSA.loc[tm]['Month'] = tm.month
    df_TWSA.loc[tm]['Day'] = tm.day
    
    time_index = date_range.get_loc(tm)
    
    df_TWSA.loc[tm]['TWSA']= TWSA[time_index,idx_lat_cumilla,idx_lon_cumilla]

    print('extracting data')
    
print('All Done')

df_TWSA.to_csv('GRACE_DAILY_TWSA_2014.csv')



