#!/usr/bin/env python

from __future__ import print_function
import util

index = util.load_index('casado', 'hansen').values()
for i in range(len(index)):
  for j in range(len(index)):
    m1, m2 = index[i], index[j]
    print(m1['path'], m2['path'])
    with open('{:02}-{:02}.mod'.format(i, j), 'w') as f:
      f.write(str(util.merge_models(m1, m2)))
