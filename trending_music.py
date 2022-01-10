# Youtube Trending Music program
# Uses Youtube API to generate a database of current trending Youtube videos
# in the music category that the user can interact with
# Features:
# Add current trending Youtube videos in the Music category to an sqlite database ✓
# Print the titles of the videos to the screen
# Sort videos in the database by position, title and view count
# Select a video specifically or randomly for playback
# API_KEY = AIzaSyDvHOFGLFVTKZVALxUfelMG8rraxybZArY

import sqlite3
import random
import datetime
import webbrowser

import googleapiclient.discovery
import googleapiclient.errors

# create database
def create_database():
    with conn:
        cur.execute("""CREATE TABLE trending (
                    positions integer,
                    ids text,
                    titles text,
                    views text
                    )""")

# populate database
def populate_database(data):
    sql = "INSERT INTO trending (positions, ids, titles, views) VALUES (?, ?, ?, ?)"
    with conn:
        cur.executemany(sql, data_prep(data))

# update database
def update_database(data):
    for video in range(len(data_prep(data))):
        sql = f"UPDATE trending SET positions=?, ids=?, titles=?, views=? WHERE positions={video + 1}"
        with conn:
            cur.execute(sql, data_prep(data)[video])

def display_database():
    cur.execute("SELECT positions, titles, views FROM trending")
    for data in cur.fetchall():
        print(f"Video Position: {data[0]} || Video Title: {data[1]} || Video Views: {data[2]}")

def select_video():
    display_database()
    try:
        user_select = input("Select a video by number OR type 'random' to receive" +
                        " a random video: > ")

        if user_select != "random":
            user_select = int(user_select)
            if user_select > 10:
                raise ValueError
            cur.execute("SELECT ids, titles FROM trending WHERE positions=?", (user_select,))
            fetched_sql = cur.fetchone()
            yt_id = fetched_sql[0]
            yt_title = fetched_sql[1]
            print(f"You have selected: {yt_title}! Enjoy!")
            yt_url = f"http://www.youtube.com/watch?v={yt_id}"
            webbrowser.open(yt_url)

        elif user_select == "random":
            random_select = random.randrange(1, 11)
            cur.execute("SELECT ids, titles FROM trending WHERE positions=?", (random_select,))
            fetched_sql = cur.fetchone()
            yt_id = fetched_sql[0]
            yt_title = fetched_sql[1]
            print(f"Random selection finds: {yt_title}! Enjoy!")
            yt_url = f"http://www.youtube.com/watch?v={yt_id}"
            webbrowser.open(yt_url)

        else:
            print("That selection was incorrect. Please try again.")

    except ValueError:
        print("That selection was incorrect. Please try again.")

# call youtube api for data
def request_yt():
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey="AIzaSyDvHOFGLFVTKZVALxUfelMG8rraxybZArY")
 
    request = youtube.videos().list(
        part="snippet, statistics",
        chart="mostPopular",
        maxResults=10,
        regionCode="US",
        videoCategoryId="10",
        fields="items(id,snippet(title)),items(statistics)"
    )
    response = request.execute()
    return response

# prep data for SQL
def data_prep(data):
    video_ids, video_titles, video_views = [], [], []
    for list_items in data.values():
        for video in list_items:
            video_ids.append(video.get("id"))
            video_titles.append(video["snippet"].get("title"))
            video_views.append(video["statistics"].get("viewCount"))
    video_positions = [x for x in range(1, len(video_ids) + 1)]

    list_data = list(zip(video_positions, video_ids, video_titles, video_views))
    return list_data
    

def main():
    select_video()
    
if __name__ == "__main__":
    conn = sqlite3.connect('trending.db')
    cur = conn.cursor()
    yt_data = request_yt()
    try:
        create_database()
        populate_database(yt_data)
        print("Database populated with new data...")
    except: #sqlite3.OperationalError: table already exists
        main()