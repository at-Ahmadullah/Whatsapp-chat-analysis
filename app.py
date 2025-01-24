import streamlit as st
import preprocessor as preprocessor, helper as helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analysis")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if not uploaded_file:
    st.title("SOCIALYTICS")
    st.markdown("<h3 style='font-size: 25px;color: grey;'>Analyse your whatsapp chats here...</h3>", unsafe_allow_html=True)
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)

    if st.sidebar.button("Show Analysis"):

        #Statistics

        num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)
        st.title('Top Statistics')

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total media")
            st.title(num_media)

        with col4:
            st.header("Total links")
            st.title(num_links)

        # Monthly Timeline

        st.title('Timeline Analysis')
        timeline = helper.monthly_timeline(selected_user, df)

        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # Daily Timeline

        st.title('Daily Timeline')
        day_timeline = helper.daily_timeline(selected_user, df)

        fig, ax = plt.subplots()
        ax.plot(day_timeline['only_date'], day_timeline['message'], color='#B284BE')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        #Activity Map

        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header('Most busy day')
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='red')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most busy month')
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='blue')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        #Activity heatmap

        st.title('Timely Activity Map')
        activity_pivot = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(activity_pivot)
        st.pyplot(fig)


        #Most busy users

        col1, col2 = st.columns(2)
        
        if selected_user =='Overall':
            st.header("Most Busy Users")
            busy_users, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(busy_users.index, busy_users.values, color='orange')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

    #Word Cloud
    df_wc = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    ax.axis('off')
    st.title('Word Cloud')
    st.pyplot(fig)

    #most common df
    most_common_df = helper.most_common_words(selected_user, df)

    fig, ax = plt.subplots()
    ax.bar(most_common_df[0], most_common_df[1])
    plt.xticks(rotation='vertical')
    st.title('Most common words')
    st.pyplot(fig)

    #Emoji Analysis
    emoji_df = helper.most_common_emoji(selected_user, df)

    if len(emoji_df) != 0:
        st.title('Emoji Analysis')

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1], labels = emoji_df[0], autopct = "%0.2f")
            st.pyplot(fig)