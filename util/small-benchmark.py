#!/usr/bin/env python

from __future__ import print_function
from util import files, Benchmark, read_nl_header

models = files('nlmodels', '''
  blend.mod
  braninu.mod  # branin1.mod in GOMODELS
  camel1u.mod  # camel1.mod in GOMODELS
  chemeq.mod
  chi.mod
  gold.mod     # goldstein1.mod in GOMODELS
  gridneta.mod
  griewank.mod
  hs105.mod
  hs106.mod
  hs109.mod
  hs111.mod
  hs112.mod
  hs114.mod
  hs116.mod
  hs15a.mod
  hs23.mod
  hs35.mod
  hs44.mod
  hs5.mod
  hs54.mod
  hs6.mod
  hs62.mod
  hs64.mod
  hs8.mod
  hs87.mod
  kowalik.mod
  levy3.mod
  ljcluster.mod
  osborne1.mod
  p2gon.mod
  pgon.mod
  powell.mod
  price.mod
  qb2.mod
  rosenbr.mod
  s324.mod
  s383.mod
  schwefel.mod
  shekel.mod
  steenbre.mod
  tre.mod
  weapon.mod
  ''')

models += files('jdp', '''
  jdp1.mod
  jdp2.mod
  jdp3.mod
  jdp4.mod
  ''')

# Timeout in seconds
TIMEOUT = 300

LGO_LOCAL_SEARCH_MODE = 0
LGO_MULTISTART_MODE   = 3

with Benchmark(log='small-knitro.yaml', solver='knitro', timeout=TIMEOUT,
               solver_options={'feastol': 1e-8}) as b:
  for model in models:
    print(model)
    b.run(model)

with Benchmark(log='small-lgo-local-search.yaml', solver='lgo', timeout=TIMEOUT,
                solver_options={'opmode': LGO_LOCAL_SEARCH_MODE}) as b:
  for model in models:
    print(model)
    b.run(model)

def update_options(nl_file):
  header = read_nl_header(nl_file.name)
  maxfct = k * 50 * (header.num_vars + header.num_cons + 2) ** 2
  b.solver_options['g_maxfct'] = maxfct
  b.solver_options['l_maxfct'] = maxfct
  b.solver_options['maxnosuc'] = maxfct

# Run benchmarks with multistart search effort set to 2.
for k in [2]:
  with Benchmark(log='small-lgo-multistart-k{}.yaml'.format(k), solver='lgo', timeout=TIMEOUT,
                 solver_options={'opmode': LGO_MULTISTART_MODE}, on_nl_file=update_options) as b:
    for model in models:
      print(model)
      b.run(model)
