import matplotlib
import numpy
import time
from pymongo import MongoClient

client = MongoClient("127.0.0.1")
db=client.test

name_in_username = 0
first_name_in_username = 0
last_name_in_username = 0
email_as_username = 0

total = 0
id_to_user = {}
num_payments_per_actor = {}
num_payments_per_target = {}

device_usage_count = {}

#this is the info that looks usefull
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
	print("	note: " + data['note'])
	print("	time: " + str(data['payment']['date_completed']))
	actor = data['payment']['actor']	# sends moneys
	target = data['payment']['target']['user']	# receives moneys

	print("	actor:")
	print_user(actor)
	print("	target:")
	print_user(target)

def parse_user(user, dict):
	if not user:
		return
	global name_in_username
	global first_name_in_username
	global last_name_in_username
	global email_as_username
	global id_to_user

	id = long(user['id'])
	if not id in id_to_user:
		id_to_user[id] = user
		if user['username']:
			if user['first_name'] in user['username']:
				first_name_in_username += 1
			if user['last_name'] in user['username']:
				last_name_in_username += 1
			if user['first_name'] in user['username'] and user['last_name'] in user['username']:
				name_in_username += 1
			if '@' in user['username']:
				email_as_username += 1

def parse_key(data):
	#print_key(data)

	parse_user(data['payment']['actor'], num_payments_per_actor)
	parse_user(data['payment']['target']['user'], num_payments_per_target)

	description = data["app"]["description"]
	global device_usage_count
	if description in device_usage_count:
		device_usage_count[description] += 1
	else:
		device_usage_count[description] = 1

for value in db.venmo.find():
	parse_key(value)
	total += 1
	if total % 100000 == 0:
		print("current: " + str(total))
		time.sleep(1)
	if total >= 500000:
		break

print("Total to name_in_username ratio: " + str(name_in_username/float(len(id_to_user)) * 100) + "%")
print("Total to first_name_in_username ratio: " + str(first_name_in_username/float(len(id_to_user)) * 100) + "%")
print("Total to last_name_in_username ratio: " + str(last_name_in_username/float(len(id_to_user)) * 100) + "%")
print("Total to email as username ratio: " + str(email_as_username/float(len(id_to_user)) * 100) + "%")
print("Found unique users: " + str(len(id_to_user)))

print("Usage stats:")
for key,value in device_usage_count.iteritems():
	print("	" + key + ": " + str(value) + " (" + str(value/float(total) * 100) + "%)")