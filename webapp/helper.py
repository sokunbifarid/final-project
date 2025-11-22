from flask_login import UserMixin
import sqlite3

db_path = "chess_app_database.db"
connection = []
cursor = []

def open_database():
    global connection 
    connection = sqlite3.connect(db_path)
    global cursor 
    cursor = connection.cursor()
    return cursor

def commit_database():
    global connection
    if connection:
        connection.commit()
    else:
        print("Database not connected")

def close_database():
    global connection
    if connection:
        connection.close()
    else:
        print("Database not connected")

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email
    def is_authenticated(self):
        if self.id and self.username and self.email and self.pasword:
            return True
        return False
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.id
    def get_email(self):
        return self.email
    def get_username(self):
        return self.username
