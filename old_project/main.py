from flask import (Flask, url_for, request, redirect, render_template,
                    abort, jsonify, make_response, session)
from werkzeug.security import generate_password_hash,  check_password_hash
import pymysql
import datetime
import os

import config
import utils


db = pymysql.connect(host="localhost", 
                        user=config.DB_LOGIN, 
                        password=config.DB_PASSWORD, 
                        database=config.DB_NAME,
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)  

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(20).hex()
app.permanent_session_lifetime = datetime.timedelta(days=1)

##############################################################################

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

##############################################################################

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'session_id' in session:
        with db.cursor() as cursor:
            db_request = "SELECT user_id FROM cookies WHERE session_id=%s"
            cursor.execute(db_request, (session['session_id']))
            user_id = cursor.fetchone()

            if user_id:
                db_request = "SELECT login FROM users WHERE id=%s"
                cursor.execute(db_request, user_id['user_id'])
                login = cursor.fetchone()
                if login:
                    new_key = utils.generate_key(30)
                    session['session_id'] = new_key
                    session.modified = True

                    db_request = "UPDATE cookies SET session_id=%s WHERE user_id=%s"
                    cursor.execute(db_request, (new_key, user_id['user_id']))
                    db.commit()

                    return redirect(url_for('user', login=login['login']))

    message = None
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        if not password or not login:
            message = "Incorrect login or password"
            return render_template('login.html', message=message)

        with db.cursor() as cursor:
            db_request = "SELECT id, hash_password FROM users WHERE login=%s"
            cursor.execute(db_request, (login))
            data = cursor.fetchone()

            try:
                user_password = data['hash_password']
            except KeyError:
                message = "Incorrect login or password"
            else:
                if not check_password_hash(user_password, password):
                    message = "Incorrect login or password"
                else:
                    db_request = "SELECT session_id FROM cookies WHERE user_id=%s"
                    cursor.execute(db_request, data['id'])
                    session_id = cursor.fetchone()

                    new_key = utils.generate_key(30)
                    session['session_id'] = new_key

                    if not session_id:
                        db_request = "INSERT INTO cookies (session_id, user_id) VALUES (%s, %s)"
                        cursor.execute(db_request, (new_key, data['id']))
                        db.commit()
                    else:
                        db_request = "UPDATE cookies SET session_id=%s WHERE user_id=%s"
                        cursor.execute(db_request, (new_key, data['id']))
                        db.commit()

                    return redirect(url_for('user', login=login))

    return render_template('login.html', message=message)

@app.route('/registration', methods=['GET', 'POST'])
def register_new_user():
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        login = request.form.get('login')
        password = request.form.get('password')

        with db.cursor() as cursor:
            db_request = "SELECT * FROM users WHERE login=%s"
            cursor.execute(db_request, (login,))
            data = cursor.fetchall()

            if len(data) == 0:
                if (len(username) > 1) and (len(login) > 6) and (len(password) > 6):
                    db_request = "INSERT INTO users (name, is_admin, login, hash_password) VALUES(%s, %s, %s, %s)"
                    cursor.execute(db_request, (username, False, login, generate_password_hash(password)))
                    db.commit()

                    #message = 'Registered sucessfuly'
                    return redirect(url_for('user', login=login))
                else:
                    message = 'Incorrect data length'
            else:
                message = 'Such login already exists.\nPlease change login and try again'

    return render_template('sign_up.html', message=message)

@app.route('/user/<login>')
def user(login=None):
    with db.cursor() as cursor:
        db_request = "SELECT id FROM users WHERE login=%s"
        cursor.execute(db_request, (login,))
        try:
            user_id = cursor.fetchone()['id']
        except TypeError:
            abort(404)
        else:
            db_request = "SELECT * FROM tasks WHERE user_id=%s"
            cursor.execute(db_request, (user_id,))
            data = cursor.fetchall()

            return render_template('user.html', user=login, tasks=data, length=len(data))

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    with db.cursor() as cursor:
        db_request = "SELECT * FROM tasks"
        cursor.execute(db_request)
        data = cursor.fetchall()
        tasks = []
        for item in data:
            task = {'name': item[1], 
                'id': item[0],
                'description': item[2]
            }
            tasks.append(task)

        return jsonify({'tasks':tasks})

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    with db.cursor() as cursor:
        db_request = "SELECT * FROM tasks WHERE id = %d"
        cursor.execute(db_request, (task_id,))
        data = cursor.fetchone()

        if len(data) == 0:
            abort(404)

        task = {'name': data[1], 
                'id': data[0],
                'description': data[2]}

        return jsonify({'task': task})

@app.route('/api/tasks', methods=['POST'])
def create_task():
    with db.cursor() as cursor:
        if not request.json or not 'name' in request.json:
            abort(400)

        db_request = "INSERT INTO tasks (name, description) VALUES (%s,%s)"
        cursor.execute(db_request, (request.json['name'], request.json['description']))
        db.commit()
        
        max_id = cursor.execute("SELECT count(*) FROM tasks").fetchone()[0]

        task = {
                'name': request.json['name'],
                'id': max_id + 1,
                'description': request.json.get('description', '')
        }

        return make_response(jsonify({'task': task}), 201)

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    with db.cursor() as cursor:
        cursor.execute("SELECT count(*) FROM tasks")
        max_id = cursor.fetchone()[0]# должно вернуть количество записей, посмотреть в каком виде

        if task_id > max_id:
            abort(400)
        
        db_request = "DELETE FROM tasks WHERE id = %d"
        cursor.execute(db_request, (task_id,))
        db.commit()

        db_request = "SELECT * FROM tasks"
        cursor.execute(db_request)
        data = cursor.fetchone()

        tasks = []
        for item in data:
            task = {'name': item[1], 
                'id': item[0],
                'description': item[2]
            }
            tasks.append(task)

        return jsonify({'tasks':tasks})

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):   
    with db.cursor() as cursor:
        db_request = "UPDATE tasks SET name = %s, description = %s WHERE id = %d"
        cursor.execute(db_request, (request.json['name'], request.json['description'], task_id))
        db.commit()

        cursor.execute("SELECT count(*) FROM tasks")
        max_id = cursor.fetchone()[0]

        if task_id > max_id:
            abort(400)
        if not request.json:
            abort(400)
        
        task = dict()
        task['name'] = request.json['name']
        task['description'] = request.json['description']
        task['corrected'] = True

        return make_response(jsonify({'task': task}), 201)

if __name__ == '__main__':
    app.run(debug=True)