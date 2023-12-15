from flask import Flask, session, render_template, redirect, request, url_for, flash
from flask import request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
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


        session_is_admin = session.get('is_admin')
        # check of gebruiker niet al bestaat
        existing_user = model.get_user_by_username(username)
        if existing_user:
            # stuur de gebruiker naar de error pagina als hij iets vindt
            flash('Er bestaat al een account met deze gebruikersnaam!')
            if session_is_admin == 1: 
                return redirect(url_for('register'))
            else:
                return redirect(url_for('admin'))
            
        model.create_user(display_name = display_name, username = username, password = password, is_admin = is_admin)
            
        if session_is_admin == 1: 
            return redirect(url_for('login'))
        else:
            return redirect(url_for('admin'))
            
        
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
            return redirect(url_for('login'))
             

@app.route('/index')
def welcome():
    username = session.get('username')
    is_admin = session.get('is_admin')

    if username == 'admin' or is_admin == 0:
        return redirect(url_for('admin'))
    else:
        return render_template('index.html')
   

@app.route('/admin')
def admin():
    username = session.get('username')
    is_admin = session.get('is_admin')
    if not username:
        flash('U moet inloggen om deze pagina te bezoeken.')
        return redirect(url_for('login'))
    else:
        model = UserModel(DATABASEFILE)
        get_techers = model.get_all_teachers()
        return render_template('admin.html', teachers = get_techers)
    

@app.route('/nieuw_account')
def nieuw_account():
    # if is_admin == 
    return render_template('nieuwe_docent.html')   


@app.route('/docent_aanpas/<int:teacher_id>')
def docent_aanpas(teacher_id):
    is_admin = session.get('is_admin')
    model = UserModel(DATABASEFILE)
    get_teacher = model.get_teacher_by_id(teacher_id)

    if get_teacher:
        return render_template('docent_aanpas.html', teacher = get_teacher)
    else:
        flash('Er is iets fout gegaan met het ophalen van de gebruiker')
        return redirect(url_for('admin'))   

@app.route('/verwerk_aanpas_docent', methods=['POST'])
def verwerk_aanpas_docent():
    teacher_id = request.form['teacher_id']
    username = request.form['username']
    display_name = request.form['display_name']
    is_admin = request.form['is_admin']

    model = UserModel(DATABASEFILE)
    update_teacher = model.update_user(teacher_id = teacher_id, display_name =  display_name, username = username, is_admin = is_admin)

    if not update_teacher:
        flash('Docent succesvol aangepast!')
        return redirect(url_for('admin'))
    else:
        flash('Er is iets fout gegaan met het aanpassen.')
        return redirect(url_for('admin'))
    

@app.route('/verwijder_docent/<int:teacher_id>')
def verwijder_docent(teacher_id):
    is_admin = session.get('is_admin')
    model = UserModel(DATABASEFILE)
    delete_usercheck = model.delete_user(teacher_id)
    if not delete_usercheck:
        flash('Gebruiker is verwijderd.')
    else:
        flash('Er is iets fout gegaan met het verwijderen van de gebruiker.')
        return redirect(url_for('admin'))
    
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('U bent nu uitgelogd.')
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)