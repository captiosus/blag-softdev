from pymongo import MongoClient
import hashlib
import time

error = ""
connection = MongoClient()
db = connection['blog']

def authenticate(username,password):
    result = db.blog.find({'name':username})
    global error
    if len(result) == 0:
        error = "User does not exist"
        return False
else:
    if pw['password'] != hashlib.sha224(password).hexdigest():
        error = "Password does not match username"
        return False
else:
    db.blog.update({'name':username}, {$set:{'time':currentTime()}})
    return True

def getError():
    global error
    return  error

def currentTime():
    return (time.strftime("%m/%d/%Y")) + " " + (time.strftime("%H:%M:%S"))

def getTime(username):
    conn = sqlite3.connect("blag.db")
    c = conn.cursor()
    q = "SELECT timestamp from users WHERE username=:uname"
    c.execute(q,{"uname":username})
    result = c.fetchone()
    if result == None:
        r = "UPDATE users SET timestamp =:time WHERE username=:uname"
        c.execute(r,{"time":currentTime(),"uname":username})
        return "Never logged in before"
else:
    time = result[0]
    r = "UPDATE users SET timestamp =:time WHERE username=:uname"
    c.execute(r,{"time":currentTime(),"uname":username})
    return time;


def nextuserid():
    conn = sqlite3.connect('blag.db')
    cur = conn.cursor()
    cur.execute('SELECT MAX(userid) FROM users')
    userid = cur.fetchall()
    cur.close()
    if userid[0] is None:
        return 1
    return userid[0][0]+1

def nextpostid():
    conn = sqlite3.connect('blag.db')
    cur = conn.cursor()
    cur.execute('SELECT MAX(postid) FROM posts')
    postid = cur.fetchall()
    cur.close()
    print postid
    if postid[0][0] is None:
        return 1
    return postid[0][0]+1

def createuser(username,password):
    user = {}
    
    time = currentTime()
    db.blog.insert(
        cur.execute('INSERT INTO users(userid,username,password,timestamp) VALUES(?,?,?,?)',(newuserid,username,password,time))
        conn.commit()
        cur.close()

def createpost(newpostid,username,post):
        conn = sqlite3.connect('blag.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO posts(postid,username,post,timestamp) VALUES(?,?,?,?)',(newpostid,username,post,currentTime()))
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
        cur.execute('UPDATE posts SET timestamp = ? WHERE postid = ?',(currentTime(),postid))
        conn.commit()
        cur.close()

def displayposts():
        conn = sqlite3.connect('blag.db')
        cur = conn.cursor()
        cur.execute('SELECT postid, timestamp, post, username FROM posts')
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
        if commentid[0] is None:
        return 1
        return commentid[0]+1

def createcomment(postid,newcommentid,username,comment):
        conn = sqlite3.connect('blag.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO comments(postid,commentid,username,comment,timestamp) VALUES(?,?,?,?,?)',(postid,newcommentid,username,comment,currentTime()))
        conn.commit()
        cur.close()

def finduserposts(username):
        conn = sqlite3.connect('blag.db')
        cur = conn.cursor()
        cur.execute('SELECT postid, timestamp, post, username FROM posts where username=:uname',{"uname":username})
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


def is_number(s):
        try:
        float(s)
        return True
        except ValueError:
        return False
