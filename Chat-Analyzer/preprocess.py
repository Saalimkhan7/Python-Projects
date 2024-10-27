import streamlit as st 
import numpy as np 
import seaborn as sns 
import pandas as pd 
import re 


def preprocess(data, key):

    split_formats = {
        '12hr' : '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][mM]\s-\s',
        '24hr' : '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s',
        'custom' : ''
    }
    datetime_formats = {
        '12hr' : '%m/%d/%y, %I:%M %p - ',
        '24hr' : '%m/%d/%y, %H:%M - ',
        'custom': ''
    }
    

    raw_string = ' '.join(data.split('\n')) # converting the list split by newline char. as one whole string as there can be multi-line messages
    user_msg = re.split(split_formats[key], raw_string) [1:] # splits at all the date-time pattern, resulting in list of all the messages with user names
    date_time = re.findall(split_formats[key], raw_string) # finds all the date-time patterns
    
    df = pd.DataFrame({'Date': date_time, 'user_msg': user_msg}) # exporting it to a df
        
    # converting date-time pattern which is of type String to type datetime,
    # format is to be specified for the whole string where the placeholders are extracted by the method 
    df['Date'] = pd.to_datetime(df['Date'], format=datetime_formats[key])
    
    # split user and msg 
    usernames = []
    msgs = []
    for i in df['user_msg']:
        a = re.split('([\w\W]+?):\s', i) # lazy pattern match to first {user_name}: pattern and spliting it aka each msg from a user
        if(a[1:]): # user typed messages
            usernames.append(a[1])
            msgs.append(a[2])
        else: # other notifications in the group(eg: someone was added, some left ...)
            usernames.append("Group Notification")
            msgs.append(a[0])

    # creating new columns         
    df['User'] = usernames
    df['Message'] = msgs

    # dropping the old user_msg col.
    df.drop('user_msg', axis=1, inplace=True)
    
    df = df[["Message", "Date", "User"]]
    
    df["Message"] = df["Message"].apply(lambda x: x.strip())
    
    # Extract the date without time
    df['Only date'] = pd.to_datetime(df['Date']).dt.date

    # Get only the Year
    df['Year'] = pd.to_datetime(df['Date']).dt.year

    # Get month number
    df['Month_num'] = pd.to_datetime(df['Date']).dt.month

    # Get name of month
    df['Month'] = pd.to_datetime(df['Date']).dt.month_name()

    # Get Day
    df['Day'] = pd.to_datetime(df['Date']).dt.day

    # Get name of Day
    df['Day_name'] = pd.to_datetime(df['Date']).dt.day_name()

    # Get hour
    df['Hour'] = pd.to_datetime(df['Date']).dt.hour

    # Get minutes
    df['Minute'] = pd.to_datetime(df['Date']).dt.minute

    
    
    return df










# # This function separetes the time from the date
# def get_date_and_time(string):
#     string = string.split(",")
#     date, time = string[0], string[1]
#     time = time.split("-")
#     time = time[0].strip()
    
#     return date+" "+time 

# # remove the traling "\n" and the end of each message
# def get_string(text):
#     return text.split('\n')[0]

# def preprocess(data):

#     # regex pattern to track date and time
#     pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

#     # Extract only the messages
#     messages = re.split(pattern, data)[1:]

#     # Extracting only the date/time
#     dates = re.findall(pattern, data)

#     # Create a dataframe with the extrated messages and dates
#     df = pd.DataFrame({"user_messages": messages, 
#                    "message_date": dates})
    
#     # Apply the function that separates the time from the date
#     df["message_date"] = df["message_date"].apply(
#         lambda text: get_date_and_time(text))

#     # Let's rename the "message_date" solumn to "date"
#     df.rename(columns={"message_date": "date"}, inplace=True)

#     # Separate users number/name from users message
#     users = []
#     messages = []

#     # loop through the "user_messages" column
#     for message in df["user_messages"]:

#         # Split on the regex expression match."users name or number"
#         entry = re.split('([\w\W]+?):\s', message)

#         # very this message has a name/number
#         if entry[1:]:
#             users.append(entry[1])
#             messages.append(entry[2])

#         # else it is a "Group Notification"
#         else:
#             users.append("Group Notification")
#             messages.append(entry[0])

#     # add the users and messages to new columns in he dataframe      
#     df["User"] = users
#     df["message"] = messages

#     # remove the traling "\n" and the end of each message
#     df["message"] = df["message"].apply(lambda text: get_string(text))

#     # Drop and rename columns
#     df = df.drop(columns=["user_messages"])
#     df = df[["message", "date", "User"]]
#     df = df.rename(columns={"message": "Message", 
#                             "date": "Date"})
    
    
#     # Extract the date without time
#     df['Only date'] = pd.to_datetime(df['Date']).dt.date

#     # Get only the Year
#     df['Year'] = pd.to_datetime(df['Date']).dt.year

#     # Get month number
#     df['Month_num'] = pd.to_datetime(df['Date']).dt.month

#     # Get name of month
#     df['Month'] = pd.to_datetime(df['Date']).dt.month_name()

#     # Get Day
#     df['Day'] = pd.to_datetime(df['Date']).dt.day

#     # Get name of Day
#     df['Day_name'] = pd.to_datetime(df['Date']).dt.day_name()

#     # Get hour
#     df['Hour'] = pd.to_datetime(df['Date']).dt.hour

#     # Get minutes
#     df['Minute'] = pd.to_datetime(df['Date']).dt.minute

#     return df