import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
file_name_in="../dataset/tw_chile_argentina_final_timeLine.csv"
file_name_out="../dataset/tw_chile_argentina_final_timeLine_country.csv"
df = pd.read_csv(file_name_in)

def getContry(x):
	geolocator = Nominatim()
	print str(x['lat']) +' ,' + str(x['lng'])
	try:
		location = geolocator.reverse(str(x['lat'])+","+str(x['lng']),timeout=10)
		print location.raw['address']['country']
		return location.raw['address']['country']
	except GeocoderTimedOut as e:
		print("Error: geocode failed on input %s with message %s"%(my_address, e.msg))
		return None

	
df['country']=df.apply(getContry ,axis=1)
df.to_csv(file_name_out, sep=',')
