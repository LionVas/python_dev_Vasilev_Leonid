from .DBconnection import database
from .Blogs_controller import get_user_id, login_check
def generate_comments(login):
    database.open_dataset_db()
    cursor = database.get_dataset_cursor()
    dataset = []
    if login_check(login, cursor):
        user_id = get_user_id(login, cursor)
        cursor.execute("SELECT post.header, author.login, COUNT(comment.id) FROM comment INNER JOIN post ON comment.post_id = post.id INNER JOIN author ON post.author_id = author.id  WHERE comment.author_id = ? GROUP BY post.header", (user_id,))
        res = cursor.fetchall()
        for elem in res:
            dataset.append({"login": login, "header": elem[0], "post_author": elem[1], "comments": elem[2]})
    database.close_dataset_db()
    return dataset

def generate_general(login):
    database.open_dataset_db()
    cursor = database.get_dataset_cursor()
    dataset = []
    if login_check(login, cursor):
        user_id = get_user_id(login, cursor)
        cursor = database.get_dataset_log_cursor()
        cursor.execute(
            "SELECT date(datetime), COUNT(CASE WHEN event_type_id=1 THEN 1 END), COUNT(CASE WHEN event_type_id=6 THEN 1 END), COUNT(CASE WHEN space_type_id <=2 THEN 1 END) FROM logs WHERE user_id = ? GROUP BY date(datetime)",
            (user_id,))
        res = cursor.fetchall()
        for elem in res:
            dataset.append({"date": elem[0], "logins": elem[1], "logouts": elem[2], "actions": elem[3]})
    database.close_dataset_db()
    return dataset