"""
Node Class
"""

import copy
import sys


class Node():
    def __init__(self, name="not defined", nodeips=[], distips={}):
        self.name = name
        self.nodeips = nodeips
        self.distips = distips
        self.nodes = []

    def onewaydistance(self, node):
        distance = 0
        for distip in self.distips.keys():
            if not node.hasdistip(distip):
                distance += self.weight(distip)
        if distance == len(self.distips):
            return float("inf")
        else:
            return distance

    def distance(self, node):
        return self.onewaydistance(node) + node.onewaydistance(self)

    def add(self, node):
        selfnodes = len(self.nodeips)
        nodenodes = len(node.nodeips)
        self.nodeips += node.nodeips

        self.nodes.append(node)

        ips = self.distips.keys() + node.distips.keys()
        seen = set()
        seen_add = seen.add
        distips = [x for x in ips if x not in seen and not seen_add(x)]

        for ip in distips:
            self.distips[ip] = float((self.weight(ip) * selfnodes + node.weight(ip) * nodenodes)) / (selfnodes + nodenodes)

    def merge(self, node):
        combined = Node(nodeips=[], distips={})
        combined.add(self)
        combined.add(node)
        return combined

    def hasdistip(self, ip):
        return ip in self.distips

    def hasnodeip(self, ip):
        return ip in self.nodeips

    def weight(self, ip):
        if ip in self.distips:
            return self.distips[ip]
        else:
            return 0

    def setname(self, nodename):
        self.nodename = nodename

    def show(self):
        print "branchname: %s" % self.name
        print "    nodeip: "
        for ip in self.nodeips:
            print "          %s" % (ip)
        print "    distip: "
        for ip in self.distips.keys():
            print "          %s: %s" % (ip, self.weight(ip))

    def show_branch(self):
        [node.show() for node in self.nodes]

    def branch(self):
        return self.nodes

    def nodelist(self):
        nodelist = []

        if len(self.nodes) == 0:
            nodelist.append(self)
        else:
            for node in self.nodes:
                nodelist += node.nodelist()

        return nodelist


class NodeTree():
    def __init__(self, distance=0, nodelist=[], isolatelist=[]):
        self.distance = distance
        self.nodelist = nodelist
        self.isolatelist = isolatelist

    def addnode(self, node):
        self.nodelist.append(node)

    def clustering(self):
        nodelist = copy.copy(self.nodelist)
        self.isolatelistd = []
        (minnode1, minnode2) = (None, None)

        while len(nodelist) >= 2:
            node1 = nodelist.pop()
            mindist = float("inf")
            nodelist_tmp = []
            while len(nodelist) >= 1:
                node2 = nodelist.pop()
                dist = node1.distance(node2)
                sys.stderr.write("\r %05d-%05d %f" % (len(self.isolatelistd), len(nodelist), dist))
                if not dist < mindist:
                    mindist = dist
                    (minnode1, minnode2) = (node1, node2)
                elif mindist == 0:
                    break
                nodelist_tmp.append(node2)
            else:
                self.isolatelistd.append(node1)
                nodelist = nodelist_tmp
        else:
                    node3 = node1.merge(node2)
                    nodelist = nodelist_tmp + nodelist + [node3]
                    break
            self.isolatelistd += nodelist

        return self.isolatelistd

    def _nodetrace(self, nodeip, nodelist):
        for node in nodelist:
            if node.hasnodeip(nodeip):
                return node

    def nodetrace(self):
        self.nodeposition = {}
        for node in self.nodetree[0]['nodelist']:
            nodeip = node.nodeips[0]
            self.nodeposition[nodeip] = []

            for nodelistdict in self.nodetree:
                nodelist = nodelistdict['nodelist']
                self.nodeposition[nodeip].append(self._nodetrace(nodeip, nodelist))

    def distsearch(self, ip):
        for nodelistdict in self.nodetree:
            for node in nodelistdict['nodelist']:
                if ip in node.distips:
                    node.show()

    def show_top(self):
        nodelist = self.nodetree[-1]['nodelist']
        [node.show() for node in nodelist]

    def show_hight(self, hight):
        level = len(self.nodetree)
        while level > 0:
            level -= 1
            distance = self.nodetree[level]['distance']
            if distance < hight:
                nodelist = self.nodetree[level]['nodelist']
                [node.show() for node in nodelist]
                break

    def show_level(self, level):
        nodelist = self.nodetree[level]['nodelist']
        [node.show() for node in nodelist]

    def branch_top(self):
        return self.nodetree[-1]['nodelist']

    def branch_hight(self, hight):
        level = len(self.nodetree)
        while level > 0:
            level -= 1
            distance = self.nodetree[level]['distance']
            if distance < hight:
                return self.nodetree[level]['nodelist']

    def branch_level(self, level):
        return self.nodetree[level]['nodelist']


class RoughNodeTree(NodeTree):
    def clustering(self):
        nodelist = copy.copy(self.nodelist)
        isolatelist = []

        while len(nodelist) >= 2:
            node1 = nodelist.pop()
            nodelist_tmp = []
            while len(nodelist) >= 1:
                node2 = nodelist.pop()
                dist = node1.distance(node2)
                sys.stderr.write("\r %05d-%05d %f" % (len(isolatelist), len(nodelist), dist))
                if not dist == float("inf"):
                    node3 = node1.merge(node2)
                    nodelist = nodelist_tmp + nodelist + [node3]
                    break
                else:
                    nodelist_tmp.append(node2)
            else:
                isolatelistd.append(node1)
                nodelist = nodelist_tmp
        else:
            isolatelistd += nodelist

        return NodeTree(isolatelist=self.isolatelistd)

if __name__ == '__main__':
    from loader import load
    nodetree = load('./data/sample.dat')
    nodetree.clustering()
