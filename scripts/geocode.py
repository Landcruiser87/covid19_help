#%%
from pygeocoder import Geocoder
from googlemaps import Client as GoogleClient
from googlemaps.places import find_place
import pandas as pd
import numpy as np
import time
import re 

#print(os.getcwd())
with open('apikey.txt') as f:
    api_k = f.readline()
    f.close

Geocoder = Geocoder(api_key=api_k)
gmaps = GoogleClient(key=api_k)

crematory_df = pd.read_csv("crematories.csv", sep=",")
crematory_df = crematory_df[0:5]
Lat = []
Long = []

for idx, row in crematory_df.iterrows():
	# print(row[1])
	results = Geocoder.geocode(row[1])
	time.sleep(2)
	if results.valid_address == True:
		cords = str(results.coordinates).strip("()")
		Lat.append(float(cords.split(',')[0]))
		Long.append(float(cords.split(',')[1]))
		crematory_df['Address'][idx] = results.formatted_address
	else:

		# print("There was an error with {}".format(row[1]))
		# Lat.append(np.NAN)s
		# Long.append(np.NAN)
		local = gmaps.find_place(
						input=str(row[0]+' '+row[1]), 
						input_type='textquery',
						fields=['place_id', 'name', 'types', 'geometry', 'formatted_address']) 	
		crematory_df['Address'][idx] = local['candidates'][0]['formatted_address']
		Lat.append(local['candidates'][0]['geometry']['location']['lat'])
		Long.append(local['candidates'][0]['geometry']['location']['lng'])

crematory_df["Lat"] = Lat
crematory_df["Long"] = Long
crematory_df['Address'] = crematory_df['Address'].str.replace('United States','USA')
crematory_df.head(5)





#%%
#Test crap
results = Geocoder.geocode("Paris, France")
print(results[0].coordinates)

