"""
Node Class
"""

import copy


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


class NodeTree():
    def __init__(self):
        self.nodetree = [{'distance': 0, 'nodelist': []}]

    def append(self, node):
        self.nodetree[0]['nodelist'].append(node)

    def _clustering(self, nodelist):
        num = len(nodelist)
        mindist = float("inf")
        mini = None
        minj = None
        for i in range(0, num):
            for j in range(i + 1, num):
                dist = nodelist[i].distance(nodelist[j])
                if mindist > dist:
                    (mini, minj) = (i, j)
                    mindist = dist

        if not mindist == float("inf"):
            nodelist_out = copy.copy(nodelist)
            nodej = nodelist_out.pop(minj)
            nodei = nodelist_out.pop(mini)
            nodeij = nodei.merge(nodej)
            nodelist_out.append(nodeij)
            return {'distance': mindist, 'nodelist': nodelist_out}
        else:
            return None

    def clustering(self):
        while True:
            nexttree = self._clustering(self.nodetree[-1]['nodelist'])

            if nexttree is None:
                break
            else:
                self.nodetree.append(nexttree)

        self.nodetrace()

    def _nodetrace(self, nodeip, nodelist):
        for node in nodelist:
            if node.hasnodeip(nodeip):
                return node

    def nodetrace(self):
        self.nodeposition = {}
        for node in self.nodetree[0]['nodelist']:
            nodeip = node.nodeips[0]
            self.nodeposition[nodeip] = []

            for branch in self.nodetree:
                nodelist = branch['nodelist']
                self.nodeposition[nodeip].append(self._nodetrace(nodeip, nodelist))

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

if __name__ == '__main__':
    from loader import load
    nodetree = load('./data/sample.dat')
    nodetree.clustering()
