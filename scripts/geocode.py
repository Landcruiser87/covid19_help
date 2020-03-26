#%%
from pygeocoder import Geocoder
from googlemaps import Client as GoogleClient
from googlemaps.places import find_place
import pandas as pd
import numpy as np
import time

#Import API Key.  NEVER store it in a doc
with open('apikey.txt') as f:
    api_k = f.readline()
    f.close
#Load up the Google Places and Geocoder API's
Geocoder = Geocoder(api_key=api_k)
gmaps = GoogleClient(key=api_k)

#read in Data
crematory_df = pd.read_csv("crematories.csv", sep=",")
crematory_df = crematory_df[0:70]
#Set up blank lists for lat long
Lat = []
Long = []
bad_rows = []

#Loop through DF.  
# First try Geocoder to extract lat long
# If that fails, do a places search
# If that fails, Then the business is probably shut down. 

for idx, row in crematory_df.iterrows():
	results = Geocoder.geocode(row[1])
	time.sleep(2)
	if results.valid_address == True:
		# If address is true pulls lat long and updates address with Goog formatted one
		cords = str(results.coordinates).strip("()")
		Lat.append(float(cords.split(',')[0]))
		Long.append(float(cords.split(',')[1]))
		crematory_df['Address'][idx] = results.formatted_address
	else:
		local = gmaps.find_place(
						input=str(row[0]+' '+row[1]), 
						input_type='textquery',
						fields=['name', 'geometry', 'formatted_address']) 	
		if local['status'] == 'OK':
			# If status is OK, pulls lat long and updates address with Goog formatted one.
			crematory_df['Address'][idx] = local['candidates'][0]['formatted_address']
			Lat.append(local['candidates'][0]['geometry']['location']['lat'])
			Long.append(local['candidates'][0]['geometry']['location']['lng'])
		else:
			# If both fail, well then maybe that funeral home is out of business. 
			print("There is no hope for {} Neither API could find it".format(row[1]))
			bad_rows.append(row[1])
			Lat.append(np.NAN)
			Long.append(np.NAN)

# Attach lat long lists to the dataframe 
crematory_df['Lat'] = Lat
crematory_df['Long'] = Long
crematory_df['Address'] = crematory_df['Address'].str.replace('United States','USA')
# Export to CSV City
crematory_df.to_csv("crematories_0_70.csv", index=False)



#%%
#Test crap
results = Geocoder.geocode("Paris, France")
print(results[0].coordinates)

