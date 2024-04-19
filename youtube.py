from googleapiclient.discovery import build
from pymongo import MongoClient
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import streamlit as st
import json
import re



#To connect ApiKey connection

def Api_connect():
    Api_key="AIzaSyC0n94exCeKRrpQ5wrzAf-8GWnQO0_2BWE"
    api_service_name="youtube"
    api_version="v3"

    youtube=build(api_service_name,api_version,developerKey=Api_key)

    return youtube 

youtube=Api_connect()


#To get channel Data
def get_Channel_info(channel_id):
    request=youtube.channels().list(

                    part="snippet,contentDetails,statistics",
                    id=channel_id
    )
    response=request.execute()

    for i in response['items']:
        data=dict(Channel_Name=i['snippet']['title'],
                Channel_Id=i["id"],
                Subscribers=i['statistics']['subscriberCount'],
                Views=i["statistics"]["viewCount"],
                Total_videos=i["statistics"]["videoCount"],
                Channel_Description=i["snippet"]["description"],
                playlist_id=i["contentDetails"]["relatedPlaylists"]["uploads"])
    return data



#To get video ids
def get_videos_ids(channel_id):
    video_ids=[]
    response=youtube.channels().list(id=channel_id,
                                    part='contentDetails').execute()
    playlist_Id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    next_page_Token=None


    while True:

        response1=youtube.playlistItems().list(
                                            part ='snippet',
                                            playlistId=playlist_Id,
                                            maxResults=50,
                                            pageToken=next_page_Token).execute()
        for i in range(len(response1['items'])):
            video_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
        
        next_page_Token=response1.get('nextpageToken')


        if next_page_Token is None:
            break

    return video_ids


#To get vedio information
def get_video_information(video_ids):
    
    video_data=[]
    for video_id in video_ids:
        request=youtube.videos().list(
            part="snippet,ContentDetails,statistics",
            id=video_id
        )
        response=request.execute()

        for item in response["items"]:
            data=dict(Channel_Name=item['snippet']['channelTitle'],
                    Channel_Id=item['snippet']['channelId'],
                    Video_Id=item['id'],
                    Title=item['snippet']['title'],
                    Tags=item['snippet'].get('tags'),
                    Thumbanail=item['snippet']['thumbnails'],
                    Description=item['snippet'].get('description'),
                    published_date=item['snippet']['publishedAt'],
                    Duration=item['contentDetails']['duration'],
                    views=item['statistics'].get('viewCount'),
                    Likes=item['statistics'].get('likeCount'),
                    comments=item['statistics'].get('comentCount'),
                    Favorit=item['statistics']['favoriteCount'],
                    Definition=item['contentDetails']['definition'],
                    caption=item['contentDetails']['caption']
            )

            video_data.append(data)
    return video_data


#To get comment Data 
def get_comment_info(video_ids):
    Comment_data=[]
    try:
        for video_id in video_ids:
            request=youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    maxResults=50
                )
            response=request.execute()
            
            
            for item in response['items']:
                data=dict(Comment_Id=item['snippet']['topLevelComment']['id'],
                        Video_Id=item['snippet']['topLevelComment']['snippet']['videoId'],
                        Comment_Text=item['snippet']['topLevelComment']['snippet']['textDisplay'],
                        Comment_Author=item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        Comment_published=item['snippet']['topLevelComment']['snippet']['publishedAt'])
                
                Comment_data.append(data)

                        
                
    except:
        pass 
    return Comment_data
              

#upload To MongoDb
client = MongoClient("mongodb://localhost:27017")
mydb=client["Youtubedata_Harvesting"]


def channel_details(channel_id):
    ch_details=get_Channel_info(channel_id)
    vi_ids=get_videos_ids(channel_id)
    vi_details=get_video_information(vi_ids)
    comment_details=get_comment_info(vi_ids)


    coll=mydb["channel_information"]
    coll.insert_one({"channel_Data":ch_details,
                     "video_Data":vi_details,
                     "comment_Data":comment_details})
    
    return "upload completed successfully"

