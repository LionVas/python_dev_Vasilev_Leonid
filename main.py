from app import Dataset_generator, Blogs_controller
from app import Logs_controller
from app.DBconnection import database
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
app = Flask(__name__)
app.json.sort_keys = False
app.secret_key = '<MEGASECRETKEY>'
login=""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        login = ""
        session.clear()
        return render_template('index.html')
    elif request.method == 'POST':
        login = request.form['login']
        if login == "" or login is None or len(login)> 20:
            return render_template('index.html', error_message="Некорректный логин")
        database.open_db()
        if Blogs_controller.login_check(login, database.get_blog_cursor()):
            #print(posts)
            session['login'] = login
            Logs_controller.log_login(login)
            return redirect(url_for("profile"))
            #return render_template('profile.html', login=login, posts=posts)
        else:
            return render_template('index.html', error_message="Неизвестный логин")

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':

        user_posts = Blogs_controller.get_posts(session['login'])

        return render_template('profile.html', posts=user_posts, login=session['login'])
    elif request.method == 'POST':
        if 'post_create' in request.form:
            header = request.form['post_header']
            post_content = request.form['post_content']
            blog_id = request.form['blog_id'].replace(" ", "")
            if (header != "") and (post_content != "") and (blog_id != ""):
                if Blogs_controller.create_post(session['login'], header, post_content, blog_id):
                    Logs_controller.log_create_post(session['login'])
            return redirect(url_for('profile'))
        elif 'comment' in request.form:
            post_id = request.form['post_id']
            comment = request.form['comment']
            if (post_id != "") and (comment != ""):
                if  Blogs_controller.comment_post(session['login'], post_id, comment):
                    Logs_controller.log_comment(session['login'])
            return redirect(url_for('profile'))
        elif 'delete' in request.form:
            post_id = request.form['del_post_id']
            if post_id != "":

                if Blogs_controller.delete_post(session['login'], post_id):
                    Logs_controller.log_delete_post(session['login'])
            return redirect(url_for('profile'))
        elif 'blog_create' in request.form:
            blog_name = request.form['blog_name']
            blog_description = request.form['blog_description']
            if (blog_name != "") and (blog_description != ""):
               if Blogs_controller.create_blog(session['login'], blog_name, blog_description):
                    Logs_controller.log_create_blog(session['login'])
            return redirect(url_for('profile'))
        elif 'logout' in request.form:
            Logs_controller.log_logout(session['login'])
            database.close_db()
            return redirect(url_for('index'))

@app.route('/comments', methods=['GET'])
def comments():
    if request.method == 'GET':
        req_login = request.args.get('login')
        comms = Dataset_generator.generate_comments(req_login)
        return jsonify(comms)
@app.route('/general', methods=['GET'])
def general():
    if request.method == 'GET':
        req_login = request.args.get('login')
        comms = Dataset_generator.generate_general(req_login)
        return jsonify(comms)
@app.errorhandler(Exception)
def handle_error(e):
    print(e)
    return render_template('error.html', error=e)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
