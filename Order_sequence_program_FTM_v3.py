#This program is intended to be able to be run either in the IDLE window
#or in the ArcPy window of ArcGIS 10.4
#Files required for program to run:
#   Exported Routes file
#   Exported Orders file

#######################SETUP####################
print ("Running program...\n")

import arcpy, csv, os
from arcpy import env

#set workplace environment
ws = r'F:\FMD_Project\Davids_work\Feed_Truck_Model\Deriving Statistics'
env.workspace = ws
env.overwriteOutput = True

#set it up to write to several CSV files
open(os.path.join(ws,'Order_sequence.csv'), 'wb')
wr1 =open(os.path.join(ws,'Order_sequence.csv'), 'ab')
writer1 = csv.writer(wr1, dialect = 'excel')

open(os.path.join(ws,'Category_co-occurance_x2.csv'), 'wb')
wr2 =open(os.path.join(ws,'Category_co-occurance_x2.csv'), 'ab')
writer2 = csv.writer(wr2, dialect = 'excel')

open(os.path.join(ws,'Category_co-occurance_x3.csv'), 'wb')
wr3 =open(os.path.join(ws,'Category_co-occurance_x3.csv'), 'ab')
writer3 = csv.writer(wr3, dialect = 'excel')

########################PARAMETERS##############
#locations of exported Orders files (R1 = Region 1, etc)
Orders_R1 = r'F:\FMD_Project\Davids_work\Feed_Truck_Model\Deriving Statistics\exported_Orders_Region_1.shp'
Orders_R2 = r'F:\FMD_Project\Davids_work\Feed_Truck_Model\Deriving Statistics\exported_Orders_Region_2.shp'
Orders_R3 = r'F:\FMD_Project\Davids_work\Feed_Truck_Model\Deriving Statistics\exported_Orders_Region_3.shp'
Orders_R4 = r'F:\FMD_Project\Davids_work\Feed_Truck_Model\Deriving Statistics\exported_Orders_Region_4.shp'
Orders = [Orders_R1, Orders_R2, Orders_R3, Orders_R4]

#locations of exported Routes files
Routes_R1 = r'F:\FMD_Project\Davids_work\Feed_Truck_Model\Deriving Statistics\exported_Routes_Region_1.shp'
Routes_R2 = r'F:\FMD_Project\Davids_work\Feed_Truck_Model\Deriving Statistics\exported_Routes_Region_2.shp'
Routes_R3 = r'F:\FMD_Project\Davids_work\Feed_Truck_Model\Deriving Statistics\exported_Routes_Region_3.shp'
Routes_R4 = r'F:\FMD_Project\Davids_work\Feed_Truck_Model\Deriving Statistics\exported_Routes_Region_4.shp'
Routes = [Routes_R1, Routes_R2, Routes_R3, Routes_R4]

#define the fields that the program will need to look at for the Routes file
fields1 = ['Name', 'TotalDista']

#define fields that the program will need to look at for the Orders file
fields2 = ['FID', 'Descriptio', 'RouteName', 'Sequence']

#define major categories:
cow_calf = ['cow_calf_l', 'cow_calf_s']
dairy = ['dairy_l', 'dairy_s']
feedlot = ['feedlot_l', 'feedlot_s']
swine = ['swine_farrow_to_feeder_l', 'swine_farrow_to_feeder_s', \
         'swine_farrow_to_wean_l', 'swine_farrow_to_wean_s', \
         'swine_other_l ', 'swine_other_s', 'swine_farrow_to_finish_l', \
         'swine_farrow_to_finish_s', 'swine_grower_finisher_l', \
         'swine_grower_finisher_s', 'swine_nursery_l']
all_categories = cow_calf + dairy + feedlot + swine

########################ACTUAL CODE############
#define RouteNames and MasterList(1-3)
#MasterList contains info for each Region
#MasterList2-3 contain info on how many times certain combinations occur
#Region number: 1   2   3   4
#index number:  0   1   2   3
RouteNames = [ [], [], [], [] ]
MasterList = [ [], [], [], [] ]
MasterList2 = []
MasterList3 = []

#define the variable that will be used to count the number of 'active' Routes
active_Routes = 0

###setup loop##
#for each region, do a thing
for r in range (0,4):

    ###First, save a list of all the names of the active Routes###
    #Routes must not have a distance of 0
    #Iterate through each route, find
    wc1 = """NOT "TotalDista" = 0"""
    with arcpy.da.SearchCursor(Routes[r], fields1, wc1) as Cursor1:
        for row1 in Cursor1:
            RouteNames[r] += [row1[0]]
            active_Routes += 1

    ###Now, go through and save the information for each Route###
    for num in range (0, len(RouteNames[r])):

        #define/reset temporary list
        tempList = []

        #define a whereclause that states to only view Orders that are status: OK
        wc2 = """ "Status" = 0"""
        
        with arcpy.da.SearchCursor(Orders[r], fields2, wc2) as Cursor2:
            for row2 in Cursor2:

                if row2[2] == RouteNames[r][num]:
                    tempList += [row2[1]]

        MasterList[r] += [tempList]
             


