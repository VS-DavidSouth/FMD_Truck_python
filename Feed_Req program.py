#Created by David South   Date: 5/15/17 Updated: N/A
#Generated in conjunction with a USDA-APHIS cooperative agreement.
#note: this program is meant to be run in the Field Calculator in ArcMap
#This program determines the amount of feed required per delivery for
#each FLAPS point.

def fnFR(Pro, numCattle, numSwine, numDeliv): 
   
  import math 
  if Pro == 'cow_calf_l' or Pro == 'cow_calf_s' or Pro == 'feedlot_l' \
    or Pro == 'feedlot_s': 
    FR = float(5 * numCattle) * 7. / float(numDeliv) 
    
  elif Pro == 'dairy_l' or Pro == 'dairy_s': 
    FR = float(11 * numCattle) * 7. / float(numDeliv) 
    
  elif  Pro == 'swine_farrow_to_feeder_l' \
    or Pro == 'swine_farrow_to_feeder_s' or Pro == 'swine_farrow_to_wean_l' \
    or Pro == 'swine_farrow_to_wean_s' or Pro == 'swine_other_l' or \
    Pro == 'swine_other_s' or Pro == 'swine_grower_finisher_l' or \
    Pro == 'swine_grower_finisher_s' or Pro == 'swine_nursery_l': 
    FR = float(2.6 * numSwine) * 7. / float(numDeliv) 
    
  elif Pro == 'swine_farrow_to_finish_l' or Pro == 'swine_farrow_to_finish_s': 
    FR = float(4.17 * numSwine) * 7. / float(numDeliv) 
  
  return FR

fnFR(!Production!, !Cattle! , !Swine!, !Deliv_wk!) 
