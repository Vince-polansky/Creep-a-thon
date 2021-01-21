import matplotlib
import numpy
import time
from pymongo import MongoClient

client = MongoClient("127.0.0.1")
db=client.test.venmo

def print_user(user):
	if not user:
		print("		NO DATA")
		return
	print("		name: " + user['first_name'] + " " + user['last_name'])
	print("		username: " + user['username'])
	print("		picture: " + user['profile_picture_url'])
	print("		ID: " + user['id'])

def print_key(data):
	print("Key info:")
	print("	Description: " + data["app"]["description"])
	print("	note: " + data['note'].encode('utf-8'))
	print("	time: " + str(data['payment']['date_completed']))
	actor = data['payment']['actor']	# sends moneys
	target = data['payment']['target']['user']	# receives moneys

	print("	actor:")
	print_user(actor)
	print("	target:")
	print_user(target)

#for value in db.find( { "$text": { "$search": 'mail.com' } } ):
#	if ('@' in value['note'] and len(value['note']) < 50):
#		print(value['note'])

#for value in db.find( { "$text": { "$search": 'bank' } } ):
#	if (len(value['note']) < 150):
#		print(value['note'])


for value in db.find( { "$text": { "$search": '2061363220316160906' } } ):
	print_key(value)

#print(db.find( { "$text": { "$search": 'pizza' } } ).count())