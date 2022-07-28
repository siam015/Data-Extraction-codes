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

df = pd.DataFrame(0.0, columns = ['Station','latitude','longitude','Surface_SM(m3m-3)','Surface_Wetness','soil_temp_layer1(K)','soil_water_infiltration_flux(kgm-2s-1)','specific_humidity_lowatmmodlay(kgkg-1)','surface_temp(K)','ground_hflux(wm-2)','latent_hflux(wm-2)','sensible_hflux(wm-2)','land_evapotranspiration_flux','leaf_area_index(m2m-2)','net_downward_longwave_flux(wm-2)','net_downward_shortwave_flux(wm-2)','overland_runoff_flux(kgm-2s-1)','radiation_longwave_absorbed_flux','radiation_shortwave_downward_flux','vegetation_greenness_fraction','windspeed_lowatmmodlay','temp_lowatmmodlay(K)'],index = date_range)


#target coordinate of the station

station = pd.read_csv('Agromet.csv')

for index, row in station.iterrows():
    
    stname = row['station']
    
    stlat = row['latitude']
    
    stlon = row['longitude']
    



    for tm in Date_range_list:
        data = Dataset('SMAP_L4_SM_gph_'+  str(tm) + '_Vv6032_001_HEGOUT.nc','r' )
       
        #Defining lat,lon variables
        
        Lat_data = data.variables["y"][:]
        Lon_data = data.variables["x"][:]

        idx_lat_st = abs(Lat_data-stlat).argmin()
        idx_lon_st = abs(Lon_data-stlon).argmin()

       
       
        #different predictors    
        
        sm_surface      = data["/Geophysical_Data/sm_surface"]
        sm_surface_wetness = data["/Geophysical_Data/sm_surface_wetness"]
        soil_temp_layer1 = data["/Geophysical_Data/soil_temp_layer1"]
        soil_water_infiltration_flux = data["/Geophysical_Data/soil_water_infiltration_flux"]
        specific_humidity_lowatmmodlay = data["/Geophysical_Data/specific_humidity_lowatmmodlay"]
        surface_temp = data["/Geophysical_Data/surface_temp"]
        ground_hflux    = data["/Geophysical_Data/heat_flux_ground"]
        latent_hflux    = data["/Geophysical_Data/heat_flux_latent"] 
        sensible_hflux  = data["/Geophysical_Data/heat_flux_sensible"]
        land_evapotranspiration_flux   = data["/Geophysical_Data/land_evapotranspiration_flux"]
        leaf_area_index = data["/Geophysical_Data/leaf_area_index"]
        net_downward_longwave_flux = data["/Geophysical_Data/net_downward_longwave_flux"]
        net_downward_shortwave_flux = data["/Geophysical_Data/net_downward_shortwave_flux"]
        overland_runoff_flux = data["/Geophysical_Data/overland_runoff_flux"]
        radiation_longwave_absorbed_flux = data["/Geophysical_Data/radiation_longwave_absorbed_flux"]
        radiation_shortwave_downward_flux = data["/Geophysical_Data/radiation_shortwave_downward_flux"]
        vegetation_greenness_fraction = data["/Geophysical_Data/vegetation_greenness_fraction"]
        windspeed_lowatmmodlay = data["/Geophysical_Data/windspeed_lowatmmodlay"]
        temp_lowatmmodlay = data["/Geophysical_Data/temp_lowatmmodlay"]




        
        
        #creating iteration date range
        
        looptime = datetime.strptime(tm,'%Y%m%dT%H%M%S')
        

        
        df.loc[looptime]['Surface_SM(m3m-3)'] = sm_surface[idx_lat_st,idx_lon_st]
        
        df.loc[looptime]['Surface_Wetness'] = sm_surface_wetness[idx_lat_st,idx_lon_st]

        df.loc[looptime]['soil_temp_layer1(K)'] = soil_temp_layer1[idx_lat_st,idx_lon_st]
        
        df.loc[looptime]['soil_water_infiltration_flux(kgm-2s-1)'] = soil_water_infiltration_flux[idx_lat_st,idx_lon_st]
        
        df.loc[looptime]['specific_humidity_lowatmmodlay(kgkg-1)'] = specific_humidity_lowatmmodlay[idx_lat_st,idx_lon_st]

        df.loc[looptime]['surface_temp(K)'] = surface_temp[idx_lat_st,idx_lon_st]
        
        df.loc[looptime]['ground_hflux(wm-2)'] = ground_hflux[idx_lat_st,idx_lon_st]

        df.loc[looptime]['latent_hflux(wm-2)'] = latent_hflux[idx_lat_st,idx_lon_st]

        df.loc[looptime]['sensible_hflux(wm-2)'] = sensible_hflux[idx_lat_st,idx_lon_st]

        df.loc[looptime]['land_evapotranspiration_flux'] = land_evapotranspiration_flux[idx_lat_st,idx_lon_st]

        df.loc[looptime]['leaf_area_index(m2m-2)'] = leaf_area_index[idx_lat_st,idx_lon_st]

        df.loc[looptime]['net_downward_longwave_flux(wm-2)'] = net_downward_longwave_flux[idx_lat_st,idx_lon_st]

        df.loc[looptime]['net_downward_shortwave_flux(wm-2)'] = net_downward_shortwave_flux[idx_lat_st,idx_lon_st]

        df.loc[looptime]['net_downward_shortwave_flux(wm-2)'] = overland_runoff_flux[idx_lat_st,idx_lon_st]

        df.loc[looptime]['radiation_longwave_absorbed_flux'] = radiation_longwave_absorbed_flux[idx_lat_st,idx_lon_st]

        df.loc[looptime]['radiation_shortwave_downward_flux'] = radiation_shortwave_downward_flux[idx_lat_st,idx_lon_st]

        df.loc[looptime]['vegetation_greenness_fraction'] = vegetation_greenness_fraction[idx_lat_st,idx_lon_st]

        df.loc[looptime]['windspeed_lowatmmodlay'] = windspeed_lowatmmodlay[idx_lat_st,idx_lon_st]

        df.loc[looptime]['temp_lowatmmodlay(K)'] = temp_lowatmmodlay[idx_lat_st,idx_lon_st]


    df["Station"] = stname
    df["latitude"] = stlat
    df["longitude"] = stlon

    print("Done for " + stname)
    df.to_csv('SMAP_GPH_' + stname + '_Data.csv')
   