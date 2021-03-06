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
    def __init__(self, distance=0, nodelist=[]):
        self.nodelists = [{'distance': distance, 'nodelist': nodelist}]

    def addnode(self, node):
        self.nodelists[0]['nodelist'].append(node)

    def rough_clustering(self):
        nodelist = copy.copy(self.nodelists[0]['nodelist'])
        isolatelist = []

        while len(nodelist) >= 2:
            node1 = nodelist.pop(0)
            nodelist_tmp = []
            while len(nodelist) >= 1:
                node2 = nodelist.pop(0)
                dist = node1.distance(node2)

                if not dist == float("inf"):
                    node3 = node1.merge(node2)
                    nodelist = [node3] + nodelist_tmp + nodelist
                    break
                else:
                    nodelist_tmp.append(node2)

                sys.stderr.write("\rrough_clustering| %05d-%05d %f"
                                 % (len(isolatelist),
                                    len(nodelist) + len(nodelist_tmp), dist))
            else:
                isolatelist.append(node1)
                nodelist = nodelist_tmp
        else:
            isolatelist += nodelist

        print ""
        return isolatelist

    def clustering(self):
        isolatelist = []
        nodelist = copy.copy(self.nodelists[0]['nodelist'])

        while len(self.nodelists[-1]['nodelist']) > 1:
            num = len(nodelist)
            mindist = float("inf")
            minnode1 = None
            minnode2 = None
            isolated = False

            for i in range(0, num):
                for j in range(i + 1, num):
                    dist = nodelist[i].distance(nodelist[j])
                    if mindist > dist:
                        (minnode1, minnode2) = (nodelist[i], nodelist[j])
                        mindist = dist
                    if dist == 0:
                        break
                else:
                    if i is 1:
                        isolated = (mindist == float("inf"))
                    continue
                break

            if isolated:
                isolatelist.append(nodelist.pop(0))

            if not mindist == float("inf"):
                node1 = nodelist.pop(nodelist.index(minnode1))
                node2 = nodelist.pop(nodelist.index(minnode2))
                node3 = node1.merge(node2)
                nodelist.insert(0, node3)
                self.nodelists.append(
                    {'distance': mindist, 'nodelist': nodelist + isolatelist})
            else:
                break

            sys.stderr.write("\rclustering| %05d-%05d %f"
                             % (len(self.nodelists),
                                len(nodelist), mindist))
        print ""

        self.nodetrace()

    def _nodetrace(self, nodeip, nodelist):
        for node in nodelist:
            if node.hasnodeip(nodeip):
                return node

    def nodetrace(self):
        self.nodeposition = {}
        for node in self.nodelists[0]['nodelist']:
            nodeip = node.nodeips[0]
            self.nodeposition[nodeip] = []

            for nodelistdict in self.nodelists:
                nodelist = nodelistdict['nodelist']
                self.nodeposition[nodeip].append(self._nodetrace(nodeip, nodelist))

    def distsearch(self, ip):
        for nodelistdict in self.nodelists:
            for node in nodelistdict['nodelist']:
                if ip in node.distips:
                    node.show()

    def show_top(self):
        nodelist = self.nodelists[-1]['nodelist']
        [node.show() for node in nodelist]

    def show_hight(self, hight):
        level = len(self.nodelists)
        while level > 0:
            level -= 1
            distance = self.nodelists[level]['distance']
            if distance < hight:
                nodelist = self.nodelists[level]['nodelist']
                [node.show() for node in nodelist]
                break

    def show_level(self, level):
        nodelist = self.nodelists[level]['nodelist']
        [node.show() for node in nodelist]

    def branch_top(self):
        return self.nodelists[-1]['nodelist']

    def branch_hight(self, hight):
        level = len(self.nodelists)
        while level > 0:
            level -= 1
            distance = self.nodelists[level]['distance']
            if distance < hight:
                return self.nodelists[level]['nodelist']

    def branch_level(self, level):
        return self.nodelists[level]['nodelist']

if __name__ == '__main__':
    from loader import load
    nodetree = load('./data/sample.dat')
    nodetree.clustering()
