import pandas as pd
import tweepy
import json
from pymongo import *
import time

def initTweepy():

	consumer_key = "mQXmG5Z5C4c2tZjMBLEq8RsB0"
	consumer_secret = "kyxNPGi8mDdGeaMXYRXcqeEww7W9xOnvvWAUdnNa3s9AyJ2yNd"
	access_token = "279593295-6Se1CYQayVpQvd7AJTMKkCv9AFnmMQ0egZiCihl8"
	access_token_secret = "jcTP4WFJgeaNsQrVMcJFQggyv1uykj1DFaa4Yp0LQH6ff"
	

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
	return api

df = pd.read_csv("tw_ecuador_eeuu.csv")
ids = df['userID']
ids.drop_duplicates();



client = MongoClient('localhost', 27017)
db = client['timeLine_db']
timelines = db['user_ecuador_eeuu']

tam = ids.count()
print(tam);
api = initTweepy()


for index in range(0,tam):
	id_user = ids[index]
	print ("Empieza")
	print (index)
	print (id_user)
	try:
		for tweet in tweepy.Cursor(api.user_timeline, user_id=id_user,count=100).items(500):
			timelines.insert(tweet._json)
	except Exception as e:
		print (e)
	print ("Termino")

