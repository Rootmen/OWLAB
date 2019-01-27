import os
from random import random

from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = '/home/rootmen/Git/Hack_flask/templates'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploaddata', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return filename
    return "Error"



@app.route('/')
def index():
    if request.path=='/':
        return render_template("index2.html")
    return render_template(request.path)

@app.route('/<path:post_id>')
def show_post(post_id):
    # вывести сообщение с данным id, id - целое число
    return render_template('%d' % post_id)
import cv


@app.route('/getprint', methods=['GET', 'POST'])
def upload_file2():
    cv.maincv()
    return


if __name__ == '__main__':
    app.run(host='0.0.0.0')