#fetching the channel_details from mongodb and store t into pandas dataframe
def channels_table(channel_name_str):
    try:
        # Create a connection to the MySQL server
        auth_plugin='mysql_native_password'
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="CHARY@sri#",
            database="firstproject",
            auth_plugin='mysql_native_password'

        )

        # Create a cursor object
        mycursor = mydb.cursor()

        # Create the table if it doesn't exist
        create_query = """
        CREATE TABLE IF NOT EXISTS channels (
            channel_Name varchar(100),
            Channel_Id varchar(80),
            Subscribers bigint,
            Views bigint,
            Total_videos bigint,
            Channel_Description text,
            playlist_id varchar(100)
        )
        """
        mycursor.execute(create_query)
        mydb.commit()
        print("Table created successfully.")

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

    except mysql.connector.Error as err:
        print("Error:", err)


    single_channel_details=[]
    mydb=client["Youtubedata_Harvesting"]
    coll=mydb["channel_information"]
    for ch_data in coll.find({"channel_Data.Channel_Name": channel_name_str},{"_id":0}):
        single_channel_details.append(ch_data["channel_Data"])
    df_single_channel=pd.DataFrame(single_channel_details)


    quoted_password = quote_plus("CHARY@sri#")
    engine = create_engine(f'mysql+pymysql://root:{quoted_password}@localhost:3306/firstproject')
    df_single_channel.to_sql('channels', engine, if_exists='append', index=False)

    print("Channel Data has been Executed.....")


#creating the table for videos data
def list_to_string(tag_list):
    return ', '.join(tag_list) if isinstance(tag_list, list) else tag_list

def videos_table(channel_name_str):
    try:

        auth_plugin='mysql_native_password'
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="CHARY@sri#",
            database="firstproject",
            auth_plugin='mysql_native_password'

            )
        mycursor=mydb.cursor() 

        
            
        create_query = """
                CREATE TABLE IF NOT EXISTS videos (
                    Channel_Name VARCHAR(100),
                    channel_Id VARCHAR(100),
                    Video_Id VARCHAR(30),
                    Title VARCHAR(150),
                    Tags TEXT,
                    Thumbanail VARCHAR(255),
                    Description TEXT,
                    published_date TIMESTAMP,
                    Duration INT,
                    views BIGINT,
                    Likes BIGINT,
                    comments INT,
                    Favorit INT,
                    Definition VARCHAR(200),
                    caption VARCHAR(60)
                )
            """
        mycursor.execute(create_query)
        mydb.commit()
        print("Table 'videos' created successfully.")
    except: 
        print("Error")


    single_videos_details = []
    client = MongoClient('mongodb://localhost:27017')
    db = client["Youtubedata_Harvesting"]
    coll1 = db["channel_information"] 
    for vi_data in coll1.find({"video_Data.Channel_Name":channel_name_str},{"_id":0}):
        single_videos_details.append(vi_data["video_Data"])
    df_single_videos = pd.DataFrame(single_videos_details[0]) 

    # Ensure columns have correct data types
    if 'published_date' not in df_single_videos.columns:
        print("Error: 'published_date' column not found in the DataFrame.")
        return

    df_single_videos['published_date'] = pd.to_datetime(df_single_videos['published_date'])
    df_single_videos['views'] = df_single_videos['views'].astype(int)
    df_single_videos['Likes'] = df_single_videos['Likes'].astype(str)
    df_single_videos['comments'] = pd.to_numeric(df_single_videos['comments'], errors='coerce').astype('Int64')
    df_single_videos['Thumbanail'] = df_single_videos['Thumbanail'].apply(lambda x: json.dumps(x) if isinstance(x, dict) else x)
    df_single_videos['Thumbanail'] = df_single_videos['Thumbanail'].apply(lambda x: x[:255] if len(x) > 255 else x)
    df_single_videos['Tags'] = df_single_videos['Tags'].apply(list_to_string)


    quoted_password = quote_plus("CHARY@sri#")
    engine = create_engine(f'mysql+pymysql://root:{quoted_password}@localhost:3306/firstproject')
    df_single_videos.to_sql('videos', engine, if_exists='append', index=False)

    print("videos Data has been Executed.....")

#creating the table for comments
import pymysql
import mysql.connector

