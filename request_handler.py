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

counters = 0  # TODO refactor for several requests at same time
rs_triggers = 0
t_triggers = 0
delays = 0


class TestEndpoint(Resource):
    @staticmethod
    def get():
        return jsonify({
            "OUT":
                {
                    "brch":
                        [
                            "{out: 1}", "{s01: 1}", "{c01: s01: 5}"
                        ],
                    "out":
                        [
                            "{c01: 1}"
                        ],
                    "s01":
                        [
                            "{000b: 1: 1}"
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
    global counters
    if node.node_type == 'OUTPUT':
        branches.update({0: []})
        return form_branch(node.link_from1, branches, current_branch_id=0,  # create initial branch
                           start_node_for_longest_branch=start_node_for_longest_branch)
    if node.logic_type == 'CNTR':
        new_branch_id = len(branches.values())
        branches.update({new_branch_id: []})  # create new branch

        return form_branch(node.link_from1, branches, new_branch_id,
                           start_node_for_longest_branch=start_node_for_longest_branch)

        # new_branch_id = len(branches.values())
        # branches.update({new_branch_id: []})

        # branches.get(0).append(
        #     f'{{c{counters if counters < 9 else "0" + str(counters)}: s{new_branch_id if new_branch_id < 9 else "0" + str(new_branch_id)}: {node.counter}}}')

    if node.link_from1.node_type == 'INPUT' and node.link_from2.node_type == 'INPUT':
        print(node)
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
        new_branch_id = len(branches.values())
        branches.update({new_branch_id: []})  # create new branch
        if node.link_from1.logic_type == 'CNTR' or node.link_from2.logic_type == 'CNTR':
            branches.get(0).append(
                f'{{c{counters if counters < 9 else "0" + str(counters)}: {LOGIC.get(node.logic_type)}}}')
            branches.get(current_branch_id).insert(0,
                                                   f'{{s{len(branches.values())}: {LOGIC.get(node.logic_type)}}}')  # add branch item to list

            return form_branch(node.link_from1, branches, new_branch_id,
                               start_node_for_longest_branch=start_node_for_longest_branch)
        branches.get(current_branch_id).insert(0,
                                               f'{{s{len(branches.values())}: {LOGIC.get(node.logic_type)}}}')  # add branch item to list

        if check_if_in_longest_branch(node.link_from1,
                                      start_node_for_longest_branch):  # if in longest branch create new branch for another node and insert current
            form_branch(node.link_from1, branches, current_branch_id,
                        start_node_for_longest_branch=start_node_for_longest_branch)
            form_branch(node.link_from2, branches, new_branch_id,
                        start_node_for_longest_branch=start_node_for_longest_branch)
        else:
            form_branch(node.link_from2, branches, current_branch_id,
                        start_node_for_longest_branch=start_node_for_longest_branch)
            form_branch(node.link_from1, branches, new_branch_id,
                        start_node_for_longest_branch=start_node_for_longest_branch)


def get_branches(nodes, start_node_for_longest_branch):
    out = nodes.get('out')
    branches = {}
    global counters
    global rs_triggers
    global t_triggers
    global delays
    counters = 0
    rs_triggers = 0
    t_triggers = 0
    delays = 0
    form_branch(out, branches, 0, start_node_for_longest_branch)
    return branches


class GetUserLogic(Resource):
    @staticmethod
    def post():
        print(request.get_json(force=True))
        objects = request.get_json(force=True).get('objects')
        links = request.get_json(force=True).get('links')
        nodes = []
        nodes_id_dict = {}
        for _object in objects:
            node = LogicNode(node_id=_object.get('id'),
                             node_type=_object.get('type'),
                             logic_type=_object.get('logicType'),
                             data=_object.get('number'),
                             value=_object.get('triggerValue'),
                             counter=_object.get('blockValue'))
            nodes.append(node)
            nodes_id_dict.update({node.node_id: node})
            if node.node_type == 'OUTPUT':
                nodes_id_dict.update({'out': node})
        del objects
        del _object
        for node in nodes:
            # if node.node_type == 'LOGIC':
            for link in links:
                print(link)
                if node.node_id == link.get('blockTo').get('id'):
                    if node.node_type == 'OUTPUT':
                        node.link_from1 = nodes_id_dict.get(link.get('blockFrom').get('id'))
                        break
                    node_link = nodes_id_dict.get(link.get('blockFrom').get('id'))
                    if node.logic_type == 'RS T':
                        if link.get('position') == 1:
                            if node.link_from2:
                                node.link_from2 = node_link.link_from1
                            node.link_from1 = node_link
                    if not node.link_from1:
                        node.link_from1 = node_link
                    else:
                        node.link_from2 = node_link

                elif node.node_id == link.get('blockFrom').get('id'):
                    node.link_to = nodes_id_dict.get(link.get('blockTo').get('id'))
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
