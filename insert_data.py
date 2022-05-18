import pymongo as pm

client = pm.MongoClient()

# create db
mydb = client['mydb_test']

# create collection
mycollection = mydb['person']


def insert_video(data_video):
    for i in range(len(data_video)):
        mycollection.insert_one(data_video.iloc[i].to_dict())


def insert_comment(dict_comments):
    for k in dict_comments:
        page = 0
        for i, com in enumerate(dict_comments[k]):
            mycollection.update_one(
                {u'video_id': k,
                 u'page': page,
                 u'c': {u'$lt': 100}},
                {u'$inc': {u'c': 1},
                 u'$push': {u'comments': {u'text': com[0], u'likes': com[1]},
                            }
                 },
                upsert=True)
            if (i % 99) == 0:
                page = page + 1


def insert_tags(tag: dict):
    for k in tag:
        temp_list = [tag[k][0], tag[k][1], tag[k][2]]
        mycollection.insert_one({
            u'tag': k,
            u'c': 1,
            u'info_tag': [{u'video_id': temp_list[0], u'video_title': temp_list[1], u'channel': temp_list[2]}]
        })
        for i, t in enumerate(tag[k][3:]):
            mycollection.update_one(
                {u'tag': k,
                 u'c': {u'$lt': 100}},
                {u'$inc': {u'c': 1},
                 u'$push': {u'info_tag': {u'video_id': t[0], u'video_title': t[1], u'channel': t[2]}

                            }
                 },
                upsert=True)
