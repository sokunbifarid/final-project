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

# def db_execute(command):
#     if type(command) == str:
#         connection = sqlite3.connect(db_path)
#         cursor = connection.cursor()
#         data = []
#         if command[0] == "SELECT":
#             data = cursor.execute(command).fetchall()
#         else:
#            data = cursor.execute(command)
#         cursor.close()
#         return data
#     else:
#         print(f"argument passed to read from data base is not a string type. Here is what you passed: {command}")
#         return 1