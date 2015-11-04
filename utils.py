from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib
from datetime import datetime
from bson.objectid import ObjectId

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
    db.comment.delete_many({"postid": str(postid)})
    db.post.remove( {"_id":ObjectId(postid)} )

def editpost(postid,username,post):
    db.post.update({'_id':ObjectId(postid)}, {'$set':{'username':username, 'post':post, 'timestamp':datetime.now()}})

def displayposts():
    allposts = db.post.find({'$query': {}, '$orderby': {'timestamp':-1}})
    postscomments = []
    for post in allposts:
        postid = post['_id']
        comments = commentsbyid(postid)
        post['comment'] = comments
        postscomments.append(post)
    return postscomments

def getpost(postid):
    post = db.post.find_one({"_id": ObjectId(postid)});
    return post["post"];

def commentsbyid(postid):
    postcomments = db.comment.find({"postid": str(postid)})
    return postcomments

def createcomment(postid,username,comment):
    comment = {"username": username,
               "postid":postid,
               "comment":comment,
               "timestamp":datetime.now()}
    db.comment.insert(comment)

def finduserposts(username):
    userposts = db.post.find({'$query': {"username": username}, '$orderby': {'timestamp':-1}})
    postscomments = []
    for post in userposts:
        postid = post['_id']
        comments = commentsbyid(postid)
        post['comment'] = comments
        postscomments.append(post)
    return postscomments

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def newsession(session):
    db.session.insert( {"username":session['username'], "id":session['id']} )

def checksession(session):
    if 'username' in session and 'id' in session:
        results = db.session.find( {'username':session['username'], 'id':session['id']} )
    else:
        return False
    return results.count() > 0

def deletesession(session):
    db.session.remove( {"username":session['username'], "id": sesion['id']} )
