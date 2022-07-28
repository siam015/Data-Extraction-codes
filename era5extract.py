# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 11:45:35 2021

@author: Siam
"""

import datetime

from netCDF4 import Dataset

import pandas as pd


# read the data

data = Dataset('F:/ACADEMIC/WRE 4-1/Thesis/Soil_Moisture/Era5/era5cumilla.nc','r')

time = data.variables['time'][:]

precip = data.variables['tp'][:]

def date_to_string(srl_no):
    new_date = datetime.datetime(1900,1,1,0,0) + datetime.timedelta(hours=srl_no)
    return new_date.strftime("%Y/%m/%d  %H")

All_Time = []

for tm in time:
    time_data = date_to_string(int(tm))
    
    All_Time.append(time_data)

Start_time =  min(All_Time)
End_Time   =  max(All_Time)  

date_range = pd.date_range(start = Start_time,end=End_Time,freq='h')

df_precip = pd.DataFrame(0.0, columns = ['Year','Month','Day','Hour','Precip','Precip_mm'],index = date_range)


for hr in date_range:
    
    df_precip.loc[hr]['Year'] = hr.year
    df_precip.loc[hr]['Month'] = hr.month
    df_precip.loc[hr]['Day'] = hr.day
    df_precip.loc[hr]['Hour'] = hr.hour
    
    time_index = date_range.get_loc(hr)
    
    df_precip.loc[hr]['Precip']= precip[time_index,0,0]
    
    print('extracting')
    
print('All Done')

    
    
df_precip.to_csv('Precipitation_2015_2016.csv')
