from node import Node

from tests import _BaseErlangTestCase


if __name__ == '__main__':
     node = Node('test', 'secret', 9999)
     node.start()
     node.connect_node('erl1')
     node.join(1000)


