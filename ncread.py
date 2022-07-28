import netCDF4
from netCDF4 import Dataset

from datetime import datetime

# read the data

data = Dataset('','r')

#read variables

time = data.variables["time"]
Lat = data.variables["y"]
Lon = data.variables["x"]
sm_surface = data["/Analysis_Data/sm_rootzone_analysis"]

#create readable arrays

time_data = data.variables["time"][:]
Lat_data = data.variables["y"][:]
Lon_data = data.variables["x"][:]
sm_surface_data = data["/Analysis_Data/sm_rootzone_analysis"][:]

#target coordinate of the station

Lat_cumilla  = 23.43
Lon_cumilla = 91.20

#Indexing station co-ordinate

idx_lat_cumilla = abs(Lat_data-Lat_cumilla).argmin()
idx_lon_cumilla = abs(Lon_data-Lon_cumilla).argmin()

#Extraction of soil moisture data
sm_surface_cumilla = sm_surface_data[idx_lat_cumilla,idx_lon_cumilla]
print(sm_surface_cumilla,sm_surface.units)




















