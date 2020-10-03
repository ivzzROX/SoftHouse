from flask import Flask
from flask_restful import Resource, Api

import config
from request_handler import TimeStamp, TestEndpoint, TestTimeEndpoint, TestPmoEndpoint, TestTelegramEndpoint, \
    TestInoEndpoint

server = Flask('my_app')
app = Flask(__name__)
api = Api(app)
api.add_resource(TimeStamp, '/timestamp')
api.add_resource(TestEndpoint, '/test')
api.add_resource(TestPmoEndpoint, '/testpmo')
api.add_resource(TestTimeEndpoint, '/testtime')
api.add_resource(TestTelegramEndpoint, '/testtlgrm')
api.add_resource(TestInoEndpoint, '/testino')


def start_server():
    app.run(host='0.0.0.0', port=config.HTTP_PORT)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.HTTP_PORT)
