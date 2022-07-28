import glob
from netCDF4 import Dataset
import datetime
import numpy as np
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

df = pd.DataFrame(0.0, columns = ['Year','Month','Day','Surface_SM','Rootzone_SM','GWS','TWS','Evaporation','Short_Wave'],index = date_range)


#target coordinate of the station

station = pd.read_csv('Agromet.csv', sep=r'\s*,\s*', header=0, encoding='ascii', engine='python' )

for index, row in station.iterrows():
    
    stname = row['StName']
    
    stlat = row['Latitude']
    
    stlon = row['Longitude']
    
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
        
        idx_lat_st= abs(Lat_data-stlat).argmin()
        idx_lon_st = abs(Lon_data-stlon).argmin()
        
         #different predictors    
        
        sm_rootzone    = data.variables['SoilMoist_RZ_tavg']
        sm_surface     = data.variables['SoilMoist_S_tavg']
        gws = data.variables['GWS_tavg']
        tws = data.variables['TWS_tavg']
        evap = data.variables['Evap_tavg']
        shortwave = data.variables['Swnet_tavg']
        
        
        
        
        df.loc[tm]['Rootzone_SM'] = sm_rootzone[0,idx_lat_st,idx_lon_st]
        
        df.loc[tm]['Surface_SM'] = sm_surface[0,idx_lat_st,idx_lon_st]
        
        df.loc[tm]['GWS'] = gws[0,idx_lat_st,idx_lon_st]
        
        df.loc[tm]['TWS'] = tws[0,idx_lat_st,idx_lon_st]
        
        df.loc[tm]['Evaporation'] = evap[0,idx_lat_st,idx_lon_st]
        
        df.loc[tm]['Short_Wave'] = shortwave[0,idx_lat_st,idx_lon_st]
        
        print('extractimg for station' +' ' + stname)
        
    df.to_csv(stname +'_' +'gldas_variable_outputs.csv')
        
        

print('All Done')
    

   
