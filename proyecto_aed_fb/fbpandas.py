import pandas as pd
import pandas.io.sql
import numpy as np
import matplotlib.pyplot as plt
import MySQLdb as mdb
from mysql.connector import Error
from time import gmtime, strftime, strptime

# server = '108.167.133.34'
# db = ''

# mysql_cn = mdb.connect(host='108.167.133.34', port=3306,user='connie_usr_aed',passwd='SK5CTTs8zXV9',db='connie_facebook')

# query_post = "select * from post where created_time like '2016-06-26%';"
# query_like = 'select * from post_like;'
# query_comment = 'select * from comment;' 
# dfPost_complete = pd.read_sql(query_post, con= mysql_cn)
# dfLike_complete = pd.read_sql(query_like, con= mysql_cn)
# dfComment_complete = pd.read_sql(query_comment, con= mysql_cn)
# mysql_cn.close()

# dfPost_complete.to_csv('postFile.csv')
# dfLike_complete.to_csv('likeFile.csv')
# dfComment_complete.to_csv('commentFile.csv')

dfPost_complete = pd.read_csv('postFile.csv')

print dfPost_complete


# dfPost_complete['day'] = dfPost_complete.apply(lambda x:strftime('%d', strptime(x['created_time'],'%Y-%m-%dT%H:%M:%S+0000')),axis=1)
# dfPost_complete['month'] = dfPost_complete.apply(lambda x:strftime('%m', strptime(x['created_time'],'%Y-%m-%dT%H:%M:%S+0000')),axis=1)
# dfPost_complete['hour']= dfPost_complete.apply(lambda x:strftime('%H', strptime(x['created_time'],'%Y-%m-%dT%H:%M:%S+0000')),axis=1)
# dfPost_complete['minute']= dfPost_complete.apply(lambda x:int(strftime('%M', strptime(x['updated_time'],'%Y-%m-%dT%H:%M:%S+0000')))//10*10+10,axis=1)
# dfPost_complete['date'] = dfPost_complete.apply(lambda x:strftime('%Y-%m-%d', strptime(x['created_time'],'%Y-%m-%dT%H:%M:%S+0000')),axis=1)
# dfPost_complete['time']=dfPost_complete.apply(lambda x:str(x['hour'])+":"+str(x['minute']),axis=1)
# df = dfPost_complete.groupby([['day','time']])
# print df
# df['time'] = dfPost_complete['time']
# df['count'] = 1
# print df
# g10 = df.groupby([pd.Grouper(freq='30M',key='time')]).sum()
# print g10


# print df.groupby(['day'], sort=True).count()
# print df.sort_values(by =['month', 'day','hour','minute','created_time'])
# postsByDay = df.day.value_counts()
# print postsByDay


# dfPivote = dfPost_complete[['created_time','id_post']]
# print dfPivote.head()

# dfLike = dfLike_complete.groupby(['id_post']).count()
# print dfLike
# dfComment = dfComment_complete.groupby(['id_post']).count()
# print dfComment.head()
# frames =[dfPivote, dfLike, dfComment]
# result = pd.concat(frames)
# print result.head()
# hour=["00:30",
# "00:40",
# "00:50",
# "01:50",
# "01:60",
# "02:10",
# "02:20",
# "02:30",
# "02:40", 
# "02:50",
# "02:60",
# "03:10",
# "03:20",
# "03:30",
# "03:40",
# "03:50",
# "03:60"]


# frec=[2,
# 1,
# 1,
# 1,
# 2,
# 1,
# 1,
# 2,
# 3,
# 4,
# 3,
# 2,
# 2,
# 1,
# 0,
# 0,
# 0]

# x=range(0,17)
# plt.xticks(x, hour,rotation='vertical')
# plt.plot(x, frec)
# #df.groupby(['time']).count()['userID'].plot(kind="line")
# plt.ylabel('Post Frecuency')
# plt.xlabel('Time')
# plt.title('Argentina vs Chile')
# plt.plot(x,frec)
# plt.show()