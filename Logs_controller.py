from datetime import datetime, timezone


import Blogs_controller
from DBconnection import database
def log(space_type_id, event_type_id, login):
    with database.logs_db:
        cursor = database.get_logs_cursor()
        time = datetime.now().isoformat()
        user_id = Blogs_controller.get_user_id(login)
        cursor.execute("INSERT INTO logs (datetime, user_id, space_type_id, event_type_id) VALUES ( ?, ?, ?, ?)", ( time, user_id, space_type_id, event_type_id ))
def log_login(login):
    log(3,1,login)
def log_create_post(login):
    log(2,3,login)
def log_create_blog(login):
    log(3, 5, login)
def log_delete_post(login):
    log(2,4, login)
def log_comment(login):
    log(1,2, login)
def log_logout(login):
    log(3,6, login)