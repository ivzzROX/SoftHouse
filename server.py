from flask import Flask
from flask import send_file
from flask import render_template
from flask_restful import Resource, Api
from flask_cors import CORS
import config
from request_handler import TimeStamp, TestEndpoint, TestTimeEndpoint, TestPmoEndpoint, TestTelegramEndpoint, \
    TestInoEndpoint, RegisterSensors, RegisterDevice, GetUserLogic

server = Flask('my_app')
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)
api.add_resource(TimeStamp, '/timestamp')
api.add_resource(TestEndpoint, '/test')
api.add_resource(TestPmoEndpoint, '/testpmo')
api.add_resource(TestTimeEndpoint, '/testtime')
api.add_resource(TestTelegramEndpoint, '/testtlgrm')
api.add_resource(TestInoEndpoint, '/testino')
api.add_resource(RegisterSensors, '/sensors')
api.add_resource(RegisterDevice, '/device')
api.add_resource(GetUserLogic, '/logic')


@app.route('/draw_page')
def draw_page():
    return render_template("draw_page.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/main')
def main():
    return render_template("main.html")


@app.route('/register')
def register():
    return render_template("register.html")


def start_server():
    app.run(host=config.HOST, port=config.HTTP_PORT)


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.HTTP_PORT)
