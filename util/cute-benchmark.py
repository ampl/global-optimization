#!/usr/bin/env python

from __future__ import print_function
import glob, os
from util import Benchmark, read_nl_header, repo_dir

# Timeout in seconds
TIMEOUT = 1

LGO_LOCAL_SEARCH_MODE = 0
LGO_MULTISTART_MODE   = 3

models = sorted(glob.glob(os.path.join(repo_dir, 'cute', '*.mod')))
models = [os.path.relpath(m, repo_dir) for m in models]

with Benchmark(log='cute-lgo-local-search.yaml', solver='lgo', timeout=TIMEOUT,
               solver_options={'opmode': LGO_LOCAL_SEARCH_MODE}) as b:
  for model in models:
    print(model)
    b.run(model)

exit(0)

with Benchmark(log='cute-lgo-multistart.yaml', solver='lgo', timeout=TIMEOUT,
                solver_options={'opmode': LGO_MULTISTART_MODE}, on_nl_file=update_options) as b:
  for model in models:
    print(model)
    b.run(model)
