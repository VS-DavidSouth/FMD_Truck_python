#Created by David South
#Note: this is not meant to be run in the python IDE nor the arcpy addon for
#ArcMap. This is meant to be run in the Field Calculator
#This is meant to have python decide how many deliveries per week that
#FLAPS point will get

def fnDeliv_wk(Pro, numCattle, numSwine, deliv_2_wks):
  import math

    if Pro == 'cow_calf_l' or Pro == 'cow_calf_s' or Pro == 'feedlot_l'\
    or Pro == 'feedlot_s': 
    FR = float(5 * numCattle)
  
  elif Pro == 'dairy_l' or Pro == 'dairy_s': 
    FR = float(11 * numCattle)
  
  elif  Pro == 'swine_farrow_to_feeder_l' \
    or Pro == 'swine_farrow_to_feeder_s' or Pro == 'swine_farrow_to_wean_l' \
    or Pro == 'swine_farrow_to_wean_s' or Pro == 'swine_other_l' or \
    Pro == 'swine_other_s' or Pro == 'swine_grower_finisher_l' or \
    Pro == 'swine_grower_finisher_s' or Pro == 'swine_nursery_l': 
    FR = float(2.6 * numSwine)
  
  elif Pro == 'swine_farrow_to_finish_l' or Pro == 'swine_farrow_to_finish_s': 
    FR = float(4.17 * numSwine)

  num_deliv = float((FR * 7) /50000)

  if deliv_2_wks == True:
    if num_deliv > 0 and num_deliv <= 0.5:
      deliv_wk = 0.5
    
    elif num_deliv <= 3 and num_deliv > 0.5:
      deliv_wk = int(math.ceil(num_deliv))
      
    elif num_deliv > 3:
      deliv_wk = int(3)
      
    else:
      deliv_wk = int(9)
    
  elif deliv_2_wks == False:
    if num_deliv <= 3 and num_deliv > 0:
      deliv_wk = int(math.ceil(num_deliv))
      
    elif num_deliv > 3:
      deliv_wk = int(3)
      
    else:
      deliv_wk = int(9)
    
  return deliv_wk

##Note: the following code goes into the [field] = [blank] area,
#not in Pre-Logic Script Code.
#for the minimum number of deliveries per week to be 1/week, use this code:
fnDeliv_wk(!Production!, !Cattle!, !Swine!, False)

#for the minimum to be 1/2weeks, use this code:
fnDeliv_wk(!Production!, !Cattle!, !Swine!, True)



