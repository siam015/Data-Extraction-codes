

import os
import shutil

os.getcwd()

RootDir1 = r'F:\ACADEMIC\WRE 4-1\Thesis\Soil_Moisture\Data\SMAP_SM l4\Bangladesh_2015\2016(part2)'
TargetFolder = r'F:\ACADEMIC\WRE 4-1\Thesis\Soil_Moisture\Data\SMAP_SM l4\Bangladesh_2015\2015_nc_files'
for root, dirs, files in os.walk((os.path.normpath(RootDir1)), topdown=False):
        for name in files:
            if name.endswith('.nc'):
                print ("Found")
                SourceFolder = os.path.join(root,name)
                shutil.copy2(SourceFolder, TargetFolder) #copies csv to new folder