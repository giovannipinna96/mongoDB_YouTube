import pymongo as pm
import streamlit as st

# connect to local mongodb
client = pm.MongoClient()
# create db
mydb = client['youtube']
mytag = mydb['tag']
mycomment = mydb['comment']
myvideo = mydb['video']

# set page
st.set_page_config(layout='wide')

# load style.css
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# title page
st.title('YouTube search')
# add task bar
task = st.selectbox('Task: ', ('Search', 'Compare'))

if task == 'Search':
    search = st.selectbox('Search for : ', ('Video title', 'Channel name', 'Tag'))

    if search == 'Video title':
        video_title = st.selectbox('Video name', (t['title'] for t in myvideo.find({}, {'_id': 0, 'title': 1})))
        for video_selected in myvideo.find({'title': video_title}):
            like = video_selected['likes']
            dislike = video_selected['dislikes']
            views = video_selected['views']
            comment_tot = video_selected['comment_total']
            like_mean = video_selected['mean_like']
            dislike_mean = video_selected['mean_dislike']
            views_mean = video_selected['mean_view']
            comment_tot_mean = video_selected['mean_comment']
            date = video_selected['date']
            category = video_selected['category_id']
            channel = video_selected['channel_title']

            st.markdown('## Statistics with respect to the mean')
            # Row A
            a1, a2, a3 = st.columns(3)
            a1.metric("Channel", channel)
            a2.metric("Category", category)
            a3.metric("Date", f'{date}.2022')
            # Row B
            b1, b2, b3, b4 = st.columns(4)
            b1.metric("Like", like, f'{round(((like * 100) / like_mean) - 100)}%')
            b2.metric("Dislike", dislike, f'{round(((dislike * 100) / dislike_mean) - 100)}%')
            b3.metric("Views", views, f'{round(((views * 100) / views_mean) - 100)}%')
            b4.metric("Total comment", comment_tot, f'{round(((comment_tot * 100) / comment_tot_mean) - 100)}%')

        col1, col2 = st.columns([3, 1])
        col1.markdown('## Comments:')
        for t in myvideo.find({'title': video_title}, {'_id': 0, 'page_total': 1, 'video_id': 1}):
            pages = t['page_total']
            video_id = t['video_id']
        p = col2.selectbox('Page', (range(pages)))
        comm = 'not comment'
        for c in mycomment.find({'video_id': video_id, 'page': (p + 1)}, {'_id': 0, 'comments': 1}):
            for i in range(100):
                comm = c['comments'][i]['text']
                like = c['comments'][i]['likes']
                col1.markdown(f'**Comment {i + 1 * (p * 100)}, like number : {like}:**')
                col1.write(comm)

    elif search == 'Channel name':
        channel_name = st.selectbox('Channel name',
                                    (ct['channel_title'] for ct in myvideo.find({}, {'_id': 0, 'channel_title': 1})))
        st.markdown(f'## Statistics for the channel: {channel_name}')
        for ch in myvideo.aggregate([{'$match': {'channel_title': 'TMZ'}},
                                     {'$group': {'_id': '$channel_title', 'tot_like': {'$sum': '$likes'},
                                                 'tot_dislike': {'$sum': '$dislikes'},
                                                 'tot_views': {'$sum': '$views'},
                                                 'tot_comments': {'$sum': '$comment_total'}
                                                 }}]):
            tot_like = ch['tot_like']
            tot_dislike = ch['tot_dislike']
            tot_views = ch['tot_views']
            tot_comments = ch['tot_comments']

            a1, a2, a3, a4 = st.columns(4)
            a1.metric("Total like", tot_like)
            a2.metric("Total dislike", tot_dislike)
            a3.metric("Total views", tot_views)
            a4.metric("Total comments", tot_comments)



    else:
        tag = st.selectbox('Tag', (tg['tag'] for tg in mytag.find({}, {'_id': 0, 'tag': 1})))
        st.markdown(f'## Statistics for the tag: {tag}')
        for tg in myvideo.aggregate([{'$match': {'tags': tag}},
                                         {'$group': {'_id': tag, 'tot_like': {'$sum': '$likes'},
                                                     'tot_dislike': {'$sum': '$dislikes'},
                                                     'tot_views': {'$sum': '$views'},
                                                     'tot_comments': {'$sum': '$comment_total'}
                                                     }}]):
                tot_like = tg['tot_like']
                tot_dislike = tg['tot_dislike']
                tot_views = tg['tot_views']
                tot_comments = tg['tot_comments']

                a1, a2, a3, a4 = st.columns(4)
                a1.metric("Total like", tot_like)
                a2.metric("Total dislike", tot_dislike)
                a3.metric("Total views", tot_views)
                a4.metric("Total comments", tot_comments)


else:
    search1 = st.selectbox('Search for : ', ('Video title', 'Channel name', 'Tag'))
    st.markdown("""## Compare""")
    c1, c2 = st.columns(2)
    if search1 == 'Video title':
        video_title1 = c1.selectbox('Video name 1 ', ('titoli'))
        video_title2 = c2.selectbox('Video name 2 ', ('titoli'))
    elif search1 == 'Channel name':
        channel_name1 = c1.selectbox('Channel name 1', ('titoli'))
        channel_name2 = c2.selectbox('Channel name 2', ('titoli'))
    else:
        tag1 = c1.selectbox('Tag 1', ('titoli'))
        tag2 = c2.selectbox('Tag 2', ('titoli'))

#

#
# # Row C
# c1, c2 = st.columns((7,3))
# with c1:
#     st.markdown('### Heatmap')
#     plost.time_hist(
#     data=seattle_weather,
#     date='date',
#     x_unit='week',
#     y_unit='day',
#     color='temp_max',
#     aggregate='median',
#     legend=None)
# with c2:
#     st.markdown('### Bar chart')
#     plost.donut_chart(
#         data=stocks,
#         theta='q2',
#         color='company')
