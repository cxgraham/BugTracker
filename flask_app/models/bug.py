from flask_app import app
from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Bug:
    db = 'bug_tracker'

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.status = data['status']
        self.priority = data['priority']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.project_id = data['project_id']
        self.project = None

    # CREATE
    @classmethod
    def create_bug(cls, data):  
        if not cls.validate_bug(data):
            return False
        query = """
        INSERT INTO bugs (title, description, status, priority, date, project_id)
        VALUES (%(title)s, %(description)s, %(status)s, %(priority)s, %(date)s, %(project_id)s)
        ;"""
        bug_id = connectToMySQL(cls.db).query_db(query, data)
        return bug_id
    
    # READ
    @classmethod
    def get_bug_by_id(cls, id):
        data = {'id': id}
        query = """
        SELECT * FROM bugs
        WHERE bugs.id = %(id)s
        ;"""
        this_bug = connectToMySQL(cls.db).query_db(query, data)
        if this_bug:
            this_bug = cls(this_bug[0])
        return this_bug

    # UPDATE
    @classmethod
    def edit_bug_by_id(cls, data): 
        if not cls.validate_bug(data):
            return False
        query = """
        UPDATE bugs
        SET title = %(title)s, description = %(description)s, status = %(status)s, priority = %(priority)s
        WHERE bugs.id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

    # DELETE 
    @classmethod
    def delete_bug_by_id(cls, id):
        data = {'id': id}
        query = """
        DELETE FROM bugs
        WHERE bugs.id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)
    

    # VALIDATE
    @staticmethod
    def validate_bug(data):
        is_valid = True
        if (data['title']) == "":
            flash('Cannot leave title blank', 'bug')
            is_valid = False
        if (data['description']) == "":
            flash('Must include details of the bug', 'bug')
            is_valid = False
        if (data['date']) == "":
            flash('Must include date of the bug','bug')
            is_valid = False
        return is_valid