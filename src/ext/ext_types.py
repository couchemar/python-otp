# coding: utf-8

class Atom(str):
    def __repr__(self):
        return 'Atom({})'.format(super(Atom, self).__repr__())
