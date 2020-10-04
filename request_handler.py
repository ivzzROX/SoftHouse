# element = {0001:  'start':    10}
#            SN     operation   value
# 1 - start
# 2 - start_not
# 3 - or
# 4 - and
# 5 - or_not
# 6 - and_not
import time
from flask import jsonify, request, Response
from flask_restful import Resource

from config import sensor_type
from db import Sensors, Devices


class TestEndpoint(Resource):
    @staticmethod
    def get():
        return jsonify({
            "OUT":
                {
                    "brch":
                        [
                            "{out: 3}", "{s01: 3}", "{s02: 3}", "{s03: 3}"
                        ],
                    "out":
                        [
                            "{0A02: 1: 12}", "{0A03: 4: 12}", "{s01: 4}", "{s02, 6}"
                        ],
                    "s01":
                        [
                            "{0A03: 1: 12}", "{s03: 4}", "{0A07: 3: 12}"
                        ],
                    "s02":
                        [
                            "{0A03: 1: 12}", "{0A05: 4: 12}", "{s03: 4}"
                        ],
                    "s03":
                        [
                            "{0A03: 1: 12}", "{0A05: 4: 12}", "{0A07: 3: 12}"
                        ]
                }
        })


class TestTimeEndpoint(Resource):
    @staticmethod
    def get():
        return jsonify({
            "OUT":
                {
                    "brch":
                        [
                            "{out: 4}", "{s01: 3}", "{s02: 3}", "{s03: 3}", "{t01: 09:30-10:00}", "{t02: 12:45-23:50}",
                            "{w01:6B}"
                        ],
                    "out":
                        [
                            "{0C02: 2: 48}", "{0004: 4: 256}", "{s01: 6}", "{s02, 3}"
                        ],
                    "s01":
                        [
                            "{0003: 2: 14}", "{s03: 6}", "{0C07: 3: 56}"
                        ],
                    "s02":
                        [
                            "{0003: 2: 14}", "{00X5: 4: 56}", "{s03: 4}"
                        ],
                    "s03":
                        [
                            "{0003: 2: 24}", "{00X5: 5: 55}", "{t01: 4}"
                        ]
                }
        })


class TestTelegramEndpoint(Resource):
    @staticmethod
    def get():
        return jsonify({
            "OUT":
                {
                    "brch":
                        [
                            "{g01: 445}"
                        ]
                }
        })


class TestInoEndpoint(Resource):
    @staticmethod
    def get():
        return jsonify({
            "OUT":
                {
                    "brch":
                        [
                            "{i01: 9}"
                        ]
                }
        })


class TestPmoEndpoint(Resource):
    @staticmethod
    def get():
        return jsonify({
            "OUT":
                {
                    "brch":
                        [
                            "{p01: 9}"
                        ]
                }
        })


class TestTelegramDataEndpoint(Resource):
    @staticmethod
    def get():
        return jsonify({
            "TLGRM":
                [
                    "{445: 1}", "{356: 0}"
                ]
        })


class TimeStamp(Resource):
    @staticmethod
    def get():
        out = f'tm:{int(time.time())},tz:{3}'
        return out


class RegisterSensors(Resource):
    @staticmethod
    def post():
        sensors = request.get_json(force=True).get('SENSOR')
        if sensors is None:
            return Response('Not valid JSON (SENSOR field is not exist)', status=400)
        for sensor in sensors:
            serial_number = sensor.get('SN')
            if serial_number is None:
                return Response('Not valid JSON (SN field is not exist)', status=400)
            type_int = sensor.get('TYPE')
            if type_int is None:
                return Response('Not valid JSON (TYPE field is not exist)', status=400)
            type_hr = sensor_type.get(type_int)
            if type_hr is None:
                return Response(f'Not valid JSON (TYPE {type_int} is not found)', status=400)
            if Sensors.select().where(Sensors.serial_number == serial_number).exists():
                return Response(f'Such serial {serial_number} is already exists', status=400)
            Sensors.create(serial_number=serial_number, type_int=type_int, type_hr=type_hr)


class RegisterDevice(Resource):
    @staticmethod
    def post():
        serial_number = request.get_json(force=True).get('DEVICE').get('SN')
        if serial_number is None:
            return Response('Not valid JSON (SN field is not exist)', status=400)
        if Devices.select().where(Devices.serial_number == serial_number).exists():
            return Response(f'Such serial {serial_number} is already exists', status=400)
        Devices.create(serial_number=serial_number)
