# Benchmark example

import couenne, lgo
from util import Config, load_index

inputs = load_index('casado', 'hansen')

# Timeout in seconds
timeout = 60

configs = [
  Config('minos'),
  Config('baron'),
  Config('couenne', couenne.options()),
  Config('lgo', {'opmode': lgo.LOCAL_SEARCH_MODE}, suffix='local-search'),
  Config('lgo', {'opmode': lgo.MULTISTART_MODE}, suffix='multistart')
]
