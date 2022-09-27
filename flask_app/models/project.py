from flask_app import app
from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, bug
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Project:
    db = 'bug_tracker'

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.details = data['details']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.bugs = []
    
    # CREATE
    @classmethod
    def create_project(cls, data):  
        if not cls.validate_project(data):
            return False
        query = """
        INSERT INTO projects (title, details, user_id)
        VALUES (%(title)s, %(details)s, %(user_id)s)
        ;"""
        project_id = connectToMySQL(cls.db).query_db(query, data)
        session['project_id'] = project_id
        return project_id

    # READ
    @classmethod
    def get_project_by_id(cls, project_id):
        data= {'id': project_id}
        query = """
        SELECT * FROM projects
        LEFT JOIN bugs ON projects.id = bugs.project_id
        WHERE projects.id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            project = cls(results[0])
            for this_project in results:
                bug_data = {
                    'id': this_project['bugs.id'],
                    'title': this_project['bugs.title'],
                    'description': this_project['description'],
                    'status': this_project['status'],
                    'priority': this_project['priority'],
                    'date': this_project['date'],
                    'project_id': this_project['project_id'],
                    'created_at': this_project['bugs.created_at'],
                    'updated_at': this_project['bugs.updated_at']
                }
                project.bugs.append(bug.Bug(bug_data))
        return project

    # UPDATE 
    @classmethod
    def edit_project_by_id(cls, data): 
        if not cls.validate_project(data):
            return False
        query = """
        UPDATE projects
        SET title = %(title)s, details = %(details)s
        WHERE projects.id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

    # DELETE
    @classmethod
    def delete_project_by_id(cls, id):
        data = {'id': id}
        query = """
        DELETE FROM projects
        WHERE projects.id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

    # VALIDATE
    @staticmethod
    def validate_project(data):
        is_valid = True
        if (data['title']) == "":
            flash('Cannot leave title blank', 'project')
            is_valid = False
        if (data['details']) == "":
            flash('Must include details of the project', 'project')
            is_valid = False
        return is_valid