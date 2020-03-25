#%%
from pygeocoder import Geocoder
from googlemaps import Client as GoogleMaps
from googlemaps.places import places_nearby
import pandas as pd
import numpy as np
import time

with open('apikey.txt') as f:
    api_k = f.readline()
    f.close

Geocoder = Geocoder(api_key=api_k)
gmaps = GoogleMaps(key=api_k)

crematory_df = pd.read_csv("crematories.csv", sep=",")
crematory_df = crematory_df[0:5]
Lat = []
Long = []

for idx, row in crematory_df.iterrows():
	# print(row[1])
	results = Geocoder.geocode(row[1])
	# time.sleep(2)
	if results.valid_address == True:
		cords = str(results.coordinates).strip("()")
		Lat.append(float(cords.split(',')[0]))
		Long.append(float(cords.split(',')[1]))
	else:
		print("There was an error with {}".format(row[1]))
		Lat.append(np.NAN)
		Long.append(np.NAN)
		# local = gmaps.places_nearby(row[1]) #str(row[0]+' '+row[1])
		# local_result = local['responseData']['results'][0]
		# Lat.append(local_result['geometry']['lat'])
		# Long.append(local_result['geometry']['long'])

crematory_df["Lat"] = Lat
crematory_df["Long"] = Long
crematory_df.head(5)





#%%
#Test crap
results = Geocoder.geocode("Paris, France")
print(results[0].coordinates)

