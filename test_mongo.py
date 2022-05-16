import pymongo

client = pymongo.MongoClient()

# create db
mydb = client['mydb_test']

# create collection
mycollection = mydb['person']

# insert data
datalist = [{'name': 'giovanni', 'age': 25},
            {'name': 'paola', 'age': 23},
            {'name': 'marta', 'age': 20},
            {'name': 'chiara', 'age': 14}]

x = mycollection.insert_many(datalist)

# some print
print(x.inserted_ids)
print('---' * 3)
print(client.list_database_names())
print('---' * 3)
print(mydb.list_collection_names())
print('---' * 20)

# print all documents in the collection person
for p in mycollection.find({}, {'_id': 0}):
    print(p.values())
    #print(type(p))

mydb.drop_collection('person')