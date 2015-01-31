#!/usr/bin/env python

import loader


nodetree = loader.load('./data/sample_isolated.dat')

nodetree.clustering()
nodetree.show_top()
