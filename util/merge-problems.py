#!/usr/bin/env python

from __future__ import print_function
import util

def print_ast(nodes):
  for node in nodes:
    print(node)

models = util.get_models('casado', 'hansen')
for m1 in models:
  for m2 in models:
    print(m1, m2)
    print_ast(util.merge_models(m1, m2))
