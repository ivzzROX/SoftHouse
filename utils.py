import copy


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
