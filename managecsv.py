import pandas as pd


def load_data(path_video: str = './trending_youtube_video_statistics_and_comments/USvideos.csv',
              path_comments: str = './trending_youtube_video_statistics_and_comments/UScomments.csv',
              path_category: str = './trending_youtube_video_statistics_and_comments/US_category_id.json'):
    data_video = pd.read_csv(path_video, error_bad_lines=False)
    data_comments = pd.read_csv(path_comments, error_bad_lines=False)
    data_category = pd.read_json(path_category)

    return data_video, data_comments, data_category


def clean_comments(data_comments):
    return data_comments.drop('replies', axis=1)


def clean_category(data_category):
    dict_category = {}
    for i in range(len(data_category)):
        dict_category.update({data_category['items'].iloc[i]['id']: data_category['items'].iloc[i]['snippet']['title']})

    return dict_category


def create_tags(data_video):
    tags = data_video.copy()
    tags.drop(['category_id', 'views', 'likes', 'dislikes', 'comment_total', 'thumbnail_link', 'date'], inplace=True,
              axis=1)
    tags.tags = tags.tags.apply(lambda x: x.split('|'))
    tags = tags.drop_duplicates()
    d = {}
    for idx, ts in enumerate(tags['tags']):
        for t in ts:
            if t in d:
                d[t].append(list(tags[['video_id', 'title', 'channel_title']].iloc[idx]))
            else:
                temp = [tags['video_id'].iloc[idx], tags['title'].iloc[idx], tags['channel_title'].iloc[idx]]
                d.update({t: temp})

    return d


def num_to_category(data_video, dict_category):
    for i in range(len(data_video.category_id)):
        if str(data_video.category_id.iloc[i]) in dict_category:
            data_video.category_id.iloc[i] = dict_category.get(str(data_video.category_id.iloc[i]))
        else:
            data_video.category_id.iloc[i] = None

    return data_video


def calculate_mean_like(data_video):
    for author in data_video['channel_title']:
        data_video.mean_like[data_video['channel_title'] == author] = data_video.mean_like[
            data_video['channel_title'] == author].fillna(
            round(data_video.likes[data_video['channel_title'] == author].mean()))
    return data_video


def calculate_mean_dislike(data_video):
    for author in data_video['channel_title']:
        data_video.mean_dislike[data_video['channel_title'] == author] = data_video.mean_dislike[
            data_video['channel_title'] == author].fillna(
            round(data_video.dislikes[data_video['channel_title'] == author].mean()))
    return data_video


def calculate_mean_view(data_video):
    for author in data_video['channel_title']:
        data_video.mean_view[data_video['channel_title'] == author] = data_video.mean_view[
            data_video['channel_title'] == author].fillna(
            round(data_video.views[data_video['channel_title'] == author].mean()))
    return data_video


def calculate_mean_comments(data_video):
    for author in data_video['channel_title']:
        data_video.mean_comment[data_video['channel_title'] == author] = data_video.mean_comment[
            data_video['channel_title'] == author].fillna(
            round(data_video.comment_total[data_video['channel_title'] == author].mean()))
    return data_video


def create_analytics_col(data_video):
    data_video['mean_like'] = None
    data_video['mean_dislike'] = None
    data_video['mean_view'] = None
    data_video['mean_comment'] = None

    return data_video


def drop_duplicates_video(data):
    return data.drop_duplicates(subset=['video_id'], keep='last', inplace=True)


def get_elaborate_data(path_video: str = './trending_youtube_video_statistics_and_comments/USvideos.csv',
                       path_comments: str = './trending_youtube_video_statistics_and_comments/UScomments.csv',
                       path_category: str = './trending_youtube_video_statistics_and_comments/US_category_id.json'):
    data_video, data_comments, data_category = load_data(path_video, path_comments, path_category)
    data_comments = clean_comments(data_comments)
    dict_category = clean_category(data_category)
    data_video.drop_duplicates(subset=['video_id'], keep='last', inplace=True)
    data_tags = create_tags(data_video)
    data_video = create_analytics_col(data_video)
    data_video = calculate_mean_comments(data_video)
    data_video = calculate_mean_view(data_video)
    data_video = calculate_mean_like(data_video)
    data_video = calculate_mean_dislike(data_video)
    data_video = num_to_category(data_video, dict_category)
    data_video['tags'] = data_video.tags.apply(lambda x: x.split('|'))

    return data_video, data_comments, dict_category, data_tags
