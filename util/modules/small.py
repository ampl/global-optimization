# Small benchmark for CORS/INFORMS 2015

import lgo
from util import Config, files, load_index

models = files('', '''
  blend
  braninu  # branin1 in GOMODELS
  camel1u  # camel1 in GOMODELS
  chemeq
  chi
  gold     # goldstein1 in GOMODELS
  gridneta
  griewank
  hs105
  hs106
  hs109
  hs111
  hs112
  hs114
  hs116
  hs15a
  hs23
  hs35
  hs44
  hs5
  hs54
  hs6
  hs62
  hs64
  hs8
  hs87
  kowalik
  levy3
  ljcluster
  osborne1
  p2gon
  pgon
  powell
  price
  qb2
  rosenbr
  s324
  s383
  schwefel
  shekel
  steenbre
  tre
  weapon
  ''')

inputs = load_index('nlmodels')
for model in inputs.keys():
  if model not in models:
    del inputs[model]
inputs.update(load_index('jdp'))

# Timeout in seconds
timeout = 60

configs = [
  Config('knitro', {'feastol': 1e-8}),
  Config('lgo', {'opmode': lgo.LOCAL_SEARCH_MODE}, suffix='local-search'),
  Config('lgo', {'opmode': lgo.MULTISTART_MODE}, suffix='multistart',
         on_nl_file=lgo.make_maxfct_setter(2))
]
