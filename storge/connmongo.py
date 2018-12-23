# -*- coding: utf-8 -*-
from pymongo import MongoClient
client = MongoClient('localhost', 27017)

db = client.dht11
collect = db.detectdata

post = {"t": 20, "h": 50}
collect.insert_one(post)
for post in collect.find():
	print(post)
collect.update_many({"h": 50}, {
	"$set":{
		"h": 60,
		"t": 30
	}
})
print("================================")
for post in collect.find():
	print(post)
# post2 = collect.find_one({"t": 20})
# print(post2)

# collect.delete_one({"t": 20})
# print("================================")
# for post in collect.find():
# 	print(post)

# collect.delete_many({"t": 20})
# print("================================")
# for post in collect.find():
# 	print(post)