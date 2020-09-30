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


class TimeStamp(Resource):
    @staticmethod
    def get():
        out = f'tm:{int(time.time())},tz:{3}'
        return out
