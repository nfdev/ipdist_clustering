"""
Loader Class
"""
from node import Node, NodeTree


def load(fname):
    datadict = {}

    lines = open(fname, 'r')
    for line in lines:
        line = line.rstrip()
        (nodeip, distip) = line.split(',')
        if nodeip in datadict:
            datadict[nodeip][distip] = 1
        else:
            datadict[nodeip] = {distip: 1}
    lines.close()

    nodetree = NodeTree()
    for nodeip in datadict.keys():
        node = Node(nodeips=[nodeip], distips=datadict[nodeip])
        nodetree.append(node)

    return nodetree
