import sys
from pymongo import *
from TweetParser import *
from FileWorker import *
import json

fileName = "tw_ecuador_eeuu.csv"

client = MongoClient('localhost', 27017)
db = client['twitter_db']
collection = db['tw_ecuador_eeuu']

tweets_iterator = collection.find()

tweet_parser = TweetParser(fields = ['id','created_at','text'],mentionsFlag = False,
			hashtagsFlag = False,urlsFlag=False,userFlag=True,coordinatesFlag=True,placeFlag=False)

lines = []
lines.append("userID,id,created_at,lat,lng")

for rawTweet in tweets_iterator:
	tweet = tweet_parser.parse(rawTweet)
	if tweet["coordinates"]:
		#line = "%s,%s,%s,%.4f,%.4f,%s"%(tweet['user']['id'], tweet['id'],tweet['created_at'], tweet["coordinates"]['latitud'], tweet["coordinates"]['longitud'], tweet['text'])
		line = "%s,%s,%s,%.4f,%.4f"%(tweet['user']['id'], tweet['id'],tweet['created_at'], tweet["coordinates"]['latitud'], tweet["coordinates"]['longitud'])
		lines.append(line)


worker = FileWorker()
worker.write(fileName,lines)