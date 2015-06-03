# Benchmark for CORS/INFORMS 2015
# This benchmark is run on a collection of 2-dimensional problems generated
# by combining problems from Casado and Hansen.

import ampl, couenne, itertools, lgo, os, random, util
from collections import OrderedDict
from util import Config

def combine(index, n, num_problems=None):
  """
  Combine *n* problems from *index* to get the given number of combined problems
  selected at random.
  """
  combinations = [i for i in itertools.combinations_with_replacement(range(len(index)), n)]
  if num_problems is None:
    return combinations
  return sorted(random.sample(combinations, num_problems))

def inputs(dirname):
  "Generate inputs by combining problems from Casado and Hansen."
  index = util.load_index('casado', 'hansen').values()
  combinations = combine(index, 2)
  composite_index = OrderedDict()
  for indices in combinations:
    merged_model, best_obj = util.merge_models([index[i] for i in indices])
    name = '-'.join(['{:02}'.format(i + 1) for i in indices])
    filename = name + '.mod'
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
