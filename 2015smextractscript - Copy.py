import glob
from netCDF4 import Dataset
import datetime
from datetime import datetime
import pandas as pd



All_Timestamp = []
Date_range_list = []

for file in glob.glob('*.nc'):
   
    data = Dataset(file,'r')
    #print(data)
    
    date_time = str(file[15:30])
    Date_range_list.append(date_time)
     
    Timestamp = datetime.strptime(date_time,'%Y%m%dT%H%M%S')
    All_Timestamp.append(Timestamp)
       

Start_time =  min(All_Timestamp)
End_Time   =  max(All_Timestamp)   

date_range = pd.date_range(start = Start_time,end=End_Time,freq='3h')

df = pd.DataFrame(0.0, columns = ['Year','Month','Day','Time','Surface_SM','Rootzone_SM'],index = date_range)

#target coordinate of the station

Lat_cumilla  = 23.43
Lon_cumilla = 91.20

for tm in Date_range_list:
    data = Dataset('SMAP_L4_SM_aup_'+  str(tm) + '_Vv5030_001_HEGOUT.nc','r' )
   
    #Defining lat,lon variables
    
    Lat_data = data.variables["y"][:]
    Lon_data = data.variables["x"][:]

    #Indexing station co-ordinate
    
    idx_lat_cumilla = abs(Lat_data-Lat_cumilla).argmin()
    idx_lon_cumilla = abs(Lon_data-Lon_cumilla).argmin()
   
    #different predictors    
    
    sm_rootzone    = data["/Analysis_Data/sm_rootzone_analysis"]
    sm_surface     = data["/Analysis_Data/sm_surface_analysis"] 
    sm_profile     = data["/Analysis_Data/sm_profile_analysis"]
    surface_temp   = data["/Analysis_Data/surface_temp_analysis"]
    
    
    #creating iteration date range
    
    looptime = datetime.strptime(tm,'%Y%m%dT%H%M%S')
    
    df.loc[looptime]['Year'] = looptime.year
    df.loc[looptime]['Month'] = looptime.month
    df.loc[looptime]['Day'] = looptime.day
    df.loc[looptime]["Time"]= looptime.hour
    
    df.loc[looptime]['Rootzone_SM'] = sm_rootzone[idx_lat_cumilla,idx_lon_cumilla]
    
    df.loc[looptime]['Surface_SM'] = sm_surface[idx_lat_cumilla,idx_lon_cumilla]
    
   
    print('Finished Extraction')
    

df_group = df.groupby(['Month','Day'])

   