import netCDF4

import datetime

from netCDF4 import Dataset

import pandas as pd


def date_to_string(srl_no):
    new_date = datetime.datetime(2000,1,1,0,0) + datetime.timedelta(srl_no)
    return new_date.strftime("%Y-%m-%d")



data = Dataset('F:/ACADEMIC/WRE 4-1/Thesis/Soil_Moisture/Data/SMAP_SM l4/2015-16/SPL4SMGP.005_9km_2015-2016.nc','r')


Lat_data = data.variables["lat"][:]
Lon_data = data.variables["lon"][:]

Time =  data.variables['time'][:]

smsurface = data.variables['Geophysical_Data_sm_surface']

smrt =  data.variables['Geophysical_Data_sm_rootzone']

All_Time = []

for tm in Time:
    time_data = date_to_string(int(tm))
    
    All_Time.append(time_data)
    
    
Start_time =  min(All_Time)
End_Time   =  max(All_Time)  

date_range = pd.date_range(start = Start_time,end=End_Time,freq='D')

df= pd.DataFrame(0.0, columns = ['Year','Month','Day','SM_Surface','SM_RTZone'],index = date_range)

Lat_cumilla  = 24.37
Lon_cumilla = 88.7

idx_lat_cumilla = abs(Lat_data-Lat_cumilla).argmin()
idx_lon_cumilla = abs(Lon_data-Lon_cumilla).argmin()


for tm in date_range:
    
    df.loc[tm]['Year'] = tm.year
    df.loc[tm]['Month'] = tm.month
    df.loc[tm]['Day'] = tm.day
    
    time_index = date_range.get_loc(tm)
    
    
    AllSM = []
    AllRT = []
    
    for i in [0,1,2,3,4,5,6,7]:
        
        Meansmsurface = smsurface[time_index,idx_lat_cumilla,idx_lon_cumilla,i]
        
        Meanrtzone = smrt[time_index,idx_lat_cumilla,idx_lon_cumilla,i]
        
        AllSM.append(Meansmsurface)
        
        AllRT.append(Meanrtzone)
        
    df.loc[tm]['SM_Surface'] = sum(AllSM)/len(AllSM)
    
    df.loc[tm]['SM_RTZone'] = sum(AllRT)/len(AllRT)
   
    print('working')
    
    
print('All Done')

df.to_csv('Rajshahi_15_16_daily.csv')

    
    