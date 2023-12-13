# from flask import Flask

# @app.route('/register')
# def register():
#     return render_template('register.html')

# @app.route('/register_check', methods=['POST'])
# def register_check():
#         username = request.form['username']
#         password = request.form['password']
#         display_name = request.form['display_name']
#         # .get is voor als je een specifieke waarde wilt ophalen, 
#         # als die waarde niet bestaat word er ingevuld wat tussen de () staat.
#         is_admin = request.form.get('is_admin', 1)
#         model = UserModel(DATABASEFILE)

#         # check of gebruiker niet al bestaat
#         existing_user = model.get_user_by_username(username)
#         if existing_user:
#             # stuur de gebruiker naar de error pagina als hij iets vindt
#             return render_template('register_error.html', message='Gebruikersnaam bestaat al!')
            
#         model.create_user(display_name = display_name, username = username, password = password, is_admin = is_admin)
#         return redirect(url_for('login'))
            