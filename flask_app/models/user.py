from flask_app import app
from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import bug, project
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re

class User:
    db = 'bug_tracker'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.projects = []
    

    # CREATE 
    @classmethod
    def create_user(cls, data):
        if not cls.validate_user(data):
            return False
        data = cls.parse_registration_data(data)
        query = """
        INSERT INTO users (first_name, email, password)
        VALUES (%(first_name)s, %(email)s, %(password)s)
        ;"""
        user_id = connectToMySQL(cls.db).query_db(query, data)
        session['user_id'] = user_id
        return user_id


    # READ
    @classmethod
    def get_user_by_email(cls, email):
        data= {'email': email}
        query = """
        SELECT * FROM users WHERE email = %(email)s
        ;"""
        this_user = connectToMySQL(cls.db).query_db(query, data)
        if this_user:
            this_user = cls(this_user[0])
        return this_user

    @classmethod
    def get_user_by_id(cls, user_id):
        data= {'id': user_id}
        query = """
        SELECT * FROM users
        LEFT JOIN projects ON users.id = projects.user_id
        WHERE users.id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            user = cls(results[0])
            for this_user in results:
                project_data = {
                    'id': this_user['projects.id'],
                    'title': this_user['title'],
                    'details': this_user['details'],
                    'user_id': this_user['user_id'],
                    'created_at': this_user['projects.created_at'],
                    'updated_at': this_user['projects.updated_at']
                }
                user.projects.append(project.Project(project_data))
        return user

    # UPDATE 




    # DELETE



    # VALIDATE
    @staticmethod
    def validate_user(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email address', 'register')
            is_valid = False
        if User.get_user_by_email((data['email']).lower()):
            flash('Email is already in use', 'register')
        if len(data['first_name']) < 2:
            flash('First name must be at least two characters', 'register')
            is_valid = False
        if len(data['password']) < 5:
            flash('Password must be at least five characters','register')
            is_valid = False
        if (data['password']) != (data['confirm_password']):
            flash('Password does not match', 'register')
            is_valid = False
        return is_valid
    
    @staticmethod
    def parse_registration_data(data):
        parsed_data = {}
        parsed_data['email'] = data['email'].lower()
        parsed_data['password'] = bcrypt.generate_password_hash(data['password'])
        parsed_data['first_name'] = data['first_name']
        return parsed_data
    
    @staticmethod
    def login(data):
        this_user = User.get_user_by_email(data['email'].lower())
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                return True
        flash('Your login info is incorrect', 'login')
        return False
