from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta
import utils, uuid

app = Flask(__name__)
@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "GET":
        return render_template('login.html', user = session.get('username'))
    else:
        username = request.form['username']
        password = request.form['password']
        error = utils.authenticate(username, password)
        if error == None:
            session['username'] = username
            session['id'] = uuid.uuid4()
            utils.newsession(session)
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes = 60);
            return redirect('/view_posts')
        else:
            print session.get('username')
            return render_template('login.html', user = session.get('username'), error = error)

@app.route('/logout')
def logout():
    if utils.checksession(session):
        session.pop('username', None)
        session.pop('id', None)
    return redirect('/view_posts')

@app.route("/view_posts", methods = ["GET","POST"])
@app.route("/", methods = ["GET","POST"])
def viewposts():
    if request.method == "GET":
        posts = utils.displayposts()
        if utils.checksession(session):
            user = session['username']
        else:
            user = None
        return render_template('view_posts.html',posts = posts, user=user)
    else:
        if utils.checksession(session):
            user=session['username']
            updatepostinput = request.form['updatepost'][0:2]
            print(updatepostinput)
            # create a post when the button "Bloginate!" is clicked
            if updatepostinput == "cr":
                 if 'username' in session:
                     post=request.form['posttext']
                     utils.createpost(user,post)
                     return redirect(url_for('viewposts'))
                 else:
                     return redirect(url_for('login'))
            # from viewposts homepage, user clicked "Write a comment"
            elif updatepostinput == "wc":
                postid = request.form['updatepost'][2:]
                post = utils.getpost(postid)
                return render_template('createcomment.html',postid = postid, user = user, post = post)
            # from the createcomments page, user submitted comment
            elif updatepostinput == "pc":
                comment = request.form['comment']
                postid = request.form['updatepost'][2:]
                utils.createcomment(postid,user,comment)
                return redirect(url_for('viewposts'))
            # from viewposts homepage, user click "Edit post"
            elif updatepostinput == "ep":
                postid = request.form['updatepost'][2:]
                post = utils.getpost(postid)
                return render_template('editpost.html',postid = postid, post = post, user = user)
            elif updatepostinput == "dp":
                postid = request.form['updatepost'][2:]
                utils.deletepost(postid)
                return redirect(url_for('viewposts'))
            elif updatepostinput == "up":
                postid = request.form['updatepost'][2:]
                print(postid)
                post = request.form['editpost']
                utils.editpost(postid,user,post)
                return redirect(url_for('viewposts'))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))

@app.route("/create_comment/<postid>",methods = ["GET","POST"])
def createcomment(postid):
    if utils.checksession(session):
        user = session.get('username')
    else:
        return redirect('/view_posts')
    if request.method == "GET":
        post = utils.getpost(postid)
        return render_template('createcomment.html',postid = post['_id'], user = post['username'], post = post['post'])
    else:
        post = request.form['comment']
        postid = request.form['updatepost']
        utils.createcomment(postid, user, post)
        return redirect('/view_posts')

@app.route("/create_account",methods = ["GET","POST"])
def createaccount():
    if request.method == "GET":
        return render_template("create_account.html", user = session.get('username'))
    else:
        username = request.form['username']
        password = request.form['password']
        utils.createuser(username,password)
        return redirect('login')

@app.route("/user/<username>")
def user_profile(username=''):
    if utils.checksession(session):
      user = session['username']
    else:
       user = None
    posts = utils.finduserposts(username)
    return render_template("profile.html", username=username, user=user, posts=posts)

if __name__ == "__main__":
    app.debug = True
    app.secret_key="Don't store this on github"
    app.run(host = '0.0.0.0', port = 5000)
