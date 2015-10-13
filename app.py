from flask import Flask,render_template,request,sessions
from flask import redirect,url_for
import utils

app = Flask(__name__)
@app.route("/", methods = ["GET","POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        if not(utils.authenticate(username,password)):              
            return redirect('/login')


if __name__ == "__main__":
    app.debug = True
    app.secret_key="Don't store this on github"
    app.run(host = '0.0.0.0', port = 5000)
