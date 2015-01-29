"""
Node Class
"""


class Node():
    left_branch = None
    right_branch = None

    def __init__(self, name="nod defined", nodeips=[], distips={}):
        self.name = name
        self.nodeips = nodeips
        self.distips = distips

    def onewaydistance(self, node):
        distance = 0
        for distip in self.distips.keys():
            if not node.hasdistip(distip):
                distance += self.weight(distip)

    def distance(self, node):
        return self.onewaydistance(node) + node.onewaydistance(self)

    def add(self, node):
        selfnodes = len(self.nodeips)
        nodenodes = len(node.nodeips)
        self.nodeips += node.nodeips

        ips = self.distips.keys() + node.distips.keys()
        seen = set()
        seen_add = seen.add
        distips = [x for x in ips if x not in seen and not seen_add(x)]

        for ip in distips:
            self.distips[ip] = (self.weight(ip) * selfnodes + node.weight(ip) * nodenodes) / (selfnodes + nodenodes)

    def merge(self, node):
        combined = Node()
        combined.add(self)
        combined.add(node)
        return combined

    def hasdistip(self, ip):
        return ip in self.distips

    def weight(self, ip):
        if ip in self.distips:
            return self.distips[ip]
        else:
            return 0

    def setname(self, nodename):
        self.nodename = nodename

    def show(self):
        print "branchname: %s" % self.name
        print "    distip: "
        for ip in self.distips.keys:
            print "          %s: %s" % [ip, self.weight(ip)]
