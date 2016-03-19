import json
from flask import Flask, g, redirect, url_for

app = Flask(__name__)
app.debug = True
from modules.reservations import *
from modules.centers import *

from flaskext.auth import Auth
from flaskext.auth.auth import AuthUser
auth = Auth(app)

app.secret_key = 'N4BUdSXUzHxNoO8g'


@app.before_request
def init_users():
    admin = AuthUser(username='admin')
    admin.set_and_encrypt_password('pokus')
    g.users = {'admin': admin}


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username in g.users:
            if g.users[username].authenticate(request.form['password']):
                return 'ok'
        return redirect('http://admin.volnekurty.cz/login', code=302)
    return redirect('http://admin.volnekurty.cz/login', code=302)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
