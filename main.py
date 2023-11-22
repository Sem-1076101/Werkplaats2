from flask import Flask, session, render_template
from flask import request

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Test Correct vragen generator'



@app.route('/login')
def login():
    username = request.args.get('gebruikersnaam', '')
    password = request.args.get('password', '')
    return render_template('/login.html')


@app.route('/login_check', methods = ['POST'])
def login_check():
    username = request.form['username']
    password = request.form['password']
    return username

if __name__ == '__main__':
    app.run()




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