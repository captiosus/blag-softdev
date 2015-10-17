import sqlite3
import time

error = ""
 
def authenticate(username,password):
    conn = sqlite3.connect("blag.db")
    c = conn.cursor()
    q = "SELECT password from users WHERE username=:uname"
    c.execute(q,{"uname":username})
    result = c.fetchone()
    global error
    if result == None:
        error = "Username does not exist"
        return False
    else:
        pw = result[0]
        if pw != password:
            error = "Password does not match username"
            return False
        else:
            return True

def getError():
    global error
    return  error

def currentTime():
    return (time.strftime("%d/%m/%Y")) + (time.strftime("%H:%M:%S"))

def getTime(username):
    conn = sqlite3.connect("blag.db")
    c = conn.cursor()
    q = "SELECT time from users WHERE username=:uname"
    c.execute(q,{"uname":username})
    result = c.fetchone()
    if result == None:
        r = "UPDATE users SET time = " + currentTime() + "WHERE username=:uname"
        c.execute(r,{"uname":username})
        return "Never logged in before"
    else:
        time = result[0]
        r = "UPDATE users SET time = " + currentTime()  + "WHERE username=:uname"
        c.execute(r,{"uname":username})
        return time;
        
        
    

authenticate('bloginator','softdev')

def nextuserid():
    conn = sqlite3.connect('blag.db')
    cur = conn.cursor()
    cur.execute('SELECT MAX(userid) FROM users')
    userid = cur.fetchall()
    cur.close()
    return userid[0][0]+1

def nextpostid():
    conn = sqlite3.connect('blag.db')
    cur = conn.cursor()
    cur.execute('SELECT MAX(postid) FROM posts')
    postid = cur.fetchall()
    cur.close()
    print postid
    if postid[0] is None:
        return 1
    return postid[0][0]+1

def createuser(username,password):
    conn = sqlite3.connect('blag.db')
    cur = conn.cursor()
    newuserid = nextuserid()
    cur.execute('INSERT INTO users(userid,username,password) VALUES(?,?,?)',(newuserid,username,password))
    conn.commit()
    cur.close()

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
    cur.execute('DELETE FROM comments WHERE postid=:id',{"id":postid})
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
    postscomments = []
    for post in allposts:
        postid = post[0]
        cur.execute('SELECT commentid, comment, username FROM comments WHERE postid=:id',{"id":postid})
        comments = cur.fetchall()
        comments = tuple(comments)
        post = post + comments
        postscomments.append(post)
    cur.close()
    return postscomments

def getpost(postid):
    conn = sqlite3.connect('blag.db')
    cur = conn.cursor()
    cur.execute('SELECT post FROM posts WHERE postid=:id',{"id":postid})
    post = cur.fetchone()[0]
    cur.close()
    return post

def nextcommentid(postid):
    conn = sqlite3.connect('blag.db')
    cur = conn.cursor()
    cur.execute('SELECT MAX(commentid) FROM comments WHERE postid=:id',{"id":postid})
    commentid = cur.fetchone()
    cur.close()
    print commentid
    if commentid[0] is None:
        return 1
    return commentid[0][0]+1

def createcomment(postid,newcommentid,username,comment):
    conn = sqlite3.connect('blag.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO comments(postid,commentid,username,comment) VALUES(?,?,?,?)',(postid,newcommentid,username,comment))
    conn.commit()
    cur.close()

