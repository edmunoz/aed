import numpy as np
#import matplotlib.pyplot as plt
import time
import re
import os
from TopicModeling import *#algorito LDA


documentosPath = "Facebook-docs/Chile Vs Argentina"
docNames = os.listdir(documentosPath);

documentos =[]
for d in docNames:
	if(d.find(".txt")!=-1):
		fileName = documentosPath + "/" + d
		with open(fileName, 'r') as myfile:
			texto = myfile.read()
			texto = re.sub('[.@/:!?"#$\n]', '', texto)
			documentos.append(texto)



#clase que clacula LDA, 
#tern score es el metodo que selecciona las palabras mas relevantes
lda_wrapper = TopicModelingLDA(documentos, "term_score")
#recibe numero de topicos: le pongo el numero de documentos xd
#recibe el numero de iteraciones: le pongo 10
lda_wrapper.fit(10, 10)

#se obtienen las 10 palabras mas importantes de cada topico
top10 = lda_wrapper.get_highest_scores()


