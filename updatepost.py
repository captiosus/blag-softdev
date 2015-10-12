import sqlite3

def createpost(newpostid,userid,post):
    conn = sqlite3.connect('blag.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO posts(postid,userid,post) VALUES(?,?,?)',(newpostid,userid,post))
    conn.commit()
    cur.close()

def updatepost(postid,userid,post):
    conn = sqlite3.connect('blag.db')
    cur = conn.cursor()
    cur.execute('UPDATE posts SET userid = ? WHERE postid = ?',(userid,postid))
    cur.execute('UPDATE posts SET post = ? WHERE postid = ?',(post,postid))
    conn.commit()
    cur.close()

