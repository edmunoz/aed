import pandas as pd
import numpy as np
from pymongo import *
import matplotlib.pyplot as plt
import time


dbName = "tw_ecuador_eeuu";

client = MongoClient('localhost', 27017)
db = client['twitter_db']
collection = db[dbName]

def obtenerTexto(idTuit):
	tuits = collection.find({"id": idTuit})
	if(tuits.count()==0):
		print("No existe ese tuit")
		return None

	t = tuits.next()
	texto = t["text"]
	print(t["text"]) 
	return texto

"""
df = pd.read_csv("tw_colombia_usa.csv")

df.apply();


df['hour']=df.apply(lambda x:time.strftime('%H', time.strptime(x['created_at'],'%a %b %d %H:%M:%S +0000 %Y')),axis=1)
df['minute']=df.apply(lambda x:int(time.strftime('%M', time.strptime(x['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))//10*10+10,axis=1)
df['time']=df.apply(lambda x:str(x['hour'])+":"+str(x['minute']),axis=1)
print (df.groupby(['time']))

"""

