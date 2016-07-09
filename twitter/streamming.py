from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from pymongo import MongoClient
import json

consumer_key = "mQXmG5Z5C4c2tZjMBLEq8RsB0"
consumer_secret = "kyxNPGi8mDdGeaMXYRXcqeEww7W9xOnvvWAUdnNa3s9AyJ2yNd"
access_token = "279593295-6Se1CYQayVpQvd7AJTMKkCv9AFnmMQ0egZiCihl8"
access_token_secret = "jcTP4WFJgeaNsQrVMcJFQggyv1uykj1DFaa4Yp0LQH6ff"

client = MongoClient('localhost', 27017)
db = client['twitter_db']
print("listo");
collection = db['tw_arg_usa'];

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        tweet = json.loads(data)
        print (tweet['text'])
        collection.insert(tweet)
        return True

    def on_error(self, status):
        print("error",status)
        if status_code == 420:
            #returning False in on_data disconnects the stream
            print(">>>>>>TERMINA STREAM");
            return False

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    print("stream"); 
    stream.filter(locations=[-95.412353,29.683270,-95.409370, 29.686434])#lng,lat