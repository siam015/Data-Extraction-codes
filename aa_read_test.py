import netCDF4

from netCDF4 import Dataset

from datetime import datetime

# read the data

data = Dataset('F:/ACADEMIC/WRE 4-1/Thesis/Soil_Moisture/Data/GLDAS_2.2/GLDAS_CLSM025_DA1_D.A20150101.022.nc4.SUB.nc4','r')



Lat_data = data.variables["lat"][:]
Lon_data = data.variables["lon"][:]

#target coordinate of the station

Lat_cumilla  = 23.43
Lon_cumilla = 91.20

idx_lat_cumilla = abs(Lat_data-Lat_cumilla).argmin()
idx_lon_cumilla = abs(Lon_data-Lon_cumilla).argmin()




