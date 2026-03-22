import sqlite3


class DBconnection:
    def __init__(self):
        self.blog_db = None
        self.logs_db = None
        self.dataset_db = None
        self.dataset_log_db = None
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
    def open_dataset_db(self):
        self.dataset_db = sqlite3.connect('Blogs.db', check_same_thread=False)
        self.dataset_log_db = sqlite3.connect('Logs.db', check_same_thread=False)
    def close_dataset_db(self):
        self.dataset_db.close()
        self.dataset_log_db.close()
    def get_dataset_cursor(self):
        return self.dataset_db.cursor()
    def get_dataset_log_cursor(self):
        return self.dataset_log_db.cursor()
database = DBconnection()