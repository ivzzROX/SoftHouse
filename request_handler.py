# element = {0001:  'start':    10}
#            SN     operation   value
# 1 - start
# 2 - start_not
# 3 - or
# 4 - and
# 5 - or_not
# 6 - and_not
import time

from flask import jsonify
from flask_restful import Resource


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
