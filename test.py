import sqlite3


video_ids = ['bvWRMAU6V-c', 'jR4AG5LdKYE', 'X-NH1uUfr0U', '9g08kucPQtE', 'l6Q-Trf5pN4']

video_position = [x for x in range(1, len(video_ids) + 1)]

video_titles = ['We Don\'t Talk About Bruno (From "Encanto")', 'NBA Youngboy - Fish Scale',
'Jessica Darrow - Surface Pressure (From "Encanto"/Sing-Along)',
'Gunna & Future - pushin P (feat. Young Thug) [Official Audio]', 'Gucci Mane - Fake Friends [Official Video]']

video_views = ['5154599', '5994076', '8070999', '9956937', '2309900']

conn = sqlite3.connect('trendingtwo.db')

cursor = conn.cursor()


# cursor.execute("""CREATE TABLE trending (
#                 position integer,
#                 ids text,
#                 titles text,
#                 views text
#                 )""")

# insert_string = ', '.join('?' * len(video_ids))
data = list(zip(video_position, video_ids, video_titles, video_views))
# position = 1
# sql = f"UPDATE trending SET position=?, ids=?, titles=?, views=? WHERE position={position}"
# with conn:
#     cursor.executemany(sql, (data[position-1], ))
# for ids in video_ids:
#     cursor.execute(sql, (ids,))
# for video in range(len(video_position)):
#     sql = f"UPDATE trending SET position=?, ids=?, titles=?, views=? WHERE position={video + 1}"
#     cursor.execute(sql, data[video])

# NOTES ----------------
# TUPLE is necessary when updating one value
# other column values must be supplied when not using WHERE statement
# when iterable contains TUPLES, the ITERABLE can be supplied alone
conn.commit()