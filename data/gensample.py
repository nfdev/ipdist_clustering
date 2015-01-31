#!/usr/bin/env python

"""
Generate Dummy Data
"""

import random
import math

groupnum = 100
nodemax = 200
distmax = 200
gentype = 'isolated'  # flat, n-dist

if groupnum > 255 or nodemax > 255 or distmax > 256:
    print "groupnum, nodemax, distmax should be less than 256"
    exit

# Set Variance
if gentype is 'n-dist':
    nodenums = [min(int(math.ceil(abs(random.gauss(0, nodemax / 3)) + 0.1)), nodemax) for x in range(0, groupnum)]
    distnums = [min(int(math.ceil(abs(random.gauss(0, distmax / 3)) + 0.1)), distmax) for x in range(0, groupnum)]
elif gentype is 'isolated':
    nodenums = [1] * (groupnum / 2)
    nodenums += [min(int(math.ceil(abs(random.gauss(0, nodemax / 3)) + 0.1)), nodemax)
                 for x in range(groupnum / 2, groupnum)]
    distnums = [min(int(math.ceil(abs(random.gauss(0, distmax / 3)) + 0.1)), distmax)
                for x in range(0, groupnum)]
else:
    nodenums = [nodemax] * groupnum
    distnums = [distmax] * groupnum

# Set IP Address

fsample = open('./sample_long.dat', 'w')
for g in range(0, groupnum):
    for i in range(0, nodenums[g]):
        nodeip = "172.16.%d.%d" % (g, i)
        for j in range(0, distnums[g]):
            distip = "10.%d.0.%d" % (g, j)
            if random.random() >= 0.5:
                fsample.write("%s,%s\n" % (nodeip, distip))
fsample.close()

fparam = open('./nodenums_long.dat', 'w')
fparam.write(','.join(map(str, nodenums)))
fparam.close()
fparam = open('./distnums_long.dat', 'w')
fparam.write(','.join(map(str, distnums)))
fparam.close()
