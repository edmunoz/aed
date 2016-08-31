from geopy.geocoders import Nominatim
import sys
from pymongo import *
from TweetParser import *
from FileWorker import *
import json


client = MongoClient('localhost', 27017)
db = client['timeLine_db']
collection = db['tw_chile_argentina_final_timeLine']
tweet_parser = TweetParser(fields = ['id','created_at','text'],mentionsFlag = False,
			hashtagsFlag = False,urlsFlag=False,userFlag=True,coordinatesFlag=True,placeFlag=False)

tweets_iterator = collection.find()

cont = 0
for rawTweet in tweets_iterator:
	tweet = tweet_parser.parse(rawTweet)
	cont +=1;
	print cont
	if tweet["coordinates"] and not ("country" in rawTweet):
		print rawTweet["_id"]
		geolocator = Nominatim()
		try:
			location = geolocator.reverse(str(tweet["coordinates"]['latitud'])+","+str(tweet["coordinates"]['longitud']),timeout=50)
			print location.raw['address']['country']
			collection.update(
			   { "_id": rawTweet["_id"] },
			   { "$set": { "country":  location.raw['address']['country']} }
			)
		except Exception as e:
			print "error"
		#print tweet
		line = "%s,%s,%s,%.4f,%.4f,%s"%(tweet['user']['id'], tweet['id'],tweet['created_at'], tweet["coordinates"]['latitud'], tweet["coordinates"]['longitud'], tweet['text'])
print "Fin"