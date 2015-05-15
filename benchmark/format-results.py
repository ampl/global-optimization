#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os, re, sys, yaml
import pandas as pd
from subprocess import Popen, PIPE, STDOUT

repo_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def model_name(path):
  return os.path.splitext(os.path.split(path)[1])[0]

def num_func_evals(result):
  m = re.search(r'(\d+) function (and constraint )?evaluations', result['solve_message'])
  return int(m.group(1)) if m else None

# Read the log and get the number of variables in each problem.
def read_log(filename):
  results = yaml.load(file(filename, 'r'))
  for result in results:
    ampl_filename = os.path.join(repo_dir, result['model'])
    dirname, filename = os.path.split(ampl_filename)
    p = Popen('ampl', cwd=dirname, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    output = p.communicate('''
      model "{}";
      display _snvars;
      '''.format(ampl_filename))[0]
    snvars = '_snvars = '
    for line in output.split('\n'):
      if line.startswith(snvars):
        result['num_vars'] = int(line[len(snvars):])
  return results

def format_header(authors, legend, columns):
  print(authors)
  print()
  print('Legend')
  for c in columns:
    print(c + '  ' + legend[c])
  print()

columns = ['MN', 'NV', 'OS', 'FE', 'RT']

def format_results(log_filename):
  results = read_log(log_filename)
  df = pd.DataFrame({
    # Model Name
    'MN': [model_name(r['model']) for r in results],
    # Number of variables
    'NV': [r['num_vars'] for r in results],
    # Objective value returned by the solver
    'OS': [r['obj_value'] for r in results],
    # Number of function evaluations
    'FE': [num_func_evals(r) for r in results],
    # Solver runtime
    'RT': [r['time'] for r in results]
    }, columns=columns)
  df['OS'] = df['OS'].map('{}'.format)
  print(df)

legend = {
  'MN': 'Model Name',
  'NV': 'Number of variables',
  'OV': 'Known optimal value (or best known objective value)',
  'OS': 'Numerical optimal value returned by the solver',
  'FE': 'Number of model function and constraint evaluations',
  'RT': 'Solver runtime (complete execution time including input '
        'and license verification time)'
  }
format_header('János D. Pintér and Victor Zverovich', legend, columns)
format_results(sys.argv[1])
