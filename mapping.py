import matplotlib
import numpy
import time
from pymongo import MongoClient

client = MongoClient("127.0.0.1")
db=client.test.venmo

id_to_user = {}
mapping = {}	# UserID1 > {UserID2: (payments)}	AKA: User1 pays UserID2
#payments = (note, time)

# sets up the ID to user dictionary
def add_user(user):
	global id_to_user
	id = long(user['id'])
	if not id in id_to_user:
		id_to_user[id] = user

def parse_key(data):
	global mapping

	if not data['payment']['target']['user']:
		return
	add_user(data['payment']['actor'])
	add_user(data['payment']['target']['user'])

	#ActorID = long(data['payment']['actor']['id'])
	#TargetID = long(data['payment']['target']['user']['id'])

	TargetID = long(data['payment']['actor']['id'])
	ActorID = long(data['payment']['target']['user']['id'])

	if ActorID in mapping:
		UserData = mapping[ActorID]
	else:
		UserData = {}
		mapping[ActorID] = UserData

	if TargetID in UserData:
		TargetData = UserData[TargetID]
	else:
		TargetData = []
		UserData[TargetID] = TargetData

	TargetData.append({
		'note': data['note'],
		'time': data['payment']['date_completed']
	})

def print_logs(key):
	user_data = id_to_user[key]
	value = mapping[key]

	print(user_data['username'] + " (" + str(user_data['id']) + "): (" + str(len(value)) + ")")
	for ID,transactions in value.iteritems():
		print("	" + str(id_to_user[ID]['username']) + " (" + str(ID) + "): (" + str(len(transactions)) + ")")
		for transaction in transactions:
			print("		" + transaction["note"].encode('utf-8') + " | " + transaction["time"].encode('utf-8'))

total = 0
for value in db.find():
	parse_key(value)
	total += 1
	if total % 100000 == 0:
		print("current: " + str(total))
		time.sleep(1)
	if total >= 700000:
		break


num_transactions_count = {}
num_unique_persons_count = {}

def inc(dict, key):
	if key in dict:
		dict[key] += 1
	else:
		dict[key] = 1

def calculate_transaction(key):
	user_data = id_to_user[key]
	value = mapping[key]

	num_transactions = 0
	for ID,transactions in value.iteritems():
		num_transactions += len(transactions)

	inc(num_transactions_count, num_transactions)
	inc(num_unique_persons_count, len(value))

for key,value in mapping.iteritems():
	calculate_transaction(key)

def print_transaction(key):
	user_data = id_to_user[key]
	value = mapping[key]

	num_transactions = 0
	for ID,transactions in value.iteritems():
		num_transactions += len(transactions)

	# Check for possible interesting notes
	"""
	for ID,transactions in value.iteritems():
		for transaction in transactions:
			if len(transaction["note"]) > 550 / num_transactions and len(transaction["note"]) < 550:	# < 550 to remove copy paste things
				print("Found possible interesting note:")
				if ID in mapping:
					print_logs(ID)
				print_logs(key)
				return
	"""

	# fancy stuffs maybe
	if num_transactions >= 20:	# 20 transactions received
		print_logs(key)
		return
	if len(value) >= 10: # 10 unique persons
		print_logs(key)
		return

for key,value in mapping.iteritems():
	print_transaction(key)

print("num_transactions_count")
for key,value in num_transactions_count.iteritems():
	print("	" + str(key) + ": " + str(value))

print("num_unique_persons_count")
for key,value in num_unique_persons_count.iteritems():
	print("	" + str(key) + ": " + str(value))