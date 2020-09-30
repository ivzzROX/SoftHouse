# element = {2:'or'}
# 2 - start
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
                            "{2: 2}", "{4: 4}", "{s01: 4}", "{s02, 6}"
                        ],
                    "s01":
                        [
                            "{3: 2}", "{s03: 4}", "{7: 3}"
                        ],
                    "s02":
                        [
                            "{3: 2}", "{5: 4}", "{s03: 4}"
                        ],
                    "s03":
                        [
                            "{3: 2}", "{5: 4}", "{7: 3}"
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
                            "{2: 2}", "{4: 4}", "{s01: 6}", "{s02, 3}"
                        ],
                    "s01":
                        [
                            "{3: 2}", "{s03: 6}", "{7: 3}"
                        ],
                    "s02":
                        [
                            "{3: 2}", "{5: 4}", "{s03: 4}"
                        ],
                    "s03":
                        [
                            "{3: 2}", "{5: 5}", "{t01: 4}"
                        ]
                }
        })


class TestPmoEndpoint(Resource):
    @staticmethod
    def get():
        return jsonify({
            "OUT":
                {
                    "pmo": 8
                }
        })


class TimeStamp(Resource):
    @staticmethod
    def get():
        out = f'tm:{int(time.time())},tz:{3}'
        return out
