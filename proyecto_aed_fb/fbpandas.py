import pandas as pd
import pandas.io.sql
import numpy as np
import MySQLdb as mdb
from mysql.connector import Error
from time import gmtime, strftime, strptime

server = '108.167.133.34'
db = ''

mysql_cn = mdb.connect(host='108.167.133.34', port=3306,user='connie_usr_aed',passwd='SK5CTTs8zXV9',db='connie_facebook')

query_post = 'select * from post;'
query_like = 'select * from post_like;'
query_comment = 'select * from comment;' 
dfPost = pd.read_sql(query_post, con= mysql_cn)
dfLike = pd.read_sql(query_like, con= mysql_cn)
dfComment = pd.read_sql(query_comment, con= mysql_cn)
mysql_cn.close()

dfPost['day'] = dfPost.apply(lambda x:strftime('%d', strptime(x['created_time'],'%Y-%m-%dT%H:%M:%S+0000')),axis=1)
dfPost['month'] = dfPost.apply(lambda x:strftime('%m', strptime(x['created_time'],'%Y-%m-%dT%H:%M:%S+0000')),axis=1)
dfPost['hour']= dfPost.apply(lambda x:strftime('%H', strptime(x['created_time'],'%Y-%m-%dT%H:%M:%S+0000')),axis=1)
dfPost['minute']= dfPost.apply(lambda x:int(strftime('%M', strptime(x['updated_time'],'%Y-%m-%dT%H:%M:%S+0000')))//10*10+10,axis=1)
df = dfPost[['day','shares']]
# print df
print df.groupby(['day'], sort=True).sum()
# print df.sort_values(by =['month', 'day','hour','minute'])
postsByDay = df.day.value_counts()
print " Post by days" + str(postsByDay)


df2 = dfPost[['id_post','day']]
frames = [df2,dfLike]
result = pd.concat(frames)
