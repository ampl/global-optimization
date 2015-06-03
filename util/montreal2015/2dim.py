# Benchmark for CORS/INFORMS 2015
# This benchmark is run on a collection of 2-dimensional problems generated
# by combining problems from Casado and Hansen.

import couenne, lgo
from util import Config, get_problem_combinator, load_index

inputs = get_problem_combinator(load_index('casado', 'hansen'), 2)

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
