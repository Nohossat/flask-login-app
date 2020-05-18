from flask import Flask, url_for, request, render_template, redirect
import pandas as pd 
from markupsafe import escape
import os

app = Flask(__name__)

users = {'prenom': [], 'nom': [], 'age' : [], 'username': [], 'email': [], 'pwd': []}
df = pd.DataFrame(data=users)

@app.route('/')
def sign(error=None):
    return render_template('signup.html', error=error)

@app.route('/create', methods=['POST'])
def create():
    df.loc[len(df)] = [request.form['firstname'], request.form['lastname'], request.form['age'], request.form['username'], request.form['email'], request.form['pwd']]
    return redirect(url_for('user', username=request.form['username']))

@app.route('/connect', methods=['POST'])
def connect():
    if valid_user(request.form['username_signin'], request.form['pwd_signin']):
        return redirect(url_for('user', username=request.form['username_signin']))
    return render_template('signup.html', error='L\'username n\'existe pas ou le mot de passe est erroné.')
        
@app.route('/change_pwd', methods=['POST'])
def change_pwd(): 
    user = df.loc[df['username'] == request.form['username']]
    user = {'prenom': user.values[0][0], 'nom': user.values[0][1], 'age' : user.values[0][2], 'username': user.values[0][3], 'email': user.values[0][4], 'pwd': user.values[0][5]}
    if user['pwd'] == request.form['ancien_pwd'] and len(request.form['pwd']) >= 6:
        update_user(request.form['username'], 'pwd', request.form['pwd'])
        print(df)
        return render_template('account.html', user=user, success='Mot de passe mis à jour')
    else:
        return redirect(url_for('user', username=request.form['username']))

def update_user(username, key, value):
    df[key].loc[df['username'] == username] = value

@app.route('/user/<username>')
def user(username, error=None, success=None):
    user = df.loc[df['username'] == username]
    if len(user) : 
        user_info = {'prenom': user.values[0][0], 'nom': user.values[0][1], 'age' : user.values[0][2], 'username': user.values[0][3], 'email': user.values[0][4], 'pwd': user.values[0][5]}
        return render_template('account.html', user=user_info, error=error, success=success)
    redirect(url_for('/'))
   
def valid_user(user, pwd):
    user = df.loc[(df['username'] == user) & (df['pwd'] == pwd)]
    if len(user):
        return True 
    return False

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    app.run(debug=True)