#!/usr/bin/env python
import node
import loader


nodetree = loader.load('./data/sample.dat')

areacluster = nodetree.rough_clustering()

nodetrees = []
for arealist in areacluster:
    nodelist = arealist.nodelist()
    subnodetree = node.NodeTree(nodelist=nodelist)
    subnodetree.clustering()
    nodetrees.append(subnodetree)
