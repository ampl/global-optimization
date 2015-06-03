# Large benchmark for CORS/INFORMS 2015

import couenne, lgo
from util import Config, load_index

inputs = load_index('cute', 'jdp', 'nlmodels')

# Timeout in seconds
timeout = 300

configs = [
  Config('minos'),
  Config('baron'),
  Config('couenne', couenne.options()),
  Config('lgo', {'opmode': lgo.LOCAL_SEARCH_MODE}, suffix='local-search'),
  Config('lgo', {'opmode': lgo.MULTISTART_MODE}, suffix='multistart',
         on_nl_file=lgo.make_maxfct_setter(2))
]
