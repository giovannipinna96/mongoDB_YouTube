import insert_data
import managecsv

video, comments, cate, tag = managecsv.get_elaborate_data()

insert_data.insert_video(video)
insert_data.insert_tags(tag)
insert_data.insert_comment(comments)
