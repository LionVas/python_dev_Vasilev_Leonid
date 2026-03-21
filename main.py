import DBcontroller

from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
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
        if DBcontroller.login_check(login):

            #print(posts)

            session['login'] = login
            return redirect(url_for("profile"))
            #return render_template('profile.html', login=login, posts=posts)
        else:
            return render_template('index.html', error_message="Неизвестный логин")
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':

        user_posts = DBcontroller.get_posts(session['login'])

        return render_template('profile.html', posts=user_posts, login=session['login'])
    elif request.method == 'POST':
        if 'post_create' in request.form:
            header = request.form['post_header'].replace(" ", "")
            post_content = request.form['post_content'].replace(" ", "")
            blog_id = request.form['blog_id'].replace(" ", "")
            if (header != "") and (post_content != "") and (blog_id != ""):
                DBcontroller.create_post(session['login'], header, post_content, blog_id)
                print("победа")
            return redirect(url_for('profile'))
        elif 'comment' in request.form:
            post_id = request.form['post_id']
            comment = request.form['comment']
            DBcontroller.comment_post(session['login'], post_id, comment)
            return redirect(url_for('profile'))
        elif 'delete' in request.form:
            post_id = request.form['del_post_id']
            DBcontroller.delete_post(session['login'], post_id)
            return redirect(url_for('profile'))
        elif 'blog_create' in request.form:
            blog_name = request.form['blog_name']
            blog_description = request.form['blog_description']
            DBcontroller.create_blog(session['login'], blog_name, blog_description)
            return redirect(url_for('profile'))
        elif 'logout' in request.form:
            return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)