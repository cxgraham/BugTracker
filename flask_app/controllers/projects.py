from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import user, bug, project

# CREATE 
@app.route('/projects/create', methods = ['POST', 'GET'])
def create_project():
    if request.method == 'GET':
        this_user = user.User.get_user_by_id(session['user_id'])
        return render_template('create_project.html', this_user=this_user)
    created_project = project.Project.create_project(request.form)
    if created_project:
        return redirect('/homepage')
    return redirect(request.referrer)

# READ
@app.route('/projects/view/<int:id>')
def view_project(id):
    this_project = project.Project.get_project_by_id(id)
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('view_project.html', this_project=this_project, this_user=this_user)

# UPDATE 
@app.route('/bugs/update', methods = ['POST'])
def update_project():
    data = {
        'title': request.form['title'],
        'details': request.form['details'],
        'id': request.form['projects.id']
    }
    project.Project.edit_project_by_id(data)
    return redirect('/homepage')


# DELETE
@app.route('/projects/delete/<int:id>')
def delete_project():
    project.Project.delete_project_by_id(id)
    return redirect(request.referrer)