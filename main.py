from flask import Flask, session, render_template, redirect, request, url_for, flash
from flask import request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask import send_file
from flask import render_template_string
from lib.testgpt.testgpt import TestGPT
from secret import OPENAI_LICENSE

import sqlite3
from lib.query_model import UserModel

app = Flask(__name__)
app.secret_key = 'mysecretkey'
DATABASEFILE = 'databases/testgpt.db'


test_gpt = TestGPT(OPENAI_LICENSE)



is_admin = 0
is_not_admin = 1


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
            return redirect(url_for('index'))
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
    # get_notes = model.get_all_notes()
    get_notes = model.get_all_notes_by_name()

    return render_template('index.html', categories=get_categories, notes=get_notes)
    
@app.route('/vragen/<int:note_id>')
def vragen(note_id):
    teacher_id = session.get('teacher_id')
    model = UserModel(DATABASEFILE)

    get_note_by_id = model.get_note_by_id(note_id)
    print(note_id)

    get_all_questions_by_name= model.get_all_notes_and_questions_by_name(note_id)
    get_all_questions_by_id_user = model.get_all_questions_by_id_user(teacher_id, note_id)


    if not get_all_questions_by_id_user:
        flash('Er zijn geen vragen gevonden.')


    if not get_all_questions_by_name:
        flash('Er zijn geen vragen gevonden')
        
    return render_template('vragen.html', note = get_note_by_id, all_questions = get_all_questions_by_name, get_all_questions_user = get_all_questions_by_id_user)


@app.route('/genereer_vraag',  methods=['GET', 'POST'])
def genereer_vraag():
    if request.method == 'POST':
        model = UserModel(DATABASEFILE)
        question_note = request.form.get('question_note')
        print(f"Question Note: {question_note}")
        get_note_id_by_note = model.get_note_id_by_note(question_note)


        open_question = test_gpt.generate_open_question(question_note)
        print(f"Generated Question: {open_question}")
        return render_template('question_note.html', question_note=question_note, open_question=open_question, note_id = get_note_id_by_note)
    
    return render_template('question_note.html')

@app.route('/question_aanmaak_verwerk', methods = ['POST', 'GET'])
def question_aanmaak_verwerk():
    teacher_id = session.get('teacher_id')
    note_id = request.form.get('note_id')
    generated_question = request.form.get('generated_question')
    final_changed_question = request.form.get('changed_question')

    model = UserModel(DATABASEFILE)
    insert_question = model.create_question(teacher_id = teacher_id, note_id = note_id, generated_question = generated_question, final_changed_question = final_changed_question)

    if insert_question:
        flash('De question is aangemaakt!')
        return redirect(url_for('vragen', note_id = note_id))
    
    return redirect(url_for('vragen', note_id = note_id))


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

    return redirect(url_for('index'))

@app.route('/export-notes')
def export_notes():
    model = UserModel(DATABASEFILE)
    model.export_notes_to_csv()
    return send_file('exported_notes.csv', as_attachment=True)

@app.route('/search-notes', methods=['GET'])
def search_notes():
    search_query = request.args.get('search', '')
    model = UserModel(DATABASEFILE)
    search_results = model.search_notes(search_query)
    return render_template_string('{% for note in notes %}<li class="note-item"><strong class="note-title">{{ note.title }}</strong><p><strong>Bron:</strong> {{ note.note_source }}</p><p><strong>Openbaar:</strong> {{ note.is_public }}</p></li>{% endfor %}', notes=search_results)

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
    if is_admin == 1:
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
            
        model.create_user(display_name = display_name, username = username, password = password, is_admin = form_is_admin)
        
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
    
@app.route('/categorie_aanpas/<int:category_id>')
def categorie_aanpas(category_id):
    model = UserModel(DATABASEFILE)
    get_categories = model.get_categories_by_id(category_id)

    if get_categories:
        return render_template('categorie_aanpas.html', categories = get_categories)
    else: 
        flash('Er is iets fout gegaan met het ophalen van de categorie')
        return redirect(url_for('admin'))   


@app.route('/verwerk_aanpas_categorie', methods=['POST'])
def verwerk_aanpas_categorie():
    category_id = request.form['category_id']
    omschrijving = request.form['omschrijving']

    model = UserModel(DATABASEFILE)
    update_teacher = model.update_category(category_id = category_id, omschrijving = omschrijving)

    if not update_teacher:
        flash('Docent succesvol aangepast!')
        return redirect(url_for('categories'))
    else:
        flash('Er is iets fout gegaan met het aanpassen.')
        return redirect(url_for('categories'))


@app.route('/vraag_aanpas/<int:questions_id>')
def vraag_aanpas(questions_id):
    model = UserModel(DATABASEFILE)
    get_questions = model.get_questions_by_id(questions_id)

    if get_questions:
        return render_template('vraag_aanpas.html', vragen = get_questions)
    else: 
        flash('Er is iets fout gegaan met het ophalen van de vragen')
        return redirect(url_for('index'))



@app.route('/verwerk_aanpas_vraag', methods=['POST'])
def verwerk_aanpas_vragen():
    questions_id = request.form['questions_id']
    exam_question = request.form['exam_question']

    model = UserModel(DATABASEFILE)
    update_question= model.update_question(questions_id = questions_id, exam_question = exam_question)

    if not update_question:
        flash('Vraag succesvol aangepast!')
        return redirect(url_for('index'))
    else:
        flash('Er is iets fout gegaan met het aanpassen.')
        return redirect(url_for('index'))

@app.route('/verwijder_question/<int:questions_id>')
def verwijder_question(questions_id):
    model = UserModel(DATABASEFILE)

    delete_question = model.delete_question(questions_id)
    if not delete_question:
        flash('Vraag is verwijderd.')
    else:
        flash('Er is iets fout gegaan met het verwijderen')
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))
    
@app.route('/verwijder_categorie/<int:category_id>')
def verwijder_categorie(category_id):
    model = UserModel(DATABASEFILE)
    delete_category = model.delete_category(category_id)
    if not delete_category:
        flash('Categorie is verwijderd.')
    else:
        flash('Er is iets fout gegaan met het verwijderen')
        return redirect(url_for('categories'))
    
    return redirect(url_for('categories'))

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