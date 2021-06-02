class LogicNode:
    def __init__(self, node_id, node_type, logic_type=None, link_from1=None, link_from2=None, link_to=None, data=None,
                 value=None, counter=None, in_type=None):
        self.link_from1 = link_from1
        self.link_from2 = link_from2
        self.link_to = link_to
        self.node_type = node_type
        self.logic_type = logic_type
        self.data = data
        self.node_id = node_id
        self.value = value
        self.counter = counter
        self.in_type = in_type

    def print_val(self):
        return f"link from 1 - {self.link_from1}, link from 2 - {self.link_from2}, link to - {self.link_to},type - {self.node_type}, logic - {self.logic_type}, data - {self.data}, id - {self.node_id}"
