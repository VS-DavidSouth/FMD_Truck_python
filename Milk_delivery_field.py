#Created by David South
#Milk_delivery_field -- Milk Truck Model
#This program is meant to be run in the Field Calculator in ArcMap 10.4.1
#It is intended to be used to calculate the field Milk_delivery on the
#Dairy_FLAPS file.

def fnMilk_delivery(milk_daily,pickups_d):
  if pickups_d <= 1:
    milk_delivery = milk_daily

  else:
    milk_delivery = float(milk_daily) / float(pickups_day)

  return int(milk_delivery)
