import plotly.graph_objects as go
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
        for ch in myvideo.aggregate([{'$match': {'channel_title': channel_name}},
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

        if st.button('Show video that has this tag'):
            for tg in mytag.find({'tag': tag}, {'_id': 0, 'info_tag': 1, 'c': 1}):
                for i in range(tg['c']):
                    video_id_tag = tg['info_tag'][i]['video_id']
                    video_title_tag = tg['info_tag'][i]['video_title']
                    video_channel_tag = tg['info_tag'][i]['channel']
                    st.write(
                        f'**{i}) video id youtube:** {video_id_tag} , **channel name:** {video_channel_tag}  **Title video:** {video_title_tag}')
        else:
            pass


else:
    search1 = st.selectbox('Search for : ', ('Video title', 'Channel name', 'Tag'))
    st.markdown("""## Compare""")
    c1, c2 = st.columns(2)
    if search1 == 'Video title':
        video_title1 = c1.selectbox('Video name 1 ', (t['title'] for t in myvideo.find({}, {'_id': 0, 'title': 1})))
        video_title2 = c2.selectbox('Video name 2 ', (t['title'] for t in myvideo.find({}, {'_id': 0, 'title': 1})))
        like = []
        dislike = []
        views = []
        comment_tot = []
        channel = []
        for video_selected in myvideo.find({'title': video_title1}):
            like.append(video_selected['likes'])
            dislike.append(video_selected['dislikes'])
            views.append(video_selected['views'])
            comment_tot.append(video_selected['comment_total'])
            channel.append(video_selected['channel_title'])

        for video_selected in myvideo.find({'title': video_title2}):
            like.append(video_selected['likes'])
            dislike.append(video_selected['dislikes'])
            views.append(video_selected['views'])
            comment_tot.append(video_selected['comment_total'])
            channel.append(video_selected['channel_title'])

            st.markdown('## Statistics with respect to the mean')
        # Row A
        a1, a2, a3 = st.columns(3)
        a1.metric(f"Video 1 in channel: {channel[0]}", video_title1)
        a2.metric("", 'VS')
        a3.metric(f"Video 2 in channel: {channel[1]}", video_title2)
        # Row B
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Like ch1 respect ch2", like[0], f'{round(((like[0] * 100) / like[1]) - 100)}%')
        b2.metric("Dislike", dislike[0], f'{round(((dislike[0] * 100) / dislike[1]) - 100)}%')
        b3.metric("Views", views[0], f'{round(((views[0] * 100) / views[1]) - 100)}%')
        b4.metric("Total comment", comment_tot[0], f'{round(((comment_tot[0] * 100) / comment_tot[1]) - 100)}%')

        g1, g2 = st.columns(2)
        fig_like = go.Figure(go.Bar(x=['video1', 'video2'], y=like, marker={'color': ['orange', 'blue']}))
        g1.plotly_chart(fig_like)
        fig_like = go.Figure(go.Bar(x=['video1', 'video2'], y=dislike, marker={'color': ['orange', 'blue']}))
        g2.plotly_chart(fig_like)
        g3, g4 = st.columns(2)
        fig_views = go.Figure(go.Bar(x=['video1', 'video2'], y=views, marker={'color': ['orange', 'blue']}))
        g3.plotly_chart(fig_views)
        fig_comments = go.Figure(
            go.Bar(x=['video1', 'video2'], y=comment_tot, marker={'color': ['orange', 'blue']}))
        g4.plotly_chart(fig_comments)
    elif search1 == 'Channel name':
        channel_name1 = c1.selectbox('Channel name 1',
                                     (ct['channel_title'] for ct in myvideo.find({}, {'_id': 0, 'channel_title': 1})))
        channel_name2 = c2.selectbox('Channel name 2',
                                     (ct['channel_title'] for ct in myvideo.find({}, {'_id': 0, 'channel_title': 1})))
        tot_like = []
        tot_dislike = []
        tot_views = []
        tot_comments = []
        for ch in myvideo.aggregate([{'$match': {'channel_title': channel_name1}},
                                     {'$group': {'_id': '$channel_title', 'tot_like': {'$sum': '$likes'},
                                                 'tot_dislike': {'$sum': '$dislikes'},
                                                 'tot_views': {'$sum': '$views'},
                                                 'tot_comments': {'$sum': '$comment_total'}
                                                 }}]):
            tot_like.append(ch['tot_like'])
            tot_dislike.append(ch['tot_dislike'])
            tot_views.append(ch['tot_views'])
            tot_comments.append(ch['tot_comments'])
        for ch in myvideo.aggregate([{'$match': {'channel_title': channel_name2}},
                                     {'$group': {'_id': '$channel_title', 'tot_like': {'$sum': '$likes'},
                                                 'tot_dislike': {'$sum': '$dislikes'},
                                                 'tot_views': {'$sum': '$views'},
                                                 'tot_comments': {'$sum': '$comment_total'}
                                                 }}]):
            tot_like.append(ch['tot_like'])
            tot_dislike.append(ch['tot_dislike'])
            tot_views.append(ch['tot_views'])
            tot_comments.append(ch['tot_comments'])

        a1, a2, a3 = st.columns(3)
        a1.metric(f"Channel 1", channel_name1)
        a2.metric("", 'VS')
        a3.metric(f"Channel 2", channel_name2)

        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Total like", tot_like[0], f'{tot_like[0] - tot_like[1]}')
        b2.metric("Total dislike", tot_dislike[0], f'{tot_dislike[0] - tot_dislike[1]}')
        b3.metric("Total views", tot_views[0], f'{tot_views[0] - tot_views[1]}')
        b4.metric("Total comments", tot_comments[0], f'{tot_comments[0] - tot_comments[1]}')

        g1, g2 = st.columns(2)
        fig_like = go.Figure(go.Bar(x=['Channel1', 'Channel2'], y=tot_like, marker={'color': ['orange', 'blue']}))
        g1.plotly_chart(fig_like)
        fig_dislike = go.Figure(
            go.Bar(x=['Channel1', 'Channel2'], y=tot_dislike, marker={'color': ['orange', 'blue']}))
        g2.plotly_chart(fig_dislike)
        g3, g4 = st.columns(2)
        fig_views = go.Figure(
            go.Bar(x=['Channel1', 'Channel2'], y=tot_views, marker={'color': ['orange', 'blue']}))
        g3.plotly_chart(fig_views)
        fig_comments = go.Figure(
            go.Bar(x=['Channel1', 'Channel2'], y=tot_comments, marker={'color': ['orange', 'blue']}))
        g4.plotly_chart(fig_comments)

    else:
        tag1 = c1.selectbox('Tag 1', (tg['tag'] for tg in mytag.find({}, {'_id': 0, 'tag': 1})))
        tag2 = c2.selectbox('Tag 2', (tg['tag'] for tg in mytag.find({}, {'_id': 0, 'tag': 1})))
        tot_like = []
        tot_dislike = []
        tot_views = []
        tot_comments = []
        for tg in myvideo.aggregate([{'$match': {'tags': tag1}},
                                     {'$group': {'_id': tag1, 'tot_like': {'$sum': '$likes'},
                                                 'tot_dislike': {'$sum': '$dislikes'},
                                                 'tot_views': {'$sum': '$views'},
                                                 'tot_comments': {'$sum': '$comment_total'}
                                                 }}]):
            tot_like.append(tg['tot_like'])
            tot_dislike.append(tg['tot_dislike'])
            tot_views.append(tg['tot_views'])
            tot_comments.append(tg['tot_comments'])
        for tg in myvideo.aggregate([{'$match': {'tags': tag2}},
                                     {'$group': {'_id': tag2, 'tot_like': {'$sum': '$likes'},
                                                 'tot_dislike': {'$sum': '$dislikes'},
                                                 'tot_views': {'$sum': '$views'},
                                                 'tot_comments': {'$sum': '$comment_total'}
                                                 }}]):
            tot_like.append(tg['tot_like'])
            tot_dislike.append(tg['tot_dislike'])
            tot_views.append(tg['tot_views'])
            tot_comments.append(tg['tot_comments'])

        a1, a2, a3 = st.columns(3)
        a1.metric(f"Tag 1", tag1)
        a2.metric("", 'VS')
        a3.metric(f"Tag 2", tag2)

        a1, a2, a3, a4 = st.columns(4)
        a1.metric("Total like", tot_like[0], f'{round(((tot_like[0] * 100) / tot_like[1]) - 100)}%')
        a2.metric("Total dislike", tot_dislike[0], f'{round(((tot_dislike[0] * 100) / tot_dislike[1]) - 100)}%')
        a3.metric("Total views", tot_views[0], f'{round(((tot_views[0] * 100) / tot_views[1]) - 100)}%')
        a4.metric("Total comments", tot_comments[0], f'{round(((tot_comments[0] * 100) / tot_comments[1]) - 100)}%')

        g1, g2 = st.columns(2)
        fig_like = go.Figure(go.Bar(x=['tag1', 'tag2'], y=tot_like, marker={'color': ['orange', 'blue']}))
        g1.plotly_chart(fig_like)
        fig_dislike = go.Figure(go.Bar(x=['tag1', 'tag2'], y=tot_dislike, marker={'color': ['orange', 'blue']}))
        g2.plotly_chart(fig_dislike)
        g3, g4 = st.columns(2)
        fig_views = go.Figure(go.Bar(x=['tag1', 'tag2'], y=tot_views, marker={'color': ['orange', 'blue']}))
        g3.plotly_chart(fig_views)
        fig_comments = go.Figure(go.Bar(x=['tag1', 'tag2'], y=tot_comments, marker={'color': ['orange', 'blue']}))
        g4.plotly_chart(fig_comments)
