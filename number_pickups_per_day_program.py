#Created by David South
#number of pickups per day program -- Milk Truck Model
#This program is meant to be run in the Field Calculator in ArcMap 10.4.1
#It calculates how many pickups per day are required at each FLAPS point.
#Note: if you want the minimum number of pickups to be once every 2 days,
#ensure that the last input of fnP_d is True. False will result in a minimum
#of one pickup per day.


#Put this part in the Pre-Logic Script Code: 
import math  
def fnP_d(numCattle, pickup_every_other_day):  
  P_d_raw = float(numCattle) * 7.7 / float(6500)  
    
  if pickup_every_other_day == True:
    if P_d_raw <= 0.5:
      P_d = 0.5

    else:
      P_d = int(math.ceil(P_d_raw))

  elif pickup_every_other_day == False:
    if P_d_raw <= 1:  
      P_d = 1  
  
    else:  
      P_d = int(math.ceil(P_d_raw)) 
 
  return P_d

##Note: the following code goes into the [field] = [blank] area
#If you want a minimum of one pickup per day, use this code:
fnP_d(!Cattle!, False)

#If you want a minimum of one pickup per two days, use this code:
fnP_d(!Cattle!, True)
