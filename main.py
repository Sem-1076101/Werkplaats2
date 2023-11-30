from flask import Flask, session, render_template, redirect, request, url_for
from flask import request
from wtforms import Form, StringField
import sqlite3

app = Flask(__name__)

# Locatie van het database bestand
# database_file = "databases/testgpt.db"
# # Maak verbinding met het database bestand
# conn = sqlite3.connect(database_file)   
# # Maak een cursor object waarmee je SQL statements kan uitvoeren
# c = conn.cursor()
# # Voer een SQL statement uit
# result = c.execute("SELECT count(*) FROM teachers")
# # Nu niet nodig, maar stel dat dit een UPDATE statement was, dan had je nu moeten committen
# # conn.commit()
# number_of_teachers = result.fetchone()[0]  
# print(f"Er zijn {number_of_teachers} docenten in de database")
# # Sluit de verbinding met de database, is netjes, moet niet
# conn.close()

# class RegisterForm(Flaskform):
    # username = StringField(validators=[InputRequired(), Length(min=4, max=20)])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    username = request.args.get('gebruikersnaam', '')
    password = request.args.get('password', '')
    return render_template('/login.html')


@app.route('/login_check', methods = ['POST'])
def login_check():
    username = request.form['username']
    password = request.form['password']


    return redirect(url_for('app.index'))

if __name__ == '__main__':
    app.run(debug=True)




    # firstName = request.args.get('firstName', '')
    # lastName = request.args.get('lastName', '')
    # yearsOnSchool = request.args.get('yearsOnSchool', '')
    # dateOfBirth = request.args.get('dateOfBirth', '')
    # email = request.args.get('email', '')
    # password = request.args.get('password', '')
    # print(firstName)
    # print(lastName)
    # print(yearsOnSchool)
    # print(dateOfBirth)
    # print(email)
    # print(password)
    # return render_template('hello_world.html')