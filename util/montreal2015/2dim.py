# Benchmark for CORS/INFORMS 2015
# This benchmark is run on a collection of 2-dimensional problems generated
# by combining problems from Casado and Hansen.

import ampl, couenne, lgo, os, util
from collections import OrderedDict
from util import Config

def inputs(dirname):
  "Generate inputs by combining problems from Casado and Hansen."
  index = util.load_index('casado', 'hansen').values()
  models = []
  composite_index = OrderedDict()
  for i in range(len(index)):
    for j in range(len(index)):
      if i > j: continue
      m1, m2 = index[i], index[j]
      name = '{:02}-{:02}'.format(i + 1, j + 1)
      filename = name + '.mod'
      models.append(os.path.relpath(filename, util.repo_dir))
      merged_model, best_obj = util.merge_models(m1, m2)
      path = os.path.join(dirname, filename)
      with open(path, 'w') as f:
        ampl.pretty_print(f, merged_model)
      composite_index[name] = {'best_obj': best_obj, 'path': path}
  return composite_index

# Timeout in seconds
timeout = 60

configs = [
  Config('lgo', {'opmode': lgo.LOCAL_SEARCH_MODE}, suffix='local-search'),
  Config('lgo', {'opmode': lgo.MULTISTART_MODE},
         suffix='multistart', on_nl_file=lgo.make_maxfct_setter(2)),
  Config('lgo', {'opmode': lgo.MULTISTART_MODE},
         suffix='multistart-k4', on_nl_file=lgo.make_maxfct_setter(4)),
  Config('minos'),
  Config('baron'),
  Config('couenne', couenne.options())
]
