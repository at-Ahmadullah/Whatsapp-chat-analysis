from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    #fetch number of messages
    num_messages = df.shape[0]

    #fetch total number of words
    words = []
    for i in df['message']:
        words.extend(i.split())

    #fetch number of media messages
    num_media_messages = df[df['message']=='<Media omitted>\n']

    #fetch number of links shared
    extractor = URLExtract()
    links = []

    for m in df['message']:
        links.extend(extractor.find_urls(m))
        
    return num_messages, len(words), len(num_media_messages), len(links)

def most_busy_users(df):
    busy_users = df['user'].value_counts().head()

    new_df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return busy_users, new_df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user']!='group_notification']
    temp = temp[temp['message']!='<Media omitted>\n']

    f= open('stop_hinglish.txt','r')
    stop_words = f.read()

    def remove_stop_words(message):
        final_message = []
        for i in message.lower().split():
            if i not in stop_words:
                final_message.append(i)
        return " ".join(final_message)
    
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    
    temp = df[df['user']!='group_notification']
    temp = temp[temp['message']!='<Media omitted>\n']
    f= open('stop_hinglish.txt','r')
    stop_words = f.read()

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def most_common_emoji(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_no', 'month']).count()['message'].reset_index()
    
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    activity_pivot = df.pivot_table(index='day_name', columns='period', values='message', aggfunc = 'count').fillna(0)

    return activity_pivot