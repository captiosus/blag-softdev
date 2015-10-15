import sqlite3
def authenticate(username,password):
    conn = sqlite3.connect("blag.db")
    c = conn.cursor()
    q = "SELECT password from users WHERE username=:uname" 
    c.execute(q,{"uname":username})
    result = c.fetchone()[0]
    return result == password

authenticate('bloginator','softdev')

def nextpostid():
    conn = sqlite3.connect('blag.db')
    cur = conn.cursor()
    cur.execute('SELECT MAX(postid) FROM posts')
    postid = cur.fetchall()
    cur.close()
    return postid[0][0]+1

def createpost(newpostid,username,post):
    conn = sqlite3.connect('blag.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO posts(postid,username,post) VALUES(?,?,?)',(newpostid,username,post))
    conn.commit()
    cur.close()

def deletepost(postid):
    conn = sqlite3.connect('blag.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM posts WHERE postid=:id',{"id":postid})
    conn.commit()
    cur.close()

def editpost(postid,username,post):
    conn = sqlite3.connect('blag.db')
    cur = conn.cursor()
    cur.execute('UPDATE posts SET username = ? WHERE postid = ?',(username,postid))
    cur.execute('UPDATE posts SET post = ? WHERE postid = ?',(post,postid))
    conn.commit()
    cur.close()

def displayposts():
    conn = sqlite3.connect('blag.db')
    cur = conn.cursor()
    cur.execute('SELECT postid, post, username FROM posts')
    allposts = cur.fetchall()
    cur.close()
    return allposts

def getpost(postid):
    conn = sqlite3.connect('blag.db')
    cur = conn.cursor()
    cur.execute('SELECT post FROM posts')
    post = cur.fetchone()[0]
    cur.close()
    return post