def comments_table(channel_name_str):
    try:
        auth_plugin='mysql_native_password'
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="CHARY@sri#",
            auth_plugin='mysql_native_password'
        )

        mycursor = mydb.cursor()

        mycursor.execute("USE firstproject")


        
        create_query = """
            CREATE TABLE IF NOT EXISTS comments (
                comment_Id varchar(100),
                Video_Id varchar(80),
                Comment_Text text,
                Comment_Author varchar(50),
                Comment_published varchar(255)
            )
        """
        mycursor.execute(create_query)
        mydb.commit()
        print("comment table created")

    except pymysql.Error as e:
        print(f"An error occurred: {e}")

    single_comments_details = []
    client = MongoClient('mongodb://localhost:27017')
    db = client["Youtubedata_Harvesting"]
    coll2 = db["channel_information"] 
    for comm_data in coll2.find({"channel_Data.Channel_Name":channel_name_str},{"_id":0}):
        single_comments_details.append(comm_data["comment_Data"])
    df_comment_videos=pd.DataFrame(single_comments_details[0]) 


    quoted_password = quote_plus("CHARY@sri#")

    engine = create_engine(f'mysql+pymysql://root:{quoted_password}@localhost:3306/firstproject')
    df_comment_videos.to_sql('comments', engine, if_exists='append', index=False)
    print("Data has been Executed.....")

    

#showing the tables in streamlit
def tables(Singlechannel):
    channels_table(Singlechannel)
    videos_table(Singlechannel)
    comments_table(Singlechannel)

    return "tables created successfully"     


def show_channels_table():
    channel_list=[]
    mydb=client["Youtubedata_Harvesting"]
    coll=mydb["channel_information"]
    for ch_data in coll.find({},{"_id":0,"channel_Data":1}):
        channel_list.append(ch_data["channel_Data"])
    df1=st.dataframe(channel_list)
    
    
    return df1


def show_videos_table():
    video_list = []
    db = client["Youtubedata_Harvesting"]
    coll1 = db["channel_information"]

    for vi_data in coll1.find({}, {"_id": 0, "video_Data": 1}):
        for i in range(len(vi_data["video_Data"])):
            video_list.append(vi_data["video_Data"][i])
        
    # Create DataFrame
    df2 = st.dataframe(video_list)
    
    return df2



def show_comments_table():
    Comment_list = []
    db = client["Youtubedata_Harvesting"]
    coll2 = db["channel_information"]

    for c_data in coll2.find({}, {"_id": 0, "comment_Data": 1}):
        for i in range(len(c_data["comment_Data"])):
            Comment_list.append(c_data["comment_Data"][i])

    df3 = st.dataframe(Comment_list)


    return df3



#streamlit Application
import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017")



st.title(":blue[Data Management using mongoDB and SQL]")
with st.sidebar:

    st.title(":red[Youtube data harvesting and warehousing]")
    st.header(":green[Skill Take Away]")
    st.caption(":rainbow[Pythonscripting]")
    st.caption(":rainbow[Data Extraction]")
    st.caption(":rainbow[MongoDB]")
    st.caption(":rainbow[API integration]")


    channel_id=st.text_input(":greY[Enter the Channel ID]")

    if st.button("collect and store data"):
        db = client["Youtubedata_Harvesting"]
        coll = db["channel_information"]
        ch_ids = []

        for ch_data in coll.find({}, {"_id": 0, "channel_Data.Channel_Id": 1}):
            ch_ids.append(ch_data["channel_Data"]["Channel_Id"])
        
        if channel_id in ch_ids:
            st.success("Channel Details of the given channel id is already exists")

        else:
            insert=channel_details(channel_id)
            st.success(insert)

    All_Channels=[]
    mydb=client["Youtubedata_Harvesting"]
    coll=mydb["channel_information"]
    for ch_data in coll.find({},{"_id":0,"channel_Data":1}):
        All_Channels.append(ch_data["channel_Data"]["Channel_Name"])


    Unique_channel=st.selectbox("Select cahnnel", All_Channels)

    if st.button("Migrate to sql"):
        Table=tables(Unique_channel)
        st.success(Table)

show_table = st.radio("SELECT THE TABLE FOR VIEW",("Channels","Videos","Comments"))

if show_table=="Channels":
    show_channels_table()

if show_table=="Videos":
    show_videos_table()

