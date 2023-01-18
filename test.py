import sqlite3
con = sqlite3.connect("data.db")
cur = con.cursor()

cur.execute('select tweet_url,link from main')
for data in cur.fetchall():
    print(data)
