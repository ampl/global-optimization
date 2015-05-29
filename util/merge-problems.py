#!/usr/bin/env python3
# Merge multiple AMPL problems into a single one.
# For example, two problems
#   minimize o: f1(x);
# and
#   minimize o: f2(x);
# are combined into a single problem
#   minimize o: f1(x1) + f2(x2);

from __future__ import print_function
import ampl, glob

for filename in sorted(glob.glob('../casado/*.mod')):
  with open(filename, 'r') as f:
    print(ampl.parse(f.read(), filename))
