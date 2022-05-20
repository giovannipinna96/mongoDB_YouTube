import pymongo as pm

client = pm.MongoClient()

# create db
mydb = client['youtube']



def insert_video(data_video):
    mycollection = mydb['video']
    for i in range(len(data_video)):
        mycollection.insert_one(data_video.iloc[i].to_dict())

    mycollection.create_index(('video_id'), unique=True)
    mycollection.create_index([('title', pm.TEXT), ('channel_title', pm.TEXT)])


def insert_comment(dict_comments):
    mycollection = mydb['comment']
    for k in dict_comments:
        page = 1
        for i, com in enumerate(dict_comments[k]):
            if (i % 100) == 0 and i != 0:
                page = page + 1
            mycollection.update_one(
                {u'video_id': k,
                 u'page': page,
                 u'c': {u'$lt': 100}},
                {u'$inc': {u'c': 1},
                 u'$push': {u'comments': {u'text': com[0], u'likes': com[1]},
                            }
                 },
                upsert=True)

    mycollection.create_index([('video_id', 1), ('page', pm.ASCENDING)], unique=True)


def insert_tags(tag: dict):
    mycollection = mydb['tag']
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

    mycollection.create_index([('tag', pm.TEXT)])