###How to read MasterList###
#Key: MasterList[a][b][c]
#the first index [a] is the Region number.'0' is Region 1, etc.
#The second index [b] is the Route index, this is in no particular sequence.
#The third index [c] is the Order index, also in no particular sequence
# this index [c] contains FLAPS category information
# the FLAPS cateogry [0] or the specific sequence number for that order [1].
# Note, the lowest value will be 2 becuase leaving the Depot is
# considered stop #1.



###Now for the part where we figure out what these huge lists actually tell us!###

#build MasterList2
for category1 in range(0, len(all_categories)):
    
    #add another blank list inside MasterList2-3 which will contain more lists
    MasterList2 += [[]]
    MasterList3 += [[]]

    for category2 in range(0, len(all_categories)):
        #add the final layer of lists inside MasterList2[category1]
        # once this loop completes, there is one list per each
        # unique combination of FLAPS categories. The list contains
        # the number of times that particular combination occurs
        MasterList2[category1] += [0]
        MasterList3[category1] += [[]]

        for category3 in range(0, len(all_categories)):
            
            #add blank values to MasterList3
            MasterList3[category1][category2] += [0]
        
#define a function that you will call back several times
def fnCount(a1,a2): #inputs must be intigers
    for category1 in range(0, len(all_categories)):
    
        
        for category2 in range(0, len(all_categories)):
            #Once this loop completes, there is one list per each
            # unique combination of FLAPS categories, inside MasterList2.
            # The list contains the number of times that particular
            # combination occurs. This level is for 2 values that
            # occur together. The next level is for 3 values co-occuring.

            #count the number of times that particular combination occurs
            if all_categories[category1] in MasterList[a1][a2] \
               and all_categories[category2] in MasterList[a1][a2]:
                MasterList2[category1][category2] += 1

            #find which groups of 3 categories co-occur
            for category3 in range(0, len(all_categories)):

                #don't record values that are the same, such as
                # [dairy_l, dairy_l, dairy_l] or
                # [feedlot_l, feedlot_l, swine_other_l]
                # These combinations would have been recorded in
                # the previous loop. Fill them with 'N/A', to be
                # deleted later
                #the next 3 lines of code can be used to get rid of doubles,
                # which were already recorded in MasterList2. If used, change
                # the next 'if' to an 'elif'
               # if category1 == category2 or category2 == category3 or \
               #    category3 == category1:
               #     MasterList3[category1][category2][category3] = 'N/A'

                if all_categories[category1] in MasterList[a1][a2] \
               and all_categories[category2] in MasterList[a1][a2] \
               and all_categories[category3] in MasterList[a1][a2]:
                    MasterList3[category1][category2][category3] += 1

#for each Route, do a thing
for d in range (0, len( MasterList )): #for each Region
    for e in range (0, len( MasterList[d] )): #for each Route in the Region
        #for f in range (0, len( MasterList[d][e] )): #for each Order
        
        fnCount(d,e)

#so this next segment of text is not currently being used, but it was saved just in case
def fnNoDoubles():
    #go through and delete all the values in MasterList3 that are 'N/A'
    for category1 in range(0, len(all_categories)):
        for category2 in range(0, len(all_categories)):
            index = 0
            while index < len(all_categories):
                if len(MasterList3[category1][category2]) == 0:
                    break
                if MasterList3[category1][category2][index] == 'N/A':
                    del MasterList3[category1][category2][index]
                    if index >= len(MasterList3[category1][category2]):
                        break
                else:
                    index = index + 1
                    if index >= len(MasterList3[category1][category2]):
                        break
                
###Now, write all the important information into the CSV files###
                
#write first row of first CSV file
writer1.writerow( ('Region Number', 'Route Name', 'FLAPS Category') )

#write the results of MasterList
for a in range (0, len( MasterList )): #for each Region
    for b in range (0, len( MasterList[a] )): #for each Route in that Region
        for c in range (0, len( MasterList[a][b] )): #for each Order
            #write in the following columns: Region, Route Name, FLAPS Category
            writer1.writerow( (a+1, RouteNames[a][b], MasterList[a][b][c]) )
            
#write first row of second CSV file
writer2.writerow( ('First Category', 'Second Category', 'Number of occurances', \
                   'Percentage of Routes', 'Probability') )

#write results of MasterList2 (how often each matchup of two categories occurs)
for g in range(0, len(MasterList2)):
    for h in range(0, len(MasterList2[g])):
        #calculate the Probability field, if it would divide by 0, answer is 0
        if MasterList2[g][g] == 0:
            prob2 = 0
        else:
            prob2 = float(MasterList2[g][h])/float(MasterList2[g][g])
        
        writer2.writerow( (all_categories[g], all_categories[h], \
         MasterList2[g][h], float(MasterList2[g][h])/float(active_Routes), \
         prob2) )
            
#write first row of third CSV file
writer3.writerow( ('First Category', 'Second Category', 'Third Category', \
                   'Number of occurances', 'Percentage of Routes') )


#write results of MasterList3 (how often each matchup of 3 categories occurs)
for i in range(0, len(MasterList3)):
    for j in range(0, len(MasterList3[i])):
        for k in range(0, len(MasterList3[i][j])):
            writer3.writerow( (all_categories[i], all_categories[j], \
             all_categories[k], MasterList3[i][j][k], \
             float(MasterList3[i][j][k])/float(active_Routes)) )
                              
print "Completed."
