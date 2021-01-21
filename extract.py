import matplotlib
import numpy
import time
from pymongo import MongoClient

client = MongoClient("127.0.0.1")
db=client.test.venmo

total = 0
for value in db.find():
	print(value)
	total += 1
	if (total > 100):
		break