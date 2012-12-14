# coding: utf-8

class Atom(str):
    def __repr__(self):
        return 'Atom({})'.format(super(Atom, self).__repr__())

class Pid(object):
    def __init__(self, node, node_id, serial, creation):
        self.node = node
        self.node_id = node_id
        self.serial = serial
        self.creation = creation

    def __repr__(self):
        return '{node}|<{creation}.{node_id}.{serial}>'.format(
            node=self.node, node_id=self.node_id,
            serial=self.serial, creation=self.creation
        )
