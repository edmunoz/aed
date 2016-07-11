from pymongo import MongoClient
import json



fileName = "user_arg_euu.csv";
fd = open(fileName,mode='w')



client = MongoClient('localhost', 27017)
db = client['timeLine_db']

cursor = db.user_arg_euu.aggregate([{
	"$group" : { "_id" :"$user.id_str", "count" :{"$sum":1}}
	}])

fd.write("id_user,numTweets")
fd.write("\n")

for document in cursor:
	line = str(document["_id"]) + "," + str(document["count"])
	fd.write(line);
	fd.write("\n");



fd.close()

