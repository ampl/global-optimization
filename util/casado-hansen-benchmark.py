#!/usr/bin/env python

from __future__ import print_function
import lgo, util

# Timeout in seconds
TIMEOUT = 60

class Config:
  def __init__(self, solver, solver_options={}, suffix=None, on_nl_file=None):
    self.solver = solver
    self.solver_options = solver_options
    self.suffix = suffix
    self.on_nl_file = on_nl_file

configs = [
  Config('minos'),
  Config('baron'),
  Config('couenne'),
  Config('lgo', {'opmode': lgo.LOCAL_SEARCH_MODE}, 'local-search'),
  Config('lgo', {'opmode': lgo.MULTISTART_MODE}, 'multistart', lgo.make_maxfct_setter(2))
]

models = util.load_index('casado', 'hansen').values()
for c in configs:
  log = 'casado-hansen-' + c.solver
  if c.suffix:
    log += '-' + c.suffix
  with util.Benchmark(log=log + '.yaml', timeout=TIMEOUT, solver=c.solver,
                      solver_options=c.solver_options, on_nl_file=c.on_nl_file) as b:
    for model in models:
      print(model['path'])
      b.run(model['path'])
