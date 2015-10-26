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
    return redirect('/view_posts')

@app.route("/view_posts", methods = ["GET","POST"])
@app.route("/", methods = ["GET","POST"])
def viewposts():
    print 'in viewposts'
    if request.method == "GET":
        posts = utils.displayposts()
        if 'username' in session:
            #print session['username']
            user=session['username']
        else:
            user=''
        return render_template('view_posts.html',posts = reversed(posts), user=user)
    else:
        #print session.keys()
        if 'username' in session:
            user = session['username']
            print request.form
            # create a post when the button "Bloginate!" is clicked
            if request.form['updatepost'] == 'createpost':
                 print 'creating new post'
                 if 'username' in session:
                     post=request.form['posttext']
                     newpostid=utils.nextpostid()
                     utils.createpost(newpostid,user,post)
                     return redirect(url_for('viewposts'))
                 else:
                     return "you are not logged in"
            # either edit the specific post or delete the post
            if request.form.has_key("editpost"):
                postid = request.form['editpost']
                post = utils.getpost(postid)
                return render_template('editpost.html',postid = postid, user = user, post = post)
            elif request.form.has_key("deletepost"):
                postid = request.form['updatepost']
                utils.deletepost(postid)
                return redirect(url_for('viewposts'))
            elif request.form.has_key("makecomment"):
                postid = request.form['makecomment']
                post = utils.getpost(postid)
                return render_template('createcomment.html',postid = postid, user = user, post = post)
        else:
            return redirect(url_for('login'))
         ########
        if (False):
            if utils.is_number(request.form['updatepost'][2:]):
                updatepostinput = request.form['updatepost'][0:2]
                # from viewposts homepage, user clicked "Write a comment"
                if updatepostinput == "cc":
                    postid = request.form['updatepost']
                    postid = float(postid[2:])
                    post = utils.getpost(postid)
                    return render_template('createcomment.html',postid = postid, user = user, post = post)
                    # from the createcomments page, user submitted comment
                elif updatepostinput == "pc":
                    comment = request.form['comment']
                    postid = float(request.form['updatepost'][2:])
                    newcommentid = utils.nextcommentid(postid)
                    utils.createcomment(postid,newcommentid,user,comment)
                    return redirect(url_for('viewposts'))             
                    # from viewposts homepage, user click "Edit post"
                elif updatepostinput == "ep":
                    post = request.form['editpost']
                    postid = float(request.form['updatepost'][2:])
                    utils.editpost(postid,user,post)
                    return redirect(url_for('viewposts'))                   
                else:
                    print 'ELSE'
                    return redirect(url_for('login'))
        #########

    
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
