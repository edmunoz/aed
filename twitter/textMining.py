import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from pymongo import *
import re
dbName = "tw_chile_argentina_final";

client = MongoClient('localhost', 27017)
db = client['twitter_db']
collection = db[dbName]

class Document():
	def __init__(self,col):
		self.documentText=""
		self.collection=col
	def obtenerPedazoDocumento(self,row):
		texto=self.obtenerTexto(row['id'])
		texto = re.sub('[.@/:!?"#$\n]', '', texto)
		self.documentText=self.documentText+texto
		return 1

	def obtenerTexto(self,idTuit):
		tuits = self.collection.find({"id": idTuit})
		if(tuits.count()==0):
			print("No existe ese tuit")
			return None
		t = tuits.next()
		texto = t["text"]
		return texto

documents=[]
df = pd.read_csv("tw_chile_argentina_final.csv")

df['hour']=df.apply(lambda x:time.strftime('%H', time.strptime(x['created_at'],'%a %b %d %H:%M:%S +0000 %Y')),axis=1)
df['minute']=df.apply(lambda x:int(time.strftime('%M', time.strptime(x['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))//10*10,axis=1)
#df['time']=df.apply(lambda x:str(x['hour'])+":"+str(x['minute']),axis=1)
grouped_df=df.groupby(['hour','minute'])
for key, item in grouped_df:
	aux_df= grouped_df.get_group(key)
	document=Document(collection)
	aux_df.apply(document.obtenerPedazoDocumento,axis=1)
	documents.append(document.documentText)
for i,doc in enumerate(documents):
	print "******************DOCUMENTO NUMERO: ",i, " ********************"
	print doc

