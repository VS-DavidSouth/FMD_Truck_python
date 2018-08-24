###############INFO#################################################
#Date created: 4/4/17 Date last updated: 5/1/17
#Creator: David South
#Python version: 2.7
#Purpose: I have a several datasets that I want to be cut up into
#seperate files, one for each region
#this file is meant to be run in the ArcMap arcpy addon window but
#can function by running it in the Pythin IDE if the file names
#are changed to full file locations.
#To clip a type of file, simply delete the "##" before the line and
#run this program. 

###################SETUP############################################

import arcpy
from arcpy import env
env.overwriteOutput = True

######################ACTUAL CODE###################################

#Note: at this point, Feed_Req field needs to be added to FLAPS file
#and Speed_Lim + Time_Cost need to be added to roads layer


#do the code 4 times
for R in range (1,5):


    #clip roads layer based on Region
    #note: the roads layer should be a network dataset first, before it is clipped
    arcpy.Clip_analysis(in_features="allroads_miv14a", clip_features="Region_" + str(R), out_feature_class="F:/FMD_Project/Davids_work/Feed_Truck_Model/Roads/Roads_Region_"  + str(R) + ".shp", cluster_tolerance="")

    #clip FLAPS based on Region. FLAPS shapefile should be in a geodatabase
    ##arcpy.Clip_analysis(in_features="FLAPS_NGNS_10up_2_copies", clip_features="Region_" + str(R), out_feature_class="F:/FMD_Project/Davids_work/Feed_Truck_Model/FLAPS/FLAPS.gdb/FLAPS_NGNS_Region_" + str(R), cluster_tolerance="")

    #clip Feed_Lic based on Region
    ##arcpy.Clip_analysis(in_features="Feed_Lic_List", clip_features="Region_" + str(R), out_feature_class="F:/FMD_Project/Davids_work/Feed_Truck_Model/Feed Lic/Feed_Lic_Region_"  + str(R) + ".shp", cluster_tolerance="")

print "Completed."
