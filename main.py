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
        form_is_admin = request.form.get('is_admin', 1)
        model = UserModel(DATABASEFILE)


        is_admin = session.get('is_admin')
        # check of gebruiker niet al bestaat
        existing_user = model.get_user_by_username(username)
        if existing_user:
            # stuur de gebruiker naar de error pagina als hij iets vindt
            if session['is_admin'] == 0: 
                flash('Er bestaat al een account met deze gebruikersnaam!')
                return redirect(url_for('admin'))
            elif is_admin == 1:
                flash('Er bestaat al een account met deze gebruikersnaam!')
                return redirect(url_for('login'))
            
        model.create_user(display_name = display_name, username = username, password = password, is_admin = form_is_admin)
            
        if session['is_admin']: 
            return redirect(url_for('admin'))
        else:
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
        
        user = user_model.get_user_by_username(username)
        if login_check:
            session['teacher_id'] = user['teacher_id']
            session['is_admin'] = user['is_admin']
            session['username'] = username
            return redirect(url_for('welcome'))
        else:
            flash('Gebruikersnaam of wachtwoord onjuist.')
            return redirect(url_for('login'))
             

@app.route('/index')
def index():
    username = session.get('username')
    is_admin = session.get('is_admin')
    teacher_id = session.get('teacher_id')

    # if username == 'admin' or is_admin == 0:
    #     return redirect(url_for('admin'))
    # else:
    model = UserModel(DATABASEFILE)
    get_categories = model.get_all_categories()
    get_notes = model.get_all_notes()
    return render_template('index.html', categories=get_categories, notes=get_notes)
    


@app.route('/save-note', methods=['POST'])
def save_note():
    title = request.form['title']
    note_source = request.form['note_source']
    is_public = request.form.get('is_public', 0) 
    teacher_id = session.get('teacher_id')
    category_id = request.form.get('category_id', 1) 
    note_content = request.form['note']

    model = UserModel(DATABASEFILE)
    model.create_note(title=title, note_source=note_source, is_public=is_public, teacher_id=teacher_id, category_id=category_id, note=note_content)

    return redirect(url_for('welcome'))

@app.route('/categories')
def categories():
    model = UserModel(DATABASEFILE)
    get_categories = model.get_all_categories()
    return render_template('categories.html', categories=get_categories)

@app.route('/save-category', methods=['POST'])
def save_category():
    description = request.form['description']
    model = UserModel(DATABASEFILE)
    model.create_category(description=description)
    return redirect(url_for('categories'))

@app.route('/admin')
def admin():
    username = session.get('username')
    is_admin = session.get('is_admin')
    teacher_id = session.get('teacher_id')
    if not username or is_admin == 1:
        flash('U moet inloggen om deze pagina te bezoeken.')
        return redirect(url_for('login'))
    else:
        model = UserModel(DATABASEFILE)
        get_techers = model.get_all_teachers()
        return render_template('admin.html', teachers = get_techers)
    

@app.route('/nieuw_account')
def nieuw_account():
    if session['is_admin'] == 0:
        return render_template('nieuwe_docent.html')   
    else:
        flash('Je hebt niet de rechten om deze pagina te bezoeken.')
        return redirect(url_for('login'))



@app.route('/register_check_admin', methods=['POST'])
def register_check_admin():
        username = request.form['username']
        password = request.form['password']
        display_name = request.form['display_name']
        # .get is voor als je een specifieke waarde wilt ophalen, 
        # als die waarde niet bestaat word er ingevuld wat tussen de () staat.
        form_is_admin = request.form.get('is_admin', 1)
        model = UserModel(DATABASEFILE)

        # check of gebruiker niet al bestaat
        existing_user = model.get_user_by_username(username)
        if existing_user:
            # stuur de gebruiker naar de error pagina als hij iets vindt
            flash('Er bestaat al een account met deze gebruikersnaam!')
            return redirect(url_for('admin'))
            
        create_user = model.create_user(display_name = display_name, username = username, password = password, is_admin = form_is_admin)
        if create_user:
            flash('Gebruiker aangemaakt')
            return redirect(url_for('admin'))
            
@app.route('/notities_admin')
def notities_admin():
    model = UserModel(DATABASEFILE)
    get_notes = model.get_all_notes()

    if get_notes:
        return render_template('admin_notities.html', note = get_notes)
    else :
        flash('Er is iets fout gegaan met het ophalen van de notities.')
        return redirect(url_for('admin'))

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