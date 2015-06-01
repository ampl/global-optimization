#!/usr/bin/env python

from __future__ import print_function
import lgo, os, util, yaml

# Timeout in seconds
TIMEOUT = 60

class Config:
  def __init__(self, solver, solver_options={}, suffix=None, on_nl_file=None):
    self.solver = solver
    self.solver_options = solver_options
    self.suffix = suffix
    self.on_nl_file = on_nl_file

configs = [
  Config('lgo', {'opmode': lgo.LOCAL_SEARCH_MODE}, 'local-search'),
  Config('lgo', {'opmode': lgo.MULTISTART_MODE}, 'multistart', lgo.make_maxfct_setter(2)),
  Config('minos'),
  Config('baron'),
  Config('couenne')
]

index = util.load_index('casado', 'hansen').values()[:4]
models = []
composite_index = {}
for i in range(len(index)):
  for j in range(len(index)):
    if i > j: continue
    m1, m2 = index[i], index[j]
    print('Merging {} and {}'.format(m1['path'], m2['path']))
    name = '{:02}-{:02}'.format(i + 1, j + 1)
    filename = name + '.mod'
    models.append(os.path.relpath(filename, util.repo_dir))
    merged_model, best_obj = util.merge_models(m1, m2)
    with open(filename, 'w') as f:
      f.write(str(merged_model))
    composite_index[name] = {'best_obj': best_obj}

with open('index.yaml', 'w') as f:
  f.write(yaml.dump(composite_index))

for c in configs:
  log = 'composite-' + c.solver
  if c.suffix:
    log += '-' + c.suffix
  with util.Benchmark(log=log + '.yaml', timeout=TIMEOUT, solver=c.solver,
                      solver_options=c.solver_options, on_nl_file=c.on_nl_file) as b:
    for model in models:
      print(model)
      b.run(model)
