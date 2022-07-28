
import datetime

from netCDF4 import Dataset

import pandas as pd


data = Dataset('F:/ACADEMIC/WRE 4-1/Thesis/Soil_Moisture/Data/ERA5/era5_daily.nc','r')

time = data.variables['time'][:]

precip = data.variables['tp']

swvl = data.variables['swvl1']

#Defining lat,lon variables
        
Lat_data = data.variables["latitude"][:]
Lon_data = data.variables["longitude"][:]


def date_to_string(srl_no):
    new_date = datetime.datetime(1900,1,1,0,0) + datetime.timedelta(hours=srl_no)
    return new_date.strftime("%Y/%m/%d")

All_Time = []

for tm in time:
    time_data = date_to_string(int(tm))
    
    All_Time.append(time_data)

Start_time =  min(All_Time)
End_Time   =  max(All_Time) 

date_range = pd.date_range(start = Start_time,end=End_Time,freq='D')


df_precip = pd.DataFrame(0.0, columns = ['Year','Month','Day','Precip','swvl1'],index = date_range)


station = pd.read_csv('Agromet.csv', sep=r'\s*,\s*', header=0, encoding='ascii', engine='python' )

for index, row in station.iterrows():
    
    stname = row['StName']
    
    stlat = row['Latitude']
    
    stlon = row['Longitude']
    
    
    for hr in date_range:
    
        df_precip.loc[hr]['Year'] = hr.year
        df_precip.loc[hr]['Month'] = hr.month
        df_precip.loc[hr]['Day'] = hr.day
       

    
        #Indexing station co-ordinate
        
        idx_lat_st= abs(Lat_data-stlat).argmin()
        idx_lon_st = abs(Lon_data-stlon).argmin()
        
        
        time_index = date_range.get_loc(hr)
        
        df_precip.loc[hr]['Precip']= precip[time_index,idx_lat_st,idx_lon_st]
        
        df_precip.loc[hr]['swvl1']= swvl[time_index,idx_lat_st,idx_lon_st]
        
        
        print('extractimg for station' +' ' + stname)
        
    df_precip['TP_mm'] = df_precip['Precip']*1000
        
    df_precip['SWVL_perc'] = df_precip['swvl1']*100
        
        
    df_precip.to_csv(stname +'_' +'ERA5_Total_Precipitation.csv')
    
print('All Done')
        



