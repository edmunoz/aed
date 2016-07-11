import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time




df = pd.read_csv("tw_colombia_usa.csv")

df['hour']=df.apply(lambda x:time.strftime('%H', time.strptime(x['created_at'],'%a %b %d %H:%M:%S +0000 %Y')),axis=1)
df['minute']=df.apply(lambda x:int(time.strftime('%M', time.strptime(x['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))//10*10+10,axis=1)
df['time']=df.apply(lambda x:str(x['hour'])+":"+str(x['minute']),axis=1)
print df.groupby(['time']).count()['userID']

hour=["00:30",
"00:40",
"00:50",
"01:50",
"01:60",
"02:10",
"02:20",
"02:30",
"02:40",
"02:50",
"02:60",
"03:10",
"03:20",
"03:30",
"03:40",
"03:50",
"03:60"]

frec=[24,
23,
24,
12,
23,
20,
16,
17,
21,
24,
18,
23,
16,
23,
22,
10,
2]



x=range(0,17)
plt.xticks(x, hour,rotation='vertical')
plt.plot(x, frec)
#df.groupby(['time']).count()['userID'].plot(kind="line")
plt.ylabel('Tweets Frecuency')
plt.xlabel('Time')
plt.title('Colombia vs USA')
plt.plot(x,frec)
plt.show()