if show_table=="Comments":
    show_comments_table()


#SQL connection
import mysql.connector

auth_plugin='mysql_native_password'
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CHARY@sri#",
    database='firstproject',
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

mycursor.execute("USE firstproject")

Question=st.selectbox("Select Your Question",("1. All the videos and the channel name",
                                              "2. channels with most number of videos",
                                              "3. 10 most viewed videos",
                                              "4.comments in each videos",
                                              "5. videos with highest likes",
                                              "6. likes of all videos",
                                              "7. views of each channel",
                                              "8. videos published in the year of 2022",
                                              "9. average duration of all videos in each channel",
                                              "10. videos with highest number of comments"))


if Question=="1. All the videos and the channel name":
    query1 = '''select title as videos, channel_name as channelname from videos'''
    mycursor.execute(query1)
    q1 = mycursor.fetchall()  
    mydb.commit()
    df = pd.DataFrame(q1, columns=["video title", "channel name"])
    st.write(df)


elif Question=="2. channels with most number of videos":
    query2 = '''select channel_name as channelname,Total_videos as no_videos from channels order by Total_videos desc'''
    mycursor.execute(query2)
    q2 = mycursor.fetchall()  
    mydb.commit()
    df1 = pd.DataFrame(q2, columns=["channel name ", "number of videos"])
    st.write(df1)


elif Question=="3. 10 most viewed videos":
    query3 = '''select views as views,channel_name as channelname,title as videotitle from videos 
                where views is not null order by views desc limit 10'''
    mycursor.execute(query3)
    q3 = mycursor.fetchall()
    mydb.commit()
    df2 = pd.DataFrame(q3, columns=[ "channel name","views","title"])
    st.write(df2)


elif Question=="4.comments in each videos":
    query4 = '''select comments as no_comments,title as videotitle from videos where comments is not null'''
    mycursor.execute(query4)
    q4 = mycursor.fetchall()  
    mydb.commit()
    df3 = pd.DataFrame(q4, columns=[ "no of comments","channel name","videotitle"])
    st.write(df3)


elif Question=="5. videos with highest likes":
    query5 = '''select title as videotitle,channel_name as channelname, likes as likecount from videos 
                where likes is not null order by likes desc'''
    mycursor.execute(query5)
    q5 = mycursor.fetchall()  
    mydb.commit()
    df4 = pd.DataFrame(q5, columns=[ "videotitle","channel name","likecount"])
    st.write(df4)


elif Question=="6. likes of all videos":
    query6= '''select likes as likecount,title as videotitle from videos'''
    mycursor.execute(query6)
    q6 = mycursor.fetchall()  
    mydb.commit()
    df5 = pd.DataFrame(q6, columns=[ "likecount","videotitle"])
    st.write(df5)


elif Question=="7. views of each channel":
    query7= '''select channel_name as channelname,views as totalviews from channels'''
    mycursor.execute(query7)
    q7 = mycursor.fetchall()  
    mydb.commit()
    df6 = pd.DataFrame(q7, columns=[ "channel name","totalviews"])
    st.write(df6)


elif Question=="8. videos published in the year of 2022":
    query8= '''select title as video_title,published_date as videorelease,channel_name as channelname from videos 
                where extract(year from published_date)=2022'''
    mycursor.execute(query8)
    q8 = mycursor.fetchall()  
    mydb.commit()
    df7 = pd.DataFrame(q8, columns=[ "videotitle","published_date","channelname"])
    st.write(df7)


elif Question=="9. average duration of all videos in each channel":
    query9= '''select channel_name as channelname, avg(duration)as avarageduration from videos group by channel_name'''
    mycursor.execute(query9)
    q9 = mycursor.fetchall()  # Fetch the results before committing
    mydb.commit()
    df8 = pd.DataFrame(q9, columns=[ "channelname","averageduration"])
    st.write(df8)


elif Question=="10. videos with the highest number of comments":
    query10 = '''select title as videotitle, channel_name as channelname, comments as comments from videos where comments is not null 
                 order by comments desc'''
    mycursor.execute(query10)
    q10 = mycursor.fetchall()  
    mydb.commit()
    df10 = pd.DataFrame(q10, columns=["video title", "channel name", "comments"])
    st.write(df10)


