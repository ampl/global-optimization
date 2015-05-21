#!/usr/bin/env python
# Clean AMPL test models by removing script commands such as
# solve and display.

from __future__ import print_function
import os, re, sys

def clean(filename):
  print(filename)
  with open(filename, 'r') as f:
    code = f.read()
  cleaned_code = re.sub(r'^\s*solve\s*;[ \t]*\n?', '', code, flags=re.MULTILINE)
  cleaned_code = re.sub(r'^\s*(display|printf)(\s[^;]+)\s*;[ \t]*\n?', '', cleaned_code, flags=re.MULTILINE)
  if code != cleaned_code:
    with open(filename, 'w') as f:
      f.write(cleaned_code)

for root, dirs, files in os.walk(sys.argv[1]):
  for f in files:
    if f.endswith('.mod'):
      clean(os.path.join(root, f))
