import sqlite3

conn = sqlite3.connect("blag.db")

cur = conn.cursor()

cur.execute('CREATE TABLE users(userid integer, username text, password text, timestamp text)')

cur.execute('CREATE TABLE posts(postid integer, username text, post text, timestamp text)')

cur.execute('CREATE TABLE comments(postid integer, commentid integer, username text, comment text, timestamp text)')

conn.commit()

