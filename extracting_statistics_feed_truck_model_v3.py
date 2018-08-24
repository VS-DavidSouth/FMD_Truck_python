#Extracting Statstics from the Feed Truck Model
#Created by David South -- Date created: 5/29/17 -- Date updated: 6/14/17
#Python version: 2.7
#Purpose: To derive the following statstics from the Feed Truck Model 
# Stats -
#1.Average Distance of a route per livestock category
#2.Average number of stops per route per livestock category
#3.Frequency of movement per livestock category (meaning the average
#number of deliveries to farms from that category per week).

#This work was funded through a USDA-APHIS cooperative agreement.

#####################SETUP###########################
import arcpy, os, numpy, csv
from arcpy import env

ws = r'F:\FMD_Project\Davids_work\Feed_Truck_Model\Deriving Statistics'
env.workspace = ws
env.overwriteOutput = True

#set it up to write to FTM_Results.csv
open(os.path.join(ws,'FTM_Results.csv'), 'wb')
g = open(os.path.join(ws,'FTM_Results.csv'), 'ab')
writer = csv.writer(g, dialect = 'excel')

####################PARAMETERS#######################

#define non-swine(NS) and swine (S) FLAPS categories
#number of livestock:   1-199         200+          1-499      500+
NS_FLAPS_categories = ['cow_calf_s','cow_calf_l', 'dairy_s', 'dairy_l', \
#                     1-999         1000+
                    'feedlot_s', 'feedlot_l']

#S_FLAPS_categories_s is for small swine farms, with 1-999 animals
S_FLAPS_categories_s = ['swine_farrow_to_feeder_s', 'swine_farrow_to_finish_s',\
                        'swine_farrow_to_wean_s', 'swine_grower_finisher_s', \
                        'swine_other_s']

#S_FLAPS_categories_l is for large swine farms, with 1000+ animals
S_FLAPS_categories_l = ['swine_nursery_l', 'swine_farrow_to_feeder_l', \
                        'swine_farrow_to_finish_l', 'swine_farrow_to_wean_l',\
                        'swine_grower_finisher_l', 'swine_other_l']


#fields the program will need to reference for Orders
fields1 = ['Descriptio', 'RouteName']

#fields for Routes
fields2 = ['Name', 'OrderCount', 'TotalDista']

#fields for Frequency of Movement FLAPS file
fields3 =  ['Production', 'Region', 'Deliv_wk']

#list for each region
regions_list = ['Region_1', 'Region_2', 'Region_3', 'Region_4']

#location of frequency of movement FLAPS file
FoM_FLAPS = r'F:\FMD_Project\Davids_work\Feed_Truck_Model\Deriving Statistics\FLAPS_Freq_of_Movement_regions1-4.shp'

####################ACTUAL CODE######################
#print intro
intro = "Feed Truck Model - Statistics for InterSpread Plus\n" + \
        "Project done by David South with the help of Dr. Hadrich, Dr. Hagerman,\n" +\
        "Dr Magzamen and Dr. Wolf\n\nThe numbers '// A / B' are the Standard Deviation(A)" +\
        "and the Range(B)\n" +\
        "\n-\n-\n-"
print intro

#write explanation rows on CSV file
writer.writerow( (['RPD = number of unique routes per day, ' + \
                  'SPR = average number of stops per route,']) )
writer.writerow( (['DPR = average distance travelled per route, ' + \
                  'DPW = average number of deliveries per week']) )

#function for finding population standard deviation and range of the list
#note this is only used at the end of the code when the results are printed
def fnStats(numericList, units):
    stDev = round(numpy.std(numericList, ddof=0), 2)
    maxList = max(numericList)
    minList = min(numericList)
    if units == "km":
        maxList = float(maxList)/1000.
        minList = float(minList)/1000.
        stDev = int(round(float(stDev)/1000.))
    return "  {{" + str(stDev) + " " + units + ", " + \
           str(int(round(maxList - minList))) + " " + units + "}}"

