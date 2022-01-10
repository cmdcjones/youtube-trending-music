# Youtube Trending Music program
# Uses Youtube API to generate a database of current trending Youtube videos
# in the music category that the user can interact with
# Features:
# Add current trending Youtube videos in the Music category to an sqlite database ✓
# Print the titles of the videos to the screen
# Sort videos in the database by title, rating, and view count
# Select a video specifically or randomly for playback
# API_KEY = AIzaSyDvHOFGLFVTKZVALxUfelMG8rraxybZArY

import sqlite3
import random
import datetime
import webbrowser

import googleapiclient.discovery
import googleapiclient.errors

# create database
def create_database(connection, cursor):
    with connection:
        cursor.execute("""CREATE TABLE trending (
                    positions integer,
                    ids text,
                    titles text,
                    views text
                    )""")

# populate database
def populate_database(connection, cursor, data):
    sql = "INSERT INTO trending (positions, ids, titles, views) VALUES (?, ?, ?, ?)"
    with connection:
        cursor.executemany(sql, data_prep(data))

# update database
def update_database(connection, cursor, data):
    for video in range(len(data_prep(data))):
        sql = f"UPDATE trending SET positions=?, ids=?, titles=?, views=? WHERE positions={video + 1}"
        with connection:
            cursor.execute(sql, data_prep(data)[video])

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
    update_database(conn, cur, yt_data)
    
if __name__ == "__main__":
    conn = sqlite3.connect('trending.db')
    cur = conn.cursor()
    yt_data = request_yt()
    try:
        create_database(conn, cur)
        populate_database(conn, cur, yt_data)
        print("Database populated with new data...")
    except:
        print("Database already established...")
    main()