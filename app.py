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

@app.route("/view_posts")
@app.route("/")
def viewposts():
    posts = utils.displayposts()
    if len(session.keys())!=0:
        print 'user'
        user=session[session.keys()[0]]
    else:
        print 'guest'
        user='guest'
    return render_template('view_posts.html',posts = posts, user=user)

@app.route("/new_post", methods = ["GET","POST"])
def makenewpost():
    if 'username' in session:
        if request.method == "GET":
            return render_template('new_post.html',s = session)
        else:
            newpostid = utils.nextpostid()
            utils.createpost(newpostid,username,post)
    else:
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.debug = True
    app.secret_key="Don't store this on github"
    app.run(host = '0.0.0.0', port = 3842)
