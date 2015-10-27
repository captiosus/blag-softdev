from pymongo import MongoClient
import hashlib
from datetime import datetime

connection = MongoClient()
db = connection['blog']

def authenticate(username,password):
    result = (db.user).find_one({"username":username})
    if result == None:
        return "User does not exist"
    else:
        if result['password'] != hashlib.sha224(password).hexdigest():
            return "Incorrect password"
        else:
            return None

def createuser(username,password):
    result = db.user.find_one({"username":username})
    if result == None:
        user = {}
        user['username'] = username
        user['password'] = hashlib.sha224(password).hexdigest()
        db.user.insert(user)

def createpost(username,post):
    post = {"username": username,
            "post":post,
            "timestamp":datetime.now()}
    db.post.insert(post)


def deletepost(postid):
    db.posts.remove( {"postid": postid} )

def editpost(postid,username,post):
    db.post.update({'postid':postid}, {'$set':{'username':username}})
    db.post.update({'postid':postid}, {'$set':{'post':post}})
    db.post.update({'postid':postid}, {'$set':{'time':datetime.now()}})

def displayposts():
    allposts = db.post.find()
    postscomments = []
    for post in allposts:
        postid = post['_id']
        comments = db.comment.find({"postid":postid})
        for info in comments:
            post = post + info
        postscomments.append(post)
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