#run a loop for each region
for rn in range (0, len(regions_list)): #rn stands for Region Number, such as Region 1, etc
    
    #print seperating text between each region
    print "------------" + regions_list[rn].upper().replace("_", " ") + "------------\n"

    #write region number and the labels for each column
    writer.writerow( ( ) )
    writer.writerow( ([regions_list[rn].title().replace("_", " ")]) )
    writer.writerow( ('Category name', 'RPD', 'SPR', 'SPR St Dev', 'SPR Range', \
                  'DPR (km)', 'DPR (miles)', 'DPR St Dev (km)', \
                  'DPR Range (km)', 'DPW', 'DPW St Dev', 'DPW Range') )


    #location of Orders file
    Orders_Name = 'exported_Orders_' + regions_list[rn] + '.shp'
    Orders_file = os.path.join(ws, Orders_Name)

    #location of Routes file
    Routes_Name = 'exported_Routes_' + regions_list[rn] + '.shp'
    Routes_file = os.path.join(ws, Routes_Name)

    #run a loop for each category
    for catNum  in range (0,len(NS_FLAPS_categories)+2):

        #create several blank lists to store information
        route_names = []
        route_names_RAW = []
        num_Orders = []
        distance = []
        FoM = []

        
        ##note that NS means non-swine, S means swine in the variable names##
        
        if catNum + 1 <= len(NS_FLAPS_categories): #for the non-swine portion
            category = NS_FLAPS_categories[catNum]
            category_formatted = "'%s'" %category
            
            #for non-swine: itterate through the table, find rows with the
            #proper FLAPS category and save it to a list called 'route_names'
            wc1 = """ "Descriptio" = %s AND NOT "RouteName" = ' ' """ %category_formatted
            whereclause1 = wc1.format(arcpy.AddFieldDelimiters(Orders_file, fields1))
            with arcpy.da.SearchCursor(Orders_file, fields1, whereclause1) as cursor1_NS:
                for row_1 in cursor1_NS:
                    route_names_RAW += [row_1[1]]
            route_names = list(set(route_names_RAW)) #gets rid of duplicates

            #since finding the Frequency of Movement(FoM) requires a different file
            #this code just creates a list of all the FLAPS for the current category
            with arcpy.da.SearchCursor(FoM_FLAPS, fields3) as cursor1_NS_FoM:
                for row_FoM1 in cursor1_NS_FoM:
                    #individual regions
                    if rn + 1 <= 4:
                        if row_FoM1[0] == NS_FLAPS_categories[catNum] \
                        and row_FoM1[1] == rn + 1:
                            FoM += [row_FoM1[2]]
                    #all regions
                    elif rn + 1 == 5:
                        if row_FoM1[0] == NS_FLAPS_categories[catNum]:
                            FoM += [row_FoM1[2]]
                        

        elif catNum + 1 > len(NS_FLAPS_categories): #for the swine portion

            #itterate through the table, find rows with the
            #proper FLAPS category and save it to a list called 'route_names'
            wc1 = """ NOT "RouteName" = ' ' """ 
            whereclause1 = wc1.format(arcpy.AddFieldDelimiters(Orders_file, fields1))
            with arcpy.da.SearchCursor(Orders_file, fields1, whereclause1) as cursor1_S:
                for row_1 in cursor1_S:
                    #small swine
                    if catNum + 1 == len(NS_FLAPS_categories) + 1:
                        if row_1[0] in S_FLAPS_categories_s:
                            route_names_RAW += [row_1[1]]
                    #large swine
                    elif catNum + 1 == len(NS_FLAPS_categories) + 2:
                        if row_1[0] in S_FLAPS_categories_l:
                            route_names_RAW += [row_1[1]]
            route_names = list(set(route_names_RAW)) #get rid of duplicates in the list

            #save data for Frequency of Movement (FoM)
            with arcpy.da.SearchCursor(FoM_FLAPS, fields3) as cursor1_NS_FoM:
                for row_FoM2 in cursor1_NS_FoM:
                    #small swine
                    if catNum + 1 == len(NS_FLAPS_categories) + 1:
                        if row_FoM2[0] in S_FLAPS_categories_s:
                            #individual regions
                            if rn + 1 <= 4:
                                if row_FoM2[1] == rn + 1:
                                    FoM += [row_FoM2[2]]
                            #all regions
                            elif rn + 1 == 5:
                                FoM += [row_FoM2[2]]
                    #large swine
                    elif catNum + 1 == len(NS_FLAPS_categories) + 2:
                        if row_FoM2[0] in S_FLAPS_categories_l:
                            if rn + 1 <= 4:
                                if row_FoM2[1] == rn + 1:
                                    FoM += [row_FoM2[2]]
                            elif rn + 1 == 5:
                                FoM += [row_FoM2[2]]
        
        #take the list route_names, and save the important information in new lists
        with arcpy.da.SearchCursor(Routes_file, fields2) as cursor2:
            for row_2 in cursor2:
                if row_2[0] in route_names:
                    num_Orders += [row_2[1]]
                    distance += [row_2[2]]
                else:
                    ()

        #calculate numbers
        rpd = float(len(route_names)) / 5. #routes per day
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

        ##print a bunch of stuff.##
        print regions_list[rn]
        #decide what to print based on which category the loop is in
        if catNum + 1 <= len(NS_FLAPS_categories): 
            print "FLAPS category:      " + category
        elif catNum + 1 == len(NS_FLAPS_categories) + 1:
            print "Swine category:      small"
        elif catNum + 1 == len(NS_FLAPS_categories) + 2:
            print "Swine category:      large"
        
        print "Number of unique routes per day: " + str(rpd)
        print "Average number of stops per route: " + str(av_stops) + " stops" \
        + " // " + str(av_stops_st_dev) + " / " + str(av_stops_range)
        print "Average distance traveled per route: " + str(dist_km) \
        + " km  (" + str(dist_mi) + " miles)" + " // " + str(dist_std_dev) \
        + " km / " + str(dist_range) + " km"
        print "Average number of deliveries per week: " \
        + str(av_FoM) + " // " + str(av_FoM_std_dev) + " / " + str(av_FoM_range) + "\n"

        #define what category it is so the CSV knows what to write
        if catNum + 1 <= len(NS_FLAPS_categories): 
            category = category.title().replace("_", " ")
        elif catNum + 1 == len(NS_FLAPS_categories) + 1:
            category = 'swine_s'
        elif catNum + 1 == len(NS_FLAPS_categories) + 2:
            category = 'swine_l'


        #write stuff to the CSV file
        writer.writerow( (category, rpd, \
            av_stops, av_stops_st_dev, av_stops_range, dist_km, dist_mi, \
            dist_std_dev, dist_range, av_FoM, av_FoM_std_dev, av_FoM_range) )
                

g.close()

print "--------------All done!--------------"
