#adding routes v3.py
#Created by David South -- Date created: 3/31/2017 Last updated: 5/24/17
#Python version: 2.7
#Purpose: to create a Feature Class for each region with a specific number
#of blank rows with specific fields that will be used to make routes in the VRP
#(Vehicle Routing Problem) in the Network Analyst addon in ArcMap.
#Note: this can be run in the Python IDE or in the arcpy window.
#Double check all the filepaths before you run this program.

import arcpy, os
from arcpy import env

#set workplace environment
ws = r'F:\FMD_Project\Davids_work\Feed_Truck_Model\Python'
env.workspace = ws
env.overwriteOutput = True


#################parameters##################
#stastics from survey - Average number of trucks per region
#  Region #: 1,2,3,4
numTrucks = [5,5,3,6]

#maximum number of orders per depot
maxOrderCount = 9

#max capacity, in pounds per delivery truck
capacity = 50000

#template for routes // not being used in the program currently
routes_template = r'F:\FMD_Project\Davids_work\Feed_Truck_Model\Python\Templates\Routes_Template.shp'

#location of routes folder
routes_folder = r'F:\FMD_Project\Davids_work\Feed_Truck_Model\Routes'

#location of the Feed_Lic folder
Feed_Lic_folder = r'F:\FMD_Project\Davids_work\Feed_Truck_Model\Feed Lic'

#define fields to be created and filled for routes
fields1 = ['Name', 'StartDepot', 'EndDepot', 'EStartTime', 'LStartTime', \
          'Capacities', 'MaxOrder']

#define fields for route renewals
fields2 = ['DEPOTNAME', 'ROUTENAME']

#define days of the week
DotW = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri']

#define dates for each day of the week. Note there is one extra day
#to incorporate a 24 hour period for each day
date = ['1994-08-22', '1994-08-23', '1994-08-24', '1994-08-25', '1994-08-26',\
        '1994-08-27']

################actual code##################


for region in range (1,5):

  #location of Feed_Lic file
  Feed_Lic_name = 'Feed_Lic_Region_' + str(region) + '.shp'
  Feed_Lic = os.path.join(Feed_Lic_folder, Feed_Lic_name)

  #number of routes per Depot 
  route_num = numTrucks[region-1]
  
  #count how many Depots there are in the region
  Feed_Lic_C = arcpy.GetCount_management(in_rows= Feed_Lic)
  Feed_Lic_Count = int(Feed_Lic_C.getOutput(0))
  
  #name of new routes file
  newFile = "routes_Region_" + str(region) + '.shp'
  newFileFull = os.path.join(routes_folder, newFile)

  #name of new routes renewals file
  newFile2 = "route_renewals_" + str(region) + ".dbf"


  #create new table for route renewals (note: pay attention to lower
  #and upper case letters, the tool may make file titles in just lower-case)
  tbl = arcpy.CreateTable_management(routes_folder, newFile2)
  tv = arcpy.MakeTableView_management(tbl, "tv")

  #create a new routes file using the Create Feature Class tool
  arcpy.CreateFeatureclass_management(out_path= \
  routes_folder, out_name= newFile, geometry_type="POLYLINE", template= "", \
  has_m="DISABLED", has_z="DISABLED")

  #create new blank fields in the freshly created routes Feature Class
  for num1 in range(0, len(fields1)):
    arcpy.AddField_management(newFileFull, fields1[num1], "TEXT", "", "", 15)

  #create new blank fields for route renewals
  for num2 in range(0, len(fields2)):
    arcpy.AddField_management(tv, fields2[num2], "TEXT", "", "", 15)
    
  #create a cursor so you can later add a buncha new rows on the routes file. 
  cursor1 = arcpy.da.InsertCursor(newFileFull, fields1)
  #create a cursor for the route renewals
  cursor2 = arcpy.da.InsertCursor(tv, fields2)
  
  for q in range (0,Feed_Lic_Count):
    for p in range (0,route_num):
      for day in range (0, len(DotW)):
        #create all the rows for routes
        cursor1.insertRow(("Route_" + str(q + 1) + "_" + str(p + 1)\
        + str(DotW[day]), str(q), str(q), date[day], date[day + 1],\
        capacity, maxOrderCount))

        #create all the rows for route renewals
        cursor2.insertRow([str(q),"Route_" + str(q + 1)\
        + "_" + str(p + 1) + str(DotW[day])])
        
  #Get rid of cursor1. You don't need it anymore. Get outta here, cursor. 
  del cursor1
  #Hey cursor2, gtfo! You aren't welcome here no more!
  del cursor2

print "Completed."
