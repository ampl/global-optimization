#!/usr/bin/env python

from __future__ import print_function
import util

models = util.get_models('casado', 'hansen')
for i in range(len(models)):
  for j in range(len(models)):
    m1, m2 = models[i], models[j]
    print(m1, m2)
    with open('{:02}-{:02}.mod'.format(i, j), 'w') as f:
      f.write(str(util.merge_models(m1, m2)))
