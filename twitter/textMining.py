import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import time
from pymongo import *
import re
from TopicModeling import *#algorito LDA

dbName = "tw_arg_usa";

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
df = pd.read_csv("tw_arg_usa.csv")

df['hour']=df.apply(lambda x:time.strftime('%H', time.strptime(x['created_at'],'%a %b %d %H:%M:%S +0000 %Y')),axis=1)
df['minute']=df.apply(lambda x:int(time.strftime('%M', time.strptime(x['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))//10*10,axis=1)
#df['time']=df.apply(lambda x:str(x['hour'])+":"+str(x['minute']),axis=1)
grouped_df=df.groupby(['hour','minute'])
for key, item in grouped_df:
	aux_df= grouped_df.get_group(key)
	document=Document(collection)
	aux_df.apply(document.obtenerPedazoDocumento,axis=1)
	documents.append(document.documentText)


#clase que clacula LDA, 
#tern score es el metodo que selecciona las palabras mas relevantes
lda_wrapper = TopicModelingLDA(documents, "term_score")
#recibe numero de topicos: le pongo el numero de documentos xd
#recibe el numero de iteraciones: le pongo 10
lda_wrapper.fit(len(documents), 10)

#se obtienen las 10 palabras mas importantes de cada topico
top10 = lda_wrapper.get_highest_scores()

"""
for i,doc in enumerate(documents):
	print ("******************DOCUMENTO NUMERO: ",i, " ********************")
	print (doc)
"""

