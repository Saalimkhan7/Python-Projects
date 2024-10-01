import streamlit as st
import preprocess
import re 
import stats 
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np 

st.sidebar.title("Whatsapp Chat Analyzer")

# upload a file
file = st.sidebar.file_uploader("choose a file")

# select the time format 12hr or 24hr
key = st.sidebar.radio("Time Format", ('12hr', '24hr', 'custom'))

if file is not None:
    bytes_data = file.getvalue()

    # converting the bytecode to the text-file
    data = bytes_data.decode("utf-8")

    # sending file data to the preprocessing function for further functioning
    df = preprocess.preprocess(data, key)

    # displaying the dataframe
    ## st.datframe(df)

    # get unique users 
    user_list = df["User"].unique().tolist()

    # remove the group notifications
    user_list.remove("Group Notification")

    # organize in order
    user_list.sort()

    # include overall. This is responsible for showcasing the overall chat analysis
    user_list.insert(0, "Overall")

    # select and display analysis of user
    selected_user = st.sidebar.selectbox(
        "Show analysis with respect to", user_list
    )

    st.title("WhatsApp Chat Analysis for " + selected_user)
    if st.sidebar.button("Show Analysis"):

        # getting the stats of the selected user from the stats script
        num_messages, num_words, media_ommited, links = stats.fetch_stats(
            selected_user, df
        )

        # first phase is to showcase the basic stats like number of users,
        # number of messages,number of media shared and all,
        # so for that 4 columns are required
        col_1, col_2, col_3, col_4 = st.columns(4)

        with col_1:
            st.header("Total Messages")
            st.title(num_messages)

        with col_2:
            st.header("Total Words")
            st.title(num_words)

        with col_3:
            st.header("Media Shared")
            st.title(media_ommited)

        with col_4:
            st.header("Total Links Shared")
            st.title(links)

       
# Sample function to simulate fetch_active_users function
    def fetch_active_users(df):
    # Example logic to count user activity
         active_count = df['user'].value_counts().head(10)  # Top 10 active users
    # Example dataframe for demonstration
         new_df = pd.DataFrame({'User': active_count.index, 'Activity Count': active_count.values})
         return active_count, new_df

# Sample dataframe for demonstration
df = pd.DataFrame({
    'user': ['User A', 'User B', 'User A', 'User C', 'User A', 'User B', 'User D', 'User A', 'User B', 'User C']
})

selected_user = "Overall"

if selected_user == "Overall":
    st.title("Most Active Users")
    active_count, new_df = fetch_active_users(df)  # Replace with your actual function call

    # Create the figure and axis for the bar chart
    fig, ax = plt.subplots()

    # Displaying the bar chart in the first column
    with st.sidebar:
        ax.bar(active_count.index, active_count.values)
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

    # Displaying the dataframe in the second column
    st.write("Top Active Users:")
    st.dataframe(new_df)


        # Word Cloud
    st.title("Word Cloud")

        # Get dataframe without "<Media omitted>"
    wc_df = df[df["Message"] != "<Media omitted>"]
    df_img = stats.create_word_cloud(selected_user, wc_df)
    fig, ax = plt.subplots()
    ax.imshow(df_img)
    ax.axis("off")
    st.pyplot(fig)

        # Most Common words in the chat
    most_common_df = stats.get_common_words(selected_user, wc_df)
    fig, ax = plt.subplots()
    ax.barh(most_common_df[0], most_common_df[1])
    plt.xticks(rotation="vertical")
    st.title("Most Common Words")
    st.pyplot(fig)

        # Emoji Analysis
    emoji_df = stats.get_emoji_stats(selected_user, df)
    emoji_df.columns = ["Emoji", "Count"]

    st.title("Emoji Analysis")

        # col_1, col_2 = st.columns(2)

        # with col_1:
        #     st.dataframe(emoji_df)

        # with col_2:
    emoji_count = list(emoji_df["Count"])
    per_list = [(i/sum(emoji_count))*100 for i in emoji_count]
    emoji_df["Percentage use"] = np.array(per_list).round(2)
    st.dataframe(emoji_df)

        # Monthly timeline
    st.title("Monthly Number of Messages")
    monthly_df = stats.monthly_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(monthly_df["monthly_timeline"], monthly_df["Message"])
    plt.xticks(rotation="vertical")
    plt.tight_layout()
    st.pyplot(fig)

        # Activity maps
    st.title("Activity Map")

    col_1, col_2 = st.columns(2)

    with col_1:

            st.header("Most Active Day")

            active_day = stats.week_activity_map(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(active_day.index, active_day.values, color="purple")
            plt.xticks(rotation="vertical")
            plt.tight_layout()
            st.pyplot(fig)

    with col_2:

            st.header("Most Active Month")
            active_month = stats.month_activity_map(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(active_month.index, active_month.values, color="orange")
            plt.xticks(rotation="vertical")
            plt.tight_layout()
            st.pyplot(fig)