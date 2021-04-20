from flask import Flask, url_for, request, render_template, abort, jsonify, make_response
from markupsafe import escape

import sqlite3

app = Flask(__name__)

DB_NAME = 'db.db'
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
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'root' and password == 'password':
            message = "Loged in"
        else:
            message = "Incorrect login or password"

    return render_template('login.html', message=message)

@app.route('/user/<name>&<int:number>')
def user(name=None, number=3):
    return render_template('user.html', user=name, number=number)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        db_request = "SELECT * FROM tasks"
        data = cursor.execute(db_request).fetchall()
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
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        db_request = "SELECT * FROM tasks WHERE id = ?"
        data = cursor.execute(db_request, (task_id,)).fetchone()

        if len(data) == 0:
            abort(404)

        task = {'name': data[1], 
                'id': data[0],
                'description': data[2]}

        return jsonify({'task': task})

@app.route('/api/tasks', methods=['POST'])
def create_task():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        if not request.json or not 'name' in request.json:
            abort(400)

        db_request = "INSERT INTO 'tasks' ('name', 'description') VALUES (?,?)"
        cursor.execute(db_request, (request.json['name'], request.json['description']))
        conn.commit()
        
        max_id = cursor.execute("SELECT count(*) FROM tasks").fetchone()[0]

        task = {
                'name': request.json['name'],
                'id': max_id + 1,
                'description': request.json.get('description', '')
        }

        return make_response(jsonify({'task': task}), 201)

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        max_id = cursor.execute("SELECT count(*) FROM tasks").fetchone()[0]
        if task_id > max_id:
            abort(400)
        
        db_request = "DELETE FROM tasks WHERE id = ?"
        cursor.execute(db_request, (task_id,))
        conn.commit()

        db_request = "SELECT * FROM tasks"
        data = cursor.execute(db_request).fetchall()
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
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        db_request = "UPDATE tasks SET name = ?, description = ?, corrected = ? WHERE id = ?"
        cursor.execute(db_request, (request.json['name'], request.json['description'], True, task_id))
        conn.commit()

        max_id = cursor.execute("SELECT count(*) FROM tasks").fetchone()[0]

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