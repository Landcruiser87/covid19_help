
# %%
from pygeocoder import Geocoder
import pandas as pd
import numpy as np

Geocoder = Geocoder(api_key='AIzaSyAcNy0IO12O-Uqdii8ZE36wPpxz6M-woEI')
crematory_df = pd.read_csv("crematories.csv", sep=",")
crematory_df = crematory_df[0:10]

Lat = []
Long = []

for row in crematory_df['Address']:
	results = Geocoder.geocode(row)
	if results.valid_address == True:
		cords = str(results.coordinates)
		Lat.append(cords.split(',')[0])
		Long.append(cords.split(',')[1])
	else:
		print("There was an error with {}".format(row))
		Lat.append(np.NAN)
		Long.append(np.NAN)

crematory_df["Lat"] = Lat
crematory_df["Long"] = Long

crematory_df.head(5)


#%%


results = Geocoder.geocode("Paris, France")
print(results[0].coordinates)

