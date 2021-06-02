import copy
import json


def get_format_str(value):
    return str(value) if value > 9 else "0" + str(value)


def format_branches(branches: dict):
    for key in [*branches]:
        if key == 0:
            branches.update({'out': branches.get(0)})
            del branches[key]
        elif type(key) == str:
            continue
        else:
            branches.update({f"s{get_format_str(key)}": branches.get(key)})
            del branches[key]


def get_week_day(value: str):
    days = [int(x) for x in value.split(',')]
    days.sort()
    bit_array = '0'
    for day in range(1, 8):
        bit_array = bit_array + '1' if day in days else bit_array + '0'
    return int(bit_array, 2).to_bytes(1, 'big').hex()


def get_format_json(raw_string: str):
    res = raw_string.replace("'", '"').replace('\\', '')
    return json.loads(res)

if __name__ == '__main__':
    print(get_week_day('1,2,4,6,7'))
