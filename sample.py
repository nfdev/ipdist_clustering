#!/usr/bin/env python

import loader


nodetree = loader.load('./data/sample.dat')

nodetree.clustering()
nodetree.show_top()
