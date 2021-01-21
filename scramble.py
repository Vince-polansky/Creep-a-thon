import math
import string
from pymongo import MongoClient

def atoi(str):
    ret = 0
    for i in range(len(str)):
        ret = ret * 10 + (ord(str[i]) - ord('0'))
    return ret

def list_to_str(list):
	str = ""
	for char in list:
		str += char
	return str

def scramble_id(id):
	id_list = list(id)
	id_len = len(id_list)
	new_id = ""
	i = 0
	while i <= id_len - 1:
		c1 = atoi(id_list[i])
		c2 = atoi(id_list[-i - 1])
		if c1 == 0:
			c1 = 5
		if c2 == 0:
			c2 = 8

		c = c1 % c2
		if (c == 0 or c == atoi(id_list[i])):
			c = c2 % c1
		if (atoi(id_list[i]) != 0):
			c += atoi(id_list[i]) // 2
		elif (atoi(id_list[-i - 1]) != 0):
			c += atoi(id_list[-i  -1]) // 2
		if (c > 9):
			c = 9
		new_id += chr(c + ord('0'))
		i += 1
	return (new_id)

client = MongoClient("127.0.0.1")
db=client.test.venmo

total = 0
for value in db.find():
	id = value["payment"]["actor"]["id"]
	id2 = scramble_id(id)
	if id == id2:
		print 'error'
	total += 1
	if (total > 100000):
		break
