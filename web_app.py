from flask import Flask, request
from db_connector import *
import os
import signal

app = Flask(__name__)


@app.route('/stop_server')
def stop_server():
    os.kill(os.getpid(), signal.SIGINT)
    return 'Server stopped'


@app.route('/users/<user_id>', methods=['GET', 'POST', 'DELETE'])
def user(user_id):
    if request.method == "GET":
        try:
            name = get_name(user_id)
            return "<H1 id='user'>" + name + "</H1>"
        except:
            return "<H1 id='error'>" 'no such user:' + user_id + "</H1>"

    elif request.method == "POST":
        print("a post request has been made")
        request_data = request.json
        name = request_data.get('name')
        try:
            add_user(user_id, name)
            print("User successfully added")
            return {'status': 'ok', 'user_added': name}, 200  # status code
        except:
            return {'status': 'error', 'reason': 'ID already exists'}, 500

    elif request.method == "DELETE":
        try:
            delete_user(user_id)
            return {'status': 'ok', 'user_deleted': user_id}, 200  # status code
        except:
            return {'status': 'error', 'reason': 'no such ID'}, 500


app.run(host='127.0.0.1', debug=True, port=5001)
