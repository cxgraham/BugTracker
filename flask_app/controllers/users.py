from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import user

# CREATE 
@app.route('/users/register', methods=['POST'])
def register():
    created_user = user.User.create_user(request.form)
    if created_user:
        return redirect('/homepage')
    return redirect('/')


# READ 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/homepage')
def homepage():
    if 'user_id' not in session:
        return redirect('/')
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('homepage.html', this_user = this_user)

@app.route('/users/login', methods = ['POST'])
def login():
    registered_user = user.User.login(request.form)
    if registered_user:
        return redirect('/homepage')
    return redirect('/')

# UPDATE 


# DELETE
@app.route('/users/logout')
def logout():
    session.clear()
    return redirect('/')