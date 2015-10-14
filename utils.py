import sqlite3
def authenticate(username,password):
    conn = sqlite3.connect("blag.db")
    c = conn.cursor()
    q = "SELECT password from users WHERE username == %s"%username 
    c.execute(q)
    result = c.fetchall()
    return result == password
    

def createpost(newpostid,username,post):
    conn = sqlite3.connect('blag.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO posts(postid,username,post) VALUES(?,?,?)',(newpostid,username,post))
    conn.commit()
    cur.close()

def updatepost(postid,username,post):
    conn = sqlite3.connect('blag.db')
    cur = conn.cursor()
    cur.execute('UPDATE posts SET username = ? WHERE postid = ?',(username,postid))
    cur.execute('UPDATE posts SET post = ? WHERE postid = ?',(post,postid))
    conn.commit()
    cur.close()

def displayposts():
    conn = sqlite3.connect('blag.db')
    cur = conn.cursor()
    cur.execute('SELECT username, post FROM posts')
    allposts = cur.fetchall()
    cur.close()
    return allposts
