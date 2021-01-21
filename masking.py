from pymongo import MongoClient
import unicodecsv as csv
from faker import Faker
from collections import defaultdict

client = MongoClient("127.0.0.1")
db=client.test.venmo

def parse_name(user):
    if not user:
        return
    return user['last_name']

def mask_name(data):
    for letter in parse_name(data['payment']['actor'])[1:]:
        letter = '*'

total = 0
for value in db.find():
    mask_name(value)
    total+=1
    print(value)
    if total >= 100000:
        break
