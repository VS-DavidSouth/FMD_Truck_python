#Extracting Statstics from the Milk Truck Model
#Created by David South -- Date created: 6/4/17 -- Date updated: 6/23/17
#Python version: 2.7
#This program can be run in the IDLE or the ArcPy window of ArcMap
#Purpose: To derive the following statstics from the Milk Truck Model 
# Stats -
#1.Average Distance of a route per livestock category
#2.Average number of stops per route per livestock category
#3.Frequency of movement per livestock category (meaning the average
#number of deliveries to farms from that category per week).

#This work was funded through a USDA-APHIS cooperative agreement.

#####################SETUP###########################
import arcpy, os, numpy, csv
from arcpy import env

ws = r'F:\FMD_Project\Davids_work\Milk_Truck_Model\Deriving_Statistics'
env.workspace = ws
env.overwriteOutput = True

#set it up to write to MTM_Results.csv
open(os.path.join(ws,'MTM_Results.csv'), 'wb')
g = open(os.path.join(ws,'MTM_Results.csv'), 'ab')
writer = csv.writer(g, dialect = 'excel')

#print intro
intro = "Milk Truck Model - Statistics for InterSpread Plus\n" + \
        "Project done by David South with the help of Dr. Hadrich, Dr. Hagerman,\n" +\
        "Dr Magzamen and Dr. Wolf\n\nThe numbers '// A / B' are the Standard Deviation(A)" +\
        "and the Range(B)\n" +\
        "\n-\n-\n-"
print(intro)

####################PARAMETERS#######################
#does the model incorporate 2 days, or just one day?
numDays = 2

#define FLAPS categories
categories = ['dairy_s', 'dairy_l']

#fields the program will need to reference for Orders
fields1 = ['Descriptio', 'RouteName']

#location of Orders file
Orders_Name = 'MTM_exported_Orders.shp'
Orders_file = os.path.join(ws, Orders_Name)

#fields for Routes
fields2 = ['Name', 'OrderCount', 'TotalDista']

#location of Routes file
Routes_Name = 'MTM_exported_Routes.shp'
Routes_file = os.path.join(ws, Routes_Name)

#fields for Frequency of Movement FLAPS file
fields3 = ['Production', 'Pickups_d']

#location of frequency of movement FLAPS file
FoM_FLAPS = r'F:\FMD_Project\Davids_work\Milk_Truck_Model\Dairy_FLAPS\FLAPS_Dairy.gdb\FLAPS_Dairy_precopies_6x'

####################ACTUAL CODE######################
###write title rows and explanation rows on CSV file
writer.writerow( (['RPD = number of unique routes per day, ' + \
                  'SPR = average number of stops per route,']) )
writer.writerow( (['DPR = average distance travelled per route, ' + \
                  'PPW = average number of pickups per week']) )
writer.writerow( ('Category name', 'RPD', 'SPR', 'SPR St Dev', 'SPR Range', \
                  'DPR (km)', 'DPR (miles)', 'DPR St Dev (km)', \
                  'DPR Range (km)', 'PPW', 'PPW St Dev', 'PPW Range') )

#run a loop for each category
for num  in range (0,len(categories)):

    #several blank lists to store information
    route_names = []
    route_names_RAW = []
    num_Orders = []
    distance = []
    FoM = []

    category = categories[num]
    category_formatted = "'%s'" %category
    
    #itterate through the table, find rows with the
    #proper FLAPS category and save it to a list called 'route_names'
    wc1 = """ "Descriptio" = %s AND NOT "RouteName" = ' ' """ %category_formatted
    whereclause1 = wc1.format(arcpy.AddFieldDelimiters(Orders_file, fields1))
    with arcpy.da.SearchCursor(Orders_file, fields1, whereclause1) as cursor_1:
        for row_1 in cursor_1:
            route_names_RAW += [row_1[1]]
            route_names += [row_1[1]]
    route_names = list(set(route_names)) #gets rid of duplicates

    #store important information from the list of routes
    with arcpy.da.SearchCursor(Routes_file, fields2) as cursor2:
        for row_2 in cursor2:
            if row_2[0] in route_names:
                num_Orders += [row_2[1]]
                distance += [row_2[2]]
            else:
                ()

    #now store the data for Frequency of Movement (FoM)
    with arcpy.da.SearchCursor(FoM_FLAPS, fields3) as cursor_3:
        for row_3 in cursor_3:
            if row_3[0] == category:
                FoM += [row_3[1]]

    #calculate numbers
    rpd = float(len(route_names)) / float(numDays) #routes per day
    sum_num_stops = float(sum(num_Orders))
    count_num_Orders = float(len(num_Orders))
    av_stops = round(sum_num_stops / count_num_Orders, 1)
    av_stops_st_dev = round(numpy.std(num_Orders, ddof=0), 2)
    av_stops_range = max(num_Orders) - min(num_Orders)
    dist_m = round(float(sum(distance)) / float(len(distance)))
    dist_km = round(dist_m  / 1000., 1)
    dist_mi = round(dist_m / 1609.34, 1)
    dist_std_dev = int(float(numpy.std(distance, ddof=0))/1000.) #in units of km
    dist_range = int(float(max(distance)-min(distance))/1000.) #in km
    av_FoM = round(float(sum(FoM)) / float(len(FoM)), 2)
    av_FoM_std_dev = round(numpy.std(FoM, ddof=0), 2)
    av_FoM_range = max(FoM) - min(FoM)

    #print stuff
    print categories[num]
    print "Number of unique routes per day: " + str(rpd)
    print "Average number of stops per route: " + str(av_stops) + " stops" \
    + " // " + str(av_stops_st_dev) + " / " + str(av_stops_range)
    print "Average distance traveled per route: " + str(dist_km) \
    + " km  (" + str(dist_mi) + " miles)" + " // " + str(dist_std_dev) \
    + " km / " + str(dist_range) + " km"
    print "Average number of deliveries per week: " \
    + str(av_FoM) + " // " + str(av_FoM_std_dev) + " / " + str(av_FoM_range) + "\n"

    ###write stuff to the CSV file
    writer.writerow( (categories[num], rpd, \
        av_stops, av_stops_st_dev, av_stops_range, dist_km, dist_mi, \
        dist_std_dev, dist_range, av_FoM, av_FoM_std_dev, av_FoM_range) )
    
g.close()
print "--------------All done!--------------"

            
