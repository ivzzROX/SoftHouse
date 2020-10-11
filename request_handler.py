# element = {0001:  'start':    10}
#            SN     operation   value
# 1 - start
# 2 - or
# 3 - and
# 4 - xor
# 5 - nor
# 6 - nand
# 7 - xnor
# 8 - not   note: just invert prev value, it doesn`t matter SN or VALUE {ffff: 8: 0}
# constants:
# sensor with address fffe always equal 0
# sensor with address ffff always equal 1


import time
from flask import jsonify, request, Response
from flask_restful import Resource

from config import sensor_type
from data_providers.LogicNode import LogicNode
from db import Sensors, Devices

LOGIC = {"START": 1, "OR": 2, "AND": 3, "XOR": 4, "NOR": 5, "NAND": 6, "XNOR": 7, "NOT": 8}


class TestEndpoint(Resource):
    @staticmethod
    def get():
        return jsonify({
            "OUT":
                {
                    "brch":
                        [
                            "{out: 2}"
                        ],
                    "out":
                        [
                            "{000b: 1: 1}", "{00c4: 3: 70}"
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


def get_longest_branch(node, counter=0):
    if node.node_type == 'OUTPUT':
        return counter
    else:
        return get_longest_branch(node.link_to, counter + 1)


def check_if_in_longest_branch(node, current_node=None):
    if not current_node.link_to:
        return False
    if current_node.node_id == node.node_id:
        return True
    else:
        return check_if_in_longest_branch(node, current_node.link_to)


def form_branch(node, branches, current_branch_id, start_node_for_longest_branch=None):
    if node.node_type == 'OUTPUT':
        branches.update({0: []})
        return form_branch(node.link_from1, branches, current_branch_id=0,  # create initial branch
                           start_node_for_longest_branch=start_node_for_longest_branch)
    if node.link_from1.node_type == 'INPUT' and node.link_from2.node_type == 'INPUT':
        branches.get(current_branch_id).insert(0,
                                               # .insert(0,foo) to insert at the begging of the list due to step-by-step
                                               f'{{{node.link_from2.data}: {LOGIC.get(node.logic_type)}: {node.link_from2.value}}}')  # add second item
        branches.get(current_branch_id).insert(0,
                                               f'{{{node.link_from1.data}: 1: {node.link_from1.value}}}')  # add start
        return branches
    if (node.link_from1.node_type == 'INPUT' and node.link_from2.node_type == 'LOGIC') or (
            node.link_from2.node_type == 'INPUT' and node.link_from1.node_type == 'LOGIC'):  # TODO refactor for smaller if
        # insert into branch input value and go next logic node
        if node.link_from1.node_type == 'INPUT':
            branches.get(current_branch_id).insert(0,
                                                   f'{{{node.link_from1.data}: {LOGIC.get(node.logic_type)}: {node.link_from1.value}}}')
            return form_branch(node.link_from2, branches, current_branch_id,
                               start_node_for_longest_branch=start_node_for_longest_branch)
        else:
            branches.get(current_branch_id).insert(0,
                                                   f'{{{node.link_from2.data}: {LOGIC.get(node.logic_type)}: {node.link_from2.value}}}')
            return form_branch(node.link_from1, branches, current_branch_id,
                               start_node_for_longest_branch=start_node_for_longest_branch)
    if node.link_from1.node_type == 'LOGIC' and node.link_from2.node_type == 'LOGIC':
        branches.get(current_branch_id).insert(0,
                                               f'{{s{current_branch_id + 1}: {LOGIC.get(node.logic_type)}}}')  # add branch item to list
        branches.update({len(branches.values()): []})  # create new branch
        if check_if_in_longest_branch(node.link_from1,
                                      start_node_for_longest_branch):  # if in longest branch create new branch for another node and insert current
            form_branch(node.link_from1, branches, current_branch_id,
                        start_node_for_longest_branch=start_node_for_longest_branch)
            form_branch(node.link_from2, branches, current_branch_id + 1,
                        start_node_for_longest_branch=start_node_for_longest_branch)
        else:
            form_branch(node.link_from2, branches, current_branch_id,
                        start_node_for_longest_branch=start_node_for_longest_branch)
            form_branch(node.link_from1, branches, current_branch_id + 1,
                        start_node_for_longest_branch=start_node_for_longest_branch)


def get_branches(nodes, start_node_for_longest_branch):
    out = nodes.get('out')
    branches = {}
    form_branch(out, branches, 0, start_node_for_longest_branch)
    return branches


class GetUserLogic(Resource):
    @staticmethod
    def post():
        # print(request.get_json(force=True))
        objects = request.get_json(force=True).get('objects')
        links = request.get_json(force=True).get('links')
        nodes = []
        nodes_id_dict = {}
        for _object in objects:
            node = LogicNode(node_id=_object.get('id'), node_type=_object.get('type'),
                             logic_type=_object.get('logicType'),
                             data=_object.get('t'), value=_object.get('v'))
            nodes.append(node)

            nodes_id_dict.update({node.node_id: node})
            if node.node_type == 'OUTPUT':
                nodes_id_dict.update({'out': node})
        del objects
        del _object
        for node in nodes:
            # if node.node_type == 'LOGIC':
            print('1')
            for link in links:
                if node.node_id == link.get('to').get('id'):
                    if node.node_type == 'OUTPUT':
                        node.link_from1 = nodes_id_dict.get(link.get('from').get('id'))
                        break
                    node_link = nodes_id_dict.get(link.get('from').get('id'))
                    if not node.link_from1:
                        node.link_from1 = node_link
                    else:
                        node.link_from2 = node_link

                elif node.node_id == link.get('from').get('id'):
                    node.link_to = nodes_id_dict.get(link.get('to').get('id'))
        start_node_for_longest_branch = None
        counter = 0
        for node in nodes:
            if node.node_type == 'INPUT':
                current_counter = get_longest_branch(node)
                if current_counter > counter:
                    counter = current_counter
                    start_node_for_longest_branch = node
            print(node.print_val() + '\n')
        print(get_branches(nodes_id_dict, start_node_for_longest_branch))
