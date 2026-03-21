import sqlite3


class DBconnection:
    def __init__(self):
        self.blog_db = None
        self.blog_db = None
        # self.blog_db.execute("PRAGMA journal_mode=WAL;")
        # self.logs_db.execute("PRAGMA journal_mode=;")
    def get_blog_cursor(self):
        return self.blog_db.cursor()
    def get_logs_cursor(self):
        return self.logs_db.cursor()
    def close_db(self):
        self.blog_db.close()
        self.logs_db.close()
    def open_db(self):
        self.blog_db = sqlite3.connect('Blogs.db', check_same_thread=False)
        self.logs_db = sqlite3.connect('Logs.db', check_same_thread=False)
database = DBconnection()