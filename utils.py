from pymongo import MongoClient
import hashlib, sqlite3
from datetime import datetime

connection = MongoClient()
db = connection['blog']

def authenticate(username,password):
    result = db.user.find({'username':username})
    if len(result) == 0:
        return "User does not exist"
    else:
        if pw['password'] != hashlib.sha224(password).hexdigest():
            return "Incorrect password"
        else:
            return True

def createuser(username,password):
    user = {}
    user['username'] = username
    user['password'] = password
    db.user.insert(user)

def createpost(newpostid,username,post):
    post = {"postid": newpostid,
            "username": username,
            "post":post}
    db.posts.insert(post)


def deletepost(postid):
    db.posts.remove( {"postid": postid} )

def editpost(postid,username,post):
    db.blog.update({'postid':postid}, {'$set':{'username':username}})
    db.blog.update({'postid':postid}, {'$set':{'post':post}})
    db.blog.update({'postid':postid}, {'$set':{'time':datetime.datetime.now()}})

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
