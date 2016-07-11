import gpxpy.geo
from pandas import *
import math
import matplotlib.pyplot as plt

fileName="tl_user_mexico_chile.csv"

result=[]
def obtenerRadioGiro(x):
	usuario={}
	coglat=x['lat'].mean()
	coglng=x['lng'].mean()
	x['aux']=x.apply(lambda row: gpxpy.geo.haversine_distance(row['lat'],row['lng'],coglat,coglng)**2  ,axis=1)
	#print ('(rti-GOTi)2 ',x['aux']+ '\n')
	result.append(math.sqrt(x['aux'].mean()))
	return x

df = pandas.read_csv(fileName, parse_dates = True)
group = df.groupby("userID");


group.apply(obtenerRadioGiro)

re = pandas.DataFrame(result)
re.hist()
plt.ylabel("frecuency")
plt.xlabel("ROG (Km)")
plt.title("ROG Mexico vs. Chile")
plt.show()

#print group
#frames = [coglat, coglng];
#result = concat(frames, axis = 1)
#result.columns = ['coglat', 'coglng'];