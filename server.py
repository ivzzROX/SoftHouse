import os
import hashlib
from flask import Flask
from flask import request, render_template, jsonify, redirect, make_response, session
from flask_restful import Resource, Api
from flask_cors import CORS
from email_sender import send_confirm_mail
from db import create_user, check_user, get_username_by_id, check_user_data_collision, get_mail_by_username, \
     confirm_user, get_users
import config
from request_handler import TimeStamp, TestEndpoint, TestTimeEndpoint, \
     SensorsStatus, RegisterDevice, GetUserLogic

server = Flask('my_app')
app = Flask(__name__)
cors = CORS(app)
app.secret_key = os.urandom(24)
app.config['SESSION_COOKIE_NAME'] = 'cookie'
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)
api.add_resource(TimeStamp, '/timestamp')
api.add_resource(TestEndpoint, '/test')
api.add_resource(TestTimeEndpoint, '/testtime')
api.add_resource(SensorsStatus, '/sensors')
api.add_resource(RegisterDevice, '/device')
api.add_resource(GetUserLogic, '/logic')


def get_session_param(param):
    if param in session:
        return int(session[param])
    return 0


def hash_generate(param):
    return hashlib.md5((param + 'salt0x45').encode()).hexdigest()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        session['log'] = '0'
        return render_template("login.html")
    elif request.method == 'POST':
        data = request.json
        user_id = check_user(data['login'], data['passwd'])
        if user_id > -1:
            session['log'] = '1'
            session['user'] = user_id
            return jsonify({"status": "OK"})
        else:
            session['log'] = '0'
            return jsonify({"status": "ERROR"})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        data = request.json
        if check_user_data_collision(data['username'], data['email']):
            return jsonify({"status": "Login or email already used"})
        else:
            create_user(data['username'], data['email'], data['passwd'])
            link = 'http://ddesmintyserver.ml:5002/account_confirm?user=' + data['username'] + '&code=' + \
                   hash_generate(data['username'] + data['email'])
            send_confirm_mail([data['email']], link)
            return jsonify({"status": "OK"})


@app.route('/account_confirm', methods=['GET'])
def account_confirm():
    if request.method == 'GET':
        user = request.args.get('user')
        code = request.args.get('code')
        mail = get_mail_by_username(user)
        if code == hash_generate(user + mail):
            confirm_user(user)
            print('User confirmed')
            return redirect("localhost:5002/login")
        else:
            print('Some mistake')


def device_list_to_htm(dev_list):
    res = ""
    for dev in dev_list:
        res += str(dev)
    return res


def device_status_list_to_htm(dev_list):
    res = ""
    for dev in dev_list:
        # get device status
        dev_status = "not connected"
        res += (str(dev) + ":" + dev_status)
    return res


@app.route('/main')
def main():
    if get_session_param('log'):
        user_id = get_session_param('user')
        # get all user devices
        device_test_list = [0o000000, 0o00001, 0o000002]
        return render_template("main.html",
                               login=get_username_by_id(user_id),
                               dev_sn=device_list_to_htm(device_test_list),
                               dev_status=device_status_list_to_htm(device_test_list))
    else:
        return redirect("localhost:5002/login")


@app.route('/draw_page')
def draw_page():
    if get_session_param('log'):
        return render_template("draw_page.html")
    else:
        return redirect("localhost:5002/login")


@app.route('/confirm_mail')
def confirm_mail():
    return render_template("confirm_mail.html")


def start_server():
    app.run(host=config.HOST, port=config.HTTP_PORT)


if __name__ == '__main__':
    get_users()
    app.run(host=config.HOST, port=config.HTTP_PORT)
