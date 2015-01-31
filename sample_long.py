#!/usr/bin/env python
import loader
import node


nodetree = loader.load('./data/sample_long.dat')

isolatedlist = nodetree.rough_clustering()

nodetrees = [node.NodeTree(nodelist=nl.nodelist()) for nl in isolatedlist]

for nodetree in nodetrees:
    nodetree.clustering()
    nodetree.show_top()
