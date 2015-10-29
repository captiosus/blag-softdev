from flask import Flask,render_template,request,session
from flask import redirect,url_for
import utils

app = Flask(__name__)
@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        error = utils.authenticate(username, password)
        if error == None:
            session['username'] = username
            posts = utils.displayposts()
            return redirect('/view_posts')
        else:
            return render_template('login.html',error = error)

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    else:
        print 'nope'
    return redirect('/view_posts')

@app.route("/view_posts", methods = ["GET","POST"])
@app.route("/", methods = ["GET","POST"])
def viewposts():
    if request.method == "GET":
        posts = utils.displayposts()
        if 'username' in session:
            user=session['username']
        else:
            user=''
        return render_template('view_posts.html', posts = posts, user=user)
    else:
        #print session.keys()
        if 'username' in session:
            user = session['username']
            # create a post when the button "Bloginate!" is clicked
            if request.form['updatepost'] == 'createpost':
                 if 'username' in session:
                     post=request.form['posttext']
                     utils.createpost(user,post)
                     return redirect(url_for('viewposts'))
                 else:
                     return "you are not logged in"
            # either edit the specific post or delete the post
            if request.form.has_key("editpost"):
                postid = request.form['editpost']
                return redirect("/edit_post/{}".format(postid))
            elif request.form.has_key("deletepost"):
                postid = request.form['updatepost']
                utils.deletepost(postid)
                return redirect(url_for('viewposts'))
            elif request.form.has_key("makecomment"):
                postid = request.form['makecomment']
                return redirect("/create_comment/{}".format(postid))
        else:
            return redirect(url_for('login'))


@app.route("/create_comment/<postid>",methods = ["GET","POST"])
def createcomment(postid):
    user = session['username']
    if request.method == "GET":
        post = utils.getpost(postid)
        return render_template('createcomment.html',postid = postid, user = user, post = post)
    else:
        post = request.form['comment']
        postid = request.form['updatepost']
        newcommentid = utils.nextcommentid(postid)
        utils.createcomment(postid,newcommentid,user,post)
        return redirect('/view_posts')


@app.route("/edit_post/<postid>",methods = ["GET","POST"])
def editpost(postid):
    user = session['username']
    if request.method == "GET":
        post = utils.getpost(postid)
        return render_template('editpost.html',postid = postid, user = user, post = post)
    else:
        post = request.form['editpost']
        postid = request.form['updatepost']
        utils.editpost(postid,user,post)
        return redirect('/view_posts')

@app.route("/create_account",methods = ["GET","POST"])
def createaccount():
    if request.method == "GET":
        return render_template("create_account.html")
    else:
        username = request.form['username']
        password = request.form['password']
        utils.createuser(username,password)
        return redirect('login')

@app.route("/user/<username>")
def user_profile(username=''):
    if username in session:
        user=session['username']
    else:
        user=''
    posts = utils.finduserposts(username)
    return render_template("profile.html", username=username, user=user, posts=posts)

if __name__ == "__main__":
    app.debug = True
    app.secret_key="Don't store this on github"
    app.run(host = '0.0.0.0', port = 5000)
