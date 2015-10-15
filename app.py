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
        if utils.authenticate(username,password):
            print "authenticated"
            session['username'] = username
            posts = utils.displayposts()
            return render_template('view_posts.html',posts = posts, user=username)
        else:             
            return redirect('/login')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    else:
        print 'nope'
    return redirect(url_for('viewposts'))

@app.route("/view_posts", methods = ["GET","POST"])
@app.route("/", methods = ["GET","POST"])
def viewposts():
    if request.method == "GET":
        posts = utils.displayposts()
        if len(session.keys())!=0:
            user=session[session.keys()[0]]
        else:
            user='guest'
        return render_template('view_posts.html',posts = posts, user=user)
    else:
        if len(session.keys())!=0:
            user = session[session.keys()[0]]
            if request.form['updatepost'] == 'createpost':
                return redirect(url_for('createpost'))
            else:
                postid = request.form['updatepost']
                post = utils.getpost(postid)
                return render_template('editpost.html',user = user, post = post)
        else:
            return redirect(url_for('login'))

@app.route('/create_new', methods=['GET','POST',])
def createpost():
    if 'username' in session:
        print request.form
        post=request.form['posttext']
        newpostid=utils.nextpostid()
        utils.createpost(newpostid,user,post)
        return redirect(url_for('viewposts'))
    else:
        return "you are not logged in"
    
# not working yet
@app.route("/editpost", methods = ["GET","POST"])
def editpost():
    if len(session.keys())!=0:
        if request.method == "GET":
            user = session[session.keys()[0]]
            postid = request.form['updatepost']
            post = utils.getpost(postid)
            return render_template('editpost.html',user = user, post = post)
        ##
    else:
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.debug = True
    app.secret_key="Don't store this on github"
    app.run(host = '0.0.0.0', port = 3842)
