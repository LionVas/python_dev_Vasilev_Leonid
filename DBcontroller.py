import sqlite3

from DBconnection import database


def get_user_id(login):
    cursor = database.get_blog_cursor()
    cursor.execute('SELECT id FROM author WHERE login = ?', (login,))
    user_id = cursor.fetchall()[0][0];
    return user_id
def login_check(login):
    cursor = database.get_blog_cursor()
    cursor.execute('SELECT * FROM author WHERE login = ?', (login,))
    users = cursor.fetchall()

    if len(users) == 1:
        return True
    else:
        return False

def get_posts(login):
    cursor = database.get_blog_cursor()
    cursor.execute('SELECT id FROM author WHERE login = ?', (login,))
    user_id = cursor.fetchall()[0][0];
    cursor.execute('SELECT header, text, id, blog_id FROM post WHERE author_id = ?', (user_id,))
    posts = cursor.fetchall()
    # connection.close()
    return posts

def create_post(login, header, post_content, blog_id):
    with database.blog_db:
        cursor = database.get_blog_cursor()
        user_id = get_user_id(login)
        cursor.execute('INSERT INTO post (header, text, author_id, blog_id) VALUES(?, ?, ?, ?)', (header, post_content, user_id, blog_id))



def create_blog(login, blog_name, blog_description):
    with database.blog_db:
        cursor = database.get_blog_cursor()
        user_id = get_user_id(login)
        cursor.execute("INSERT INTO blog (owner_id, name, description) VALUES(?, ?, ?)", (user_id, blog_name, blog_description))


def delete_post(login, id):

    with database.blog_db:
        cursor = database.get_blog_cursor()
        user_id = get_user_id(login)
        cursor.execute('SELECT author_id FROM post WHERE id = ?', (id,))
        res = cursor.fetchall()
        if len(res) == 0:
            return False
        else:
            author_id = res[0][0]
        if author_id == user_id:
            cursor.execute('DELETE FROM post WHERE id = ?', (id,))
            database.blog_db.commit()



def comment_post(login, post_id, comment):
    with database.blog_db:
        cursor = database.get_blog_cursor()
        user_id = get_user_id(login, )

        cursor.execute('SELECT count(*) FROM post WHERE id = ?', (post_id,))
        count = cursor.fetchone()[0]
        if count > 0:
            cursor.execute("INSERT INTO comment (author_id, post_id, text) VALUES(?, ?, ?)", (user_id,post_id,comment))


