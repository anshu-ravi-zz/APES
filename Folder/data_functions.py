import pandas as pd

def remove_short_comments(data, min_words):
    nwords = []
    for i in range(data['comment'].count()):
        nwords.append(len(data['comment'][i].split()))
    data['wordcount'] = nwords
    data.drop(data[data['wordcount'] < min_words].index, inplace=True)
    return data

def count_comments(data):
    data = data.groupby(['student'])['comment'].count()
    data = data.to_frame().reset_index()
    data.columns = ['student', 'num_comments']
    return data


def get_zoom_data(filename='zoom_chat.txt', min_words=2):
    zoom_chat = pd.read_csv(filename, 
                sep='\t', 
                encoding='latin-1',
                names=['time', 'student', 'comment'])
    zoom_chat['student'] = zoom_chat['student'].replace(':', '', regex=True)

    long_comments_only = remove_short_comments(zoom_chat, min_words)
    comment_df = count_comments(long_comments_only)

    return comment_df


def get_adobe_data(filename='CHAT.csv', min_words=2):
    adobe_chat = pd.read_csv(filename,
                sep=":",
                encoding='latin-1',
                names=["student", "comment"],
                keep_default_na=False,
                skipinitialspace=True,
                comment='"')

    long_comments_only = remove_short_comments(adobe_chat, min_words)
    comment_df = count_comments(long_comments_only)

    return comment_df

def get_student_names(comment_df):
    return list(comment_df['student'])