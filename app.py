#!/usr/bin/python3
from email import message
from pickle import NONE
from xml.etree.ElementTree import Comment
from flask import Flask, request, render_template, make_response, redirect, url_for, send_file, session, g
import sqlite3
import hashlib
import os
import time, random
import os #운영체제에서 제공되는 여러 기능을 파이썬에서 수행할 수 있게 해줌.
from flask import Flask, flash, request, redirect
from flask import url_for, render_template
from werkzeug.utils import secure_filename
#from xss_stored import xss_stored_page, xss_stored_api
from util import get_root_dir, get_uploads_folder_url
from db_helper import db_helper
from db_models import db_models
from middlewares import require_api_key
import urllib.request
from vulns.sql_injection.sql_injection_login import sql_injection_login_page, sql_injection_login_api
from vulns.sql_injection.sql_injection_search import sql_injection_search_page
from vulns.file_upload.file_upload import file_upload_page, file_upload_api
from vulns.xssinjection.xss_reflected import xss_reflected_page
from vulns.xssinjection.xss_stored import xss_stored_page, xss_stored_api
from vulns.ssrf.ssrf import ssrf_page, ssrf_api
from vulns.path_traversal.path_traversal import path_traversal_page, path_traversal_image
from pathlib import Path

app = Flask(__name__)

app.config['TEMP_UPLOAD_FOLDER'] = f"{get_root_dir()}/temp/uploads"
app.config['PUBLIC_UPLOAD_FOLDER'] = f"{get_root_dir()}/static/uploads"
app.config['PUBLIC_IMG_FOLDER'] = f"{get_root_dir()}/static/img"
app.config['STATIC_BASE_URL'] = '/static'
app.config['PUBLIC_UPLOADS_URL'] = f"{app.config['STATIC_BASE_URL']}/uploads"
ALLOWED_EXTENSIONS = ['.png', '.jpeg', '.jpg']

app.secret_key = os.urandom(32)
DATABASE = "database.db"
MAXRESETCOUNT = 5

app.db_helper = db_helper
app.db_models = db_models

def makeBackupcode():
    return random.randrange(100)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/main_success/<userid>')
def index(userid):
    return render_template('main_success.html', userid=userid)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        userid = request.form.get("userid")
        userpasswd = request.form.get("userpasswd")

        conn = get_db()
        cur = conn.cursor()
        user = cur.execute("SELECT * FROM user WHERE userid = '%s' and userpasswd = '%s'"%(userid, userpasswd)).fetchone()        
        if user:
            session['userid'] = user['userid']
            session['userpasswd'] = user['userpasswd']
            return redirect(url_for('index', userid=userid)) #userid=userid

        return "<script>alert('잘못된 아이디 또는 패스워드입니다.');history.back(-1);</script>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        userid = request.form.get("userid")
        userpasswd = request.form.get("userpasswd")
        name = request.form.get("name")
        email = request.form.get("email")
        birth = request.form.get("birth")

        conn = get_db()
        cur = conn.cursor()
        user = cur.execute('SELECT * FROM user WHERE userid = ?', (userid,)).fetchone()
        
        if user:
            return "<script>alert('이미 존재하는 아이디입니다.');history.back(-1);</script>";
        user = cur.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()
        if user:
            return "<script>alert('이미 존재하는 이메일입니다.');history.back(-1);</script>";

        sql = "INSERT INTO user(userid, userpasswd, name, email, birth) VALUES (?, ?, ?, ?, ?)"
        cur.execute(sql, (userid, userpasswd, name, email, birth))
        conn.commit()
        return render_template("index.html", msg=f"<b>회원가입에 성공하였습니다.</b><br/>")

@app.route('/list', methods=['GET', 'POST'])
def list():
    conn = get_db()
    cur = conn.cursor()
    if request.method == 'GET':
        rows = cur.execute("SELECT * FROM brdwrite")
        
        return render_template('list.html',rows=rows)
    else:
        no = request.form.get("no")
        title = request.form.get("title")
        write = request.form.get("write")
        regdate = request.form.get("regdate")
        count = request.form.get("count")
       

        cur.execute("SELECT * FROM brdwrite WHERE no = ?", (no,)).fetchall()
        conn.commit()
        return render_template("list.html")


@app.route('/write', methods=['GET', 'POST'])
def write():
    conn = get_db()
    cur = conn.cursor()
    if request.method == 'GET':
        userid = request.form.get("userid")
        rows = cur.execute("SELECT * FROM user WHERE userid = ?", (userid,)).fetchall()
        return render_template('write.html',rows=rows)
    else:
        writer = request.form.get("writer")
        title = request.form.get("title")
        context = request.form.get("context")

     #   if brdcontext:
     #       brdcontext = cur.execute("SELECT * FROM brdcontext")

        sql = "INSERT INTO brdwrite(writer, title, context) VALUES (?, ?, ?)"
        cur.execute(sql, (writer, title, context))
        conn.commit()
        
        return render_template('write.html')

@app.route('/read', methods=['GET', 'POST'])
def read():
    if request.method == 'GET':
        return render_template('read.html')
    else:
        no = request.form.get("no")
        title = request.form.get("title")
        write = request.form.get("write")
        regdate = request.form.get("regdate")
        count = request.form.get("count")

        conn = get_db()
        cur = conn.cursor()
        sql = 'SELECT * FROM brdwrite WHERE no,'
        cur.execute(sql,(no, title, write, regdate, count))

        conn.commit()
        return render_template("read.html")

@app.route('/sell', methods=['GET', 'POST'])
def sell():
    return render_template('sell.html')

