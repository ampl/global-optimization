#!/usr/bin/env python

from __future__ import print_function
import glob, os
from util import Benchmark, read_nl_header, repo_dir

# Timeout in seconds
TIMEOUT = 1

LGO_LOCAL_SEARCH_MODE = 0
LGO_MULTISTART_MODE   = 3

models = []
for subdir in ['cute', 'jdp', 'nlmodels']:
  models += glob.glob(os.path.join(repo_dir, subdir, '*.mod'))
models = sorted([os.path.relpath(m, repo_dir) for m in models])

with Benchmark(log='large-knitro.yaml', timeout=TIMEOUT,
               solver='knitro', solver_options={'feastol': 1e-8}) as b:
  for model in models:
    print(model)
    b.run(model)

with Benchmark(log='large-baron.yaml', timeout=TIMEOUT, solver='baron') as b:
  for model in models:
    print(model)
    b.run(model)

with Benchmark(log='large-lgo-local-search.yaml', timeout=TIMEOUT,
               solver='lgo', solver_options={'opmode': LGO_LOCAL_SEARCH_MODE}) as b:
  for model in models:
    print(model)
    b.run(model)

def update_options(nl_file):
  header = read_nl_header(nl_file.name)
  maxfct = k * 50 * (header.num_vars + header.num_cons + 2) ** 2
  b.solver_options['g_maxfct'] = maxfct
  b.solver_options['l_maxfct'] = maxfct
  b.solver_options['maxnosuc'] = maxfct

k = 2
with Benchmark(log='large-lgo-multistart.yaml', timeout=TIMEOUT,
               solver='lgo', solver_options={'opmode': LGO_MULTISTART_MODE},
               on_nl_file=update_options) as b:
  for model in models:
    print(model)
    b.run(model)
