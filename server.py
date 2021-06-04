import os
import json
import hashlib
from flask import Flask, url_for
from flask import request, render_template, jsonify, redirect, make_response, session
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from email_sender import send_confirm_mail
from db import create_user, check_user, get_username_by_id, check_user_data_collision, get_mail_by_username, \
    confirm_user, get_users, load_user_logic_from_db
import config
from request_handler import TimeStamp, TestEndpoint, TestTimeEndpoint, \
    RegisterSensors, RegisterDevice, SaveUserLogic, OutputsToUpdate, DeviceLogs

server = Flask('my_app')
app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.secret_key = os.urandom(24)
app.config['SESSION_COOKIE_NAME'] = 'data'
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)
api.add_resource(TimeStamp, '/timestamp')
api.add_resource(TestEndpoint, '/test_1')
api.add_resource(TestTimeEndpoint, '/testtime')
api.add_resource(RegisterSensors, '/sensors')
api.add_resource(RegisterDevice, '/device')
api.add_resource(SaveUserLogic, '/logic')
api.add_resource(OutputsToUpdate, '/sensor_list')
api.add_resource(DeviceLogs, '/device_logs')


def get_session_param(param):
    if param in session:
        return int(session[param])
    return 0


def hash_generate(param):
    return hashlib.md5((param + 'salt0x45').encode()).hexdigest()


@app.route('/login', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def login():
    if request.method == 'GET':
        session['log'] = '0'
        return render_template("login.html")
    elif request.method == 'POST':
        data = request.json
        user_id = check_user(data['login'], data['passwd'])
        if user_id > -1:
            resp = make_response(jsonify({"status": "OK"}))
            # resp = jsonify({"status": "OK"})
            resp.set_cookie("user_id", str(user_id))
            # resp.headers.add('Access-Control-Allow-Credentials', 'true')
            # resp.set_cookie("user_id", str(user_id))
            session['user'] = str(user_id)
            session['log'] = '1'
            session.modified = True
            return resp
        else:
            session['log'] = '0'
            return jsonify({"status": "ERROR"})


@app.route('/register', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def register():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        data = request.json
        if check_user_data_collision(data['username'], data['email']):
            return jsonify({"status": "Login or email already used"})
        else:
            create_user(data['username'], data['email'], data['passwd'])
            link = 'http://ddesmintyserver.ml:5002/account_confirm?user=' + data['username'] + '&code=' + hash_generate(
                data['username'] + data['email'])
            send_confirm_mail([data['email']], link)
            return jsonify({"status": "OK"})


@app.route('/account_confirm', methods=['GET'])
@cross_origin(supports_credentials=True)
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


@app.route('/')
@cross_origin(supports_credentials=True)
def empty_url():
    return redirect('localhost:5002/main')


@app.route('/main')
@cross_origin(supports_credentials=True)
def main():
    if get_session_param('log'):
        user_id = get_session_param('user')
        return render_template("main.html", login=get_username_by_id(user_id), dev_sn="000000",
                               dev_status="not connected")
    else:
        return redirect(url_for("login"))


@app.route('/draw_page')
@cross_origin(supports_credentials=True)
def draw_page():
    if True:#get_session_param('log'):
        return render_template("draw_page.html")
    else:
        return redirect(url_for("login"))


@app.route('/load_logic')
@cross_origin(supports_credentials=True)
def load_user_logic():
    user_id = request.args.get('user_id')
    output_id = request.args.get('output_id')
    res = load_user_logic_from_db(user_id, output_id)
    return jsonify(res)


@app.route('/confirm_mail')
@cross_origin(supports_credentials=True)
def confirm_mail():
    return render_template("confirm_mail.html")


def start_server():
    app.run(host=config.HOST, port=config.HTTP_PORT)


if __name__ == '__main__':
    # get_users()  # TODO handle when user table does not exist
    app.run(host=config.HOST, port=config.HTTP_PORT)