"""
@app.route('/writecomment', methods=['GET', 'POST'])
def writecomment():
    if request.method == 'GET':
        return render_template('write.html')
    else:
        writer = request.form.get("writer")
        comment = request.form.get("comment")

        conn = get_db()
        cur = conn.cursor()

     #   if brdcontext:
     #       brdcontext = cur.execute("SELECT * FROM brdcontext")

        sql = "INSERT INTO brdcomment(writer, title, context) VALUES (?, ?, ?)"
        cur.execute(sql, (writer, comment))
        conn.commit()
        
        return render_template("write.html")
"""
"""
@app.route('/downfile')
def down_page():
	files = os.listdir("./uploads")
	return render_template('filedown.html',files=files)

#파일 다운로드 처리
@app.route('/fileDown', methods = ['GET', 'POST'])
def down_file():
	if request.method == 'POST':
		sw=0
		files = os.listdir("./uploads")
		for x in files:
			if(x==request.form['file']):
				sw=1

		path = "./uploads/" 
		return send_file(path + request.form['file'],
				attachment_filename = request.form['file'],
				as_attachment=True)
"""

#@app.route('/upload', methods=['GET', 'POST'])
#def upload():
#    return render_template("upload.html")

def xss_stored_page(request, app):
    messages = app.db_helper.execute_read('SELECT * FROM messages', {})
    print(messages)
    xss_message = []
    for i in messages:
        xss_message.append(i[0])

    return render_template('xss_stored.html', messages=xss_message)


def xss_stored_api(request, app):
    message = request.form['message']
    result = app.db_helper.execute_write('INSERT INTO messages (message) VALUES (:msg)', { 'msg': message })

    return xss_stored_page(request, app)

def ssrf_page(request, app):
    return render_template(
        'ssrf.html'
    )


def ssrf_api(request, app):
    form = request.form

    name = form['name']
    email = form['email']
    original_picture_url = form['imageUrl']

    downloaded_url = _download_image(original_picture_url, app)

    return render_template(
        'ssrf.html',
        email=email,
        name=name,
        original_url=original_picture_url,
        profile_picture_url=downloaded_url
    )


def _download_image(url, app):
    if not url:
        return ''

    download_image_path = ''

    with urllib.request.urlopen(url) as f:
        download_image_path = f"{app.config['PUBLIC_UPLOAD_FOLDER']}/downloaded-image.png"

        with open(download_image_path, 'wb') as file:
            file_content = f.read()
            file.write(file_content)
            file.close()

    public_url = f"{app.config['PUBLIC_UPLOADS_URL']}/downloaded-image.png"

    return public_url

def path_traversal_page(request, app):                  #넣지 않아도 작동함
    return render_template("path-traversal.html")


def path_traversal_image(request, app):                 #넣지 않아도 작동함
    image_path = f"{app.config['PUBLIC_IMG_FOLDER']}/{request.args.get('img')}"

    return send_file(image_path)

def file_upload_page():
    return render_template('file_upload.html', file_url=None)


def file_upload_api(request, app):
    file = request.files['file']

    if not _validate_file(file.filename):
        return {
            'message': 'Invalid file extension',
            'allowed_ext': ALLOWED_EXTENSIONS,
            'filename': file.filename
        }, 422

    saved_file_result = _save_temp_file(file, app)
    saved_file_path = saved_file_result['saved_path']

    file_name = Path(saved_file_path).name

    public_upload_file_path = os.path.join(app.config['PUBLIC_UPLOAD_FOLDER'], file_name)
    
    os.system(f'mv {saved_file_path} {public_upload_file_path}')

    return render_template('file_upload.html', file_url=f'{get_uploads_folder_url()}/{file_name}')


def _validate_file(filename):
    extension = os.path.splitext(filename)[1]
    return extension in ALLOWED_EXTENSIONS


def _save_temp_file(file, app):
    original_file_name = file.filename
    temp_upload_file_path = os.path.join(app.config['TEMP_UPLOAD_FOLDER'], original_file_name)
    file.save(temp_upload_file_path)
    
    resized_image_path = f'{temp_upload_file_path}.min.png'
    # https://imagemagick.org/script/convert.php
    command = f'convert "{temp_upload_file_path}" -resize 50% "{resized_image_path}"'
    os.system(command)

    return {
        'saved_path': resized_image_path
    }

@app.route('/xss_stored', methods=['GET', 'POST'])
def xss_stored():
    if request.method == 'GET':
        return xss_stored_page(request, app)

    return xss_stored_api(request, app) 

@app.route('/reset-database', methods=['POST'])
def reset_database():
    db_helper.reset_database()
    return redirect(url_for('home', reset_db=1))


@app.route('/sql-injection/login', methods=['GET', 'POST'])
def sql_injection_login():
    if request.method == 'GET':
        return sql_injection_login_page(request, app)

    return sql_injection_login_api(request, app)


@app.route('/sql-injection/search', methods=['GET'])
def sql_injection_search():
    return sql_injection_search_page(request, app)


@app.route('/file-upload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        return file_upload_api(request, app)
    
    return file_upload_page()


@app.route('/ssrf', methods=['GET', 'POST'])
def ssrf():
    if request.method == 'GET':
        return ssrf_page(request, app)

    return ssrf_api(request, app)


@app.route('/path-traversal', methods=['GET'])
def path_traversal():
    return path_traversal_page(request, app)


@app.route('/path-traversal-img', methods=['GET'])
def path_traversal_img():
    return path_traversal_image(request, app)

app.run(host='0.0.0.0', port=4900)
