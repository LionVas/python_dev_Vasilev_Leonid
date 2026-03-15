

from flask import Flask, render_template, request
app = Flask(__name__)
login=""
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        login = request.form['login']

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)