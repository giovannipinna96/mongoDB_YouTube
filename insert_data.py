import pymongo as pm

client = pm.MongoClient()

# create db
mydb = client['mydb_test']

# create collection
mycollection = mydb['person']


def insert_video():
    pass


def insert_comment():
    pass


def insert_tags():
    pass
