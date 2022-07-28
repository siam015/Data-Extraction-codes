import datetime

from netCDF4 import Dataset

import pandas as pd




def date_to_string(srl_no):
    new_date = datetime.datetime(2010,1,1,0,0) + datetime.timedelta(srl_no)
    return new_date.strftime("%Y-%m-%d")

data = Dataset('F:/ACADEMIC/WRE 4-1/Thesis/Soil_Moisture/Data/Regression dataset/POWER_SinglePoint_Daily_20100101_20160831_023d43N_091d20E_8564cb19.nc','r')


lat = data.variables['lat'][:]
lon = data.variables['lon'][:]

Precip_merra = data.variables['PRECTOT'][:]


Time =  data.variables['time'][:]

All_Time = []

for tm in Time:
    time_data = date_to_string(int(tm))
    
    All_Time.append(time_data)
    
    
Start_time =  min(All_Time)
End_Time   =  max(All_Time)  

date_range = pd.date_range(start = Start_time,end=End_Time,freq='D')

df_rainfall = pd.DataFrame(0.0, columns = ['Year','Month','Day','Rainfall'],index = date_range)



for tm in date_range:
    
    df_rainfall.loc[tm]['Year'] = tm.year
    df_rainfall.loc[tm]['Month'] = tm.month
    df_rainfall.loc[tm]['Day'] = tm.day
    
    time_index = date_range.get_loc(tm)
    
    df_rainfall.loc[tm]['Rainfall']= Precip_merra[time_index,0,0]

    print('extracting data')
    
print('All Done')

df_rainfall.to_csv('GRACE_DAILY_rainfall_regression_cumilla.csv')