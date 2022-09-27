from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import user, bug, project

# CREATE 
@app.route('/bugs/create', methods = ['POST', 'GET'])
def create_bug():
    if request.method == 'GET':
        this_project = project.Project.get_project_by_id(session['project_id'])
        return render_template('create_bug.html', this_project = this_project)
    created_bug = bug.Bug.create_bug(request.form)
    if created_bug:
        return redirect('/homepage')
    return redirect(request.referrer)


# READ 
@app.route('/bugs/edit/<int:id>')
def edit_bug(id):
    this_bug = bug.Bug.get_bug_by_id(id)
    this_user = user.User.get_user_by_id(session['user_id'])
    data = {'id': session['project_id']}
    this_project = project.Project.get_project_by_id(data)
    return render_template('edit_bug.html', this_bug = this_bug, this_user = this_user, this_project = this_project)


# UPDATE 
@app.route('/bugs/update', methods = ['POST'])
def update_bug():
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'status': request.form['status'],
        'priority': request.form['priority'],
        'date': request.form['date'],
        'id': request.form['bug.id']
    }
    bug.Bug.edit_bug_by_id(data)
    return redirect ('/homepage')

# DELETE
@app.route('/bugs/delete/<int:id>')
def delete_bug(id):
    bug.Bug.delete_bug_by_id(id)
    return redirect(request.referrer)
