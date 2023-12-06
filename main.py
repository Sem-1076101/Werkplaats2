from flask import Flask, session, render_template, redirect, request, url_for, flash
from flask import request
from wtforms import Form, StringField
import sqlite3
from lib.query_model import UserModel

app = Flask(__name__)
app.secret_key = 'mysecretkey'
DATABASEFILE = 'databases/testgpt.db'


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register_check', methods=['POST'])
def register_check():
        username = request.form['username']
        password = request.form['password']
        display_name = request.form['display_name']
        # .get is voor als je een specifieke waarde wilt ophalen, 
        # als die waarde niet bestaat word er ingevuld wat tussen de () staat.
        is_admin = request.form.get('is_admin', 1)
        model = UserModel(DATABASEFILE)

        # check of gebruiker niet al bestaat
        existing_user = model.get_user_by_username(username)
        if existing_user:
            # stuur de gebruiker naar de error pagina als hij iets vindt
            return render_template('register_error.html', message='Gebruikersnaam bestaat al!')
            
        model.create_user(display_name = display_name, username = username, password = password, is_admin = is_admin)
        return redirect(url_for('login'))
            


        
@app.route('/')
def login():
    return render_template('login.html')



@app.route('/login', methods=['POST'])
def login_check():
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_model = UserModel(DATABASEFILE)
        login_check = user_model.check_login(username, password)
        if login_check:
            session['username'] = username
            return redirect(url_for('welcome'))
        else:
            flash('Gebruikersnaam of wachtwoord onjuist.')
            return render_template(url_for(login))
             

@app.route('/welcome')
def welcome():
    username = session.get('username')

    if username == 'admin':
        return render_template(url_for('admin'))
    else:
        return render_template('index.html')
   

@app.route('/admin')
def admin():
    return render_template('admin.html')


if __name__ == '__main__':
    app.run(debug=True)