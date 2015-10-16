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
            return redirect('/view_posts')
        else:             
            return render_template('login.html',error = utils.getError())

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
            user=''
        return render_template('view_posts.html',posts = posts, user=user)
    else:
        if len(session.keys())!=0:
            user = session[session.keys()[0]]
            print request.form
            if request.form['updatepost'] == 'createpost':
                 print 'creating new post'
                 if 'username' in session:
                     post=request.form['posttext']
                     newpostid=utils.nextpostid()
                     utils.createpost(newpostid,user,post)
                     return redirect(url_for('viewposts'))
                 else:
                     return "you are not logged in"
            elif is_number(request.form['updatepost']):
                postid = request.form['updatepost']
                post = utils.getpost(postid)
                return render_template('editpost.html',postid = postid, user = user, post = post)
            else: 
                post = request.form['updatepost']
                postid = request.form['postid']
                utils.editpost(postid,user,post)
                return redirect(url_for('viewposts'))
        else:
            return redirect(url_for('login'))
    
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
    if len(session.keys())!=0:
        username = session[session.keys()[0]]
    return render_template("profile.html", username=username)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    app.debug = True
    app.secret_key="Don't store this on github"
    app.run(host = '0.0.0.0', port = 5000)
