import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time




df = pd.read_csv("tw_colombia_usa.csv")

df['hour']=df.apply(lambda x:time.strftime('%H', time.strptime(x['created_at'],'%a %b %d %H:%M:%S +0000 %Y')),axis=1)
df['minute']=df.apply(lambda x:int(time.strftime('%M', time.strptime(x['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))//10*10+10,axis=1)
df['time']=df.apply(lambda x:str(x['hour'])+":"+str(x['minute']),axis=1)
print df.groupby(['time']).count()['userID']
