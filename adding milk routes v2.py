#adding milk routes v2.py
#Created by David South -- Last updated: 6/1/17
#Adapted from "adding routes v3" for the Feed Truck Model
#Purpose: to create a Feature Class for each region with a specific number
#of blank rows with specific fields that will be used to make routes in the VRP
#(Vehicle Routing Problem) in the Network Analyst addon in ArcMap.
#Note: this can be run in the Python IDE or in the arcpy window.

######################SETUP###################
import arcpy, os
from arcpy import env

#set workplace environment
ws = r'F:\FMD_Project\Davids_work\Milk_Truck_Model\Python'
env.workspace = ws
env.overwriteOutput = True

######################PARAMETERS##############

#max capacity, in gallons per delivery truck
capacities = 6500

#location of routes folder
routes_folder = r'F:\FMD_Project\Davids_work\Milk_Truck_Model\Routes'

#location of the creameries folder
creameries_folder = r'F:\FMD_Project\Davids_work\Milk_Truck_Model\Creameries'

#location of the creameries file
creameries = r'F:\FMD_Project\Davids_work\Milk_Truck_Model\Creameries\creameries_v4_3.shp'

#define fields to search in the creameries file
fields1 = ['FID', 'Trucks_per']

#define fields for the routes file (EStartTime and LStartTime fields are for
#determining which day the route will run, Earliest and Latest start time)
fields2 = ['Name', 'StartDepot', 'EndDepot','EStartTime', 'LStartTime', \
           'Capacities']
    #these fields were not used but can be added in:
    #'MaxOrder'

#name of the new file
newFile = 'MTM_routes.shp'     #MTM means Milk Truck Model
newFileFull = os.path.join(routes_folder, newFile)

#define days of the week that the routes can run on. Note there is one extra
#day, this is to incorporate a 24 hour period for each day. 
date = ['1994-08-22', '1994-08-23', '1994-08-24']

#define days of the week
DotW = ['Mon', 'Tues']

####################ACTUAL CODE#################

#count how many Depots there are in the region
creameries_C = arcpy.GetCount_management(in_rows= creameries)
creameries_Count = int(creameries_C.getOutput(0))

#define blank lists
trucks_per_creamery = []

#make a search cursor to save the info from the creameries and save it to a list
with arcpy.da.SearchCursor(creameries, fields1) as cursor1:
    for row_1 in cursor1:
        trucks_per_creamery += [row_1[1]]

#create a new completely blank shapefile for the routes
arcpy.CreateFeatureclass_management(out_path= \
routes_folder, out_name= newFile, geometry_type="POLYLINE", template= "", \
has_m="DISABLED", has_z="DISABLED")

#add new fields
for num1 in range(0, len(fields2)):
    arcpy.AddField_management(newFileFull, fields2[num1], "TEXT", "", "", 15)

#define a cursor
cursor2 = arcpy.da.InsertCursor(newFileFull, fields2)

##add in a buncha blank rows for the routes##
#make two copies of the routes, one for each 24 hour period
for s in range (0, len(date)-1):
    #do this for each for each creamery
    for q in range (0, creameries_Count):
        #do this for for each route
        for p in range (0, trucks_per_creamery[q]):
            #fill the fields from fields2 with the following info
            cursor2.insertRow(['Route_' + str(q)+ '_' + str(p) + DotW[s], \
            str(q), str(q), date[s], date[s+1], str(capacities)])

#get outta here cursor. You ain't gotta go home, but you can't stay here.
del cursor2
           
print "Completed."
