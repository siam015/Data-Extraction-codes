

import datetime

from netCDF4 import Dataset

import pandas as pd


data = Dataset('F:/Era5/cumilla15_16tp.nc','r')

time = data.variables['time'][:]

precip = data.variables['tp'][:]


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


df_precip = pd.DataFrame(0.0, columns = ['Year','Month','Day','Precip','Precip_mm'],index = date_range)


for hr in date_range:
    
    df_precip.loc[hr]['Year'] = hr.year
    df_precip.loc[hr]['Month'] = hr.month
    df_precip.loc[hr]['Day'] = hr.day
   
    
    time_index = date_range.get_loc(hr)
    
    df_precip.loc[hr]['Precip']= precip[time_index,0,0]
    
    print('extracting')
    
print('All Done')


df_precip['Precip_mm'] = df_precip['Precip']*1000


df_precip.to_csv('cumilla_daily_precip_15-16.csv')
