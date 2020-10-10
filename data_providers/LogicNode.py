class LogicNode:
    def __init__(self, node_type,logic_type=None, link1=None, link2=None, data=None):
        self.link1 = link1
        self.link2 = link2
        self.node_type = node_type
        self.logic_type = logic_type
        self.data = data
