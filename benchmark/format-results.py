#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os, re, sys, yaml
import pandas as pd
from subprocess import Popen, PIPE, STDOUT

repo_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def model_name(result):
  "Extracts the model name from a benchmark result."
  return os.path.splitext(os.path.split(result['model'])[1])[0]

def max_con_violations(result):
  m = re.search(r'Maximum constraint violation (.+)', result['solve_message'])
  return m.group(1) if m else '-'

def num_func_evals(result):
  m = re.search(r'(\d+) function (and constraint )?evaluations',
                result['solve_message'])
  return int(m.group(1)) if m else None

def load_index(*args):
  index = {}
  for dirname in args:
    index.update(yaml.load(open(os.path.join(repo_dir, dirname, 'index.yaml'))))
  return index

index = load_index('nlmodels', 'jdp')

# Read the log and get the number of variables and constraints
# for each problem.
def read_log(filename):
  results = yaml.load(file(filename, 'r'))
  for result in results:
    ampl_filename = os.path.join(repo_dir, result['model'])
    dirname, filename = os.path.split(ampl_filename)
    p = Popen('ampl', cwd=dirname, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    output = p.communicate('''
      model "{}";
      display _snvars;
      display _sncons;
      '''.format(ampl_filename))[0]
    snvars = '_snvars = '
    sncons = '_sncons = '
    for line in output.split('\n'):
      if line.startswith(snvars):
        result['num_vars'] = int(line[len(snvars):])
      elif line.startswith(sncons):
        result['num_cons'] = int(line[len(sncons):])
  return results

def format_header(authors, legend, columns):
  print(authors)
  print()
  print('Legend')
  for c in columns:
    print(c + '  ' + legend[c])
  print()

columns = ['MN', 'NV', 'NC', 'OV', 'OS', 'CV', 'FE', 'RT']

def format_results(log_filename):
  results = read_log(log_filename)
  df = pd.DataFrame({
    # Model Name
    'MN': [model_name(r) for r in results],
    # Number of variables
    'NV': [r['num_vars'] for r in results],
    # Number of constraints
    'NC': [r['num_cons'] for r in results],
    # Best known objective value
    'OV': [index[model_name(r)]['best_obj'] for r in results],
    # Objective value returned by the solver
    'OS': [r['obj_value'] for r in results],
    # Maximal constraint violation
    'CV': [max_con_violations(r) for r in results],
    # Number of function evaluations
    'FE': [num_func_evals(r) for r in results],
    # Solver runtime
    'RT': [r['time'] for r in results]
    }, columns=columns)
  for col in ['OV', 'OS']:
    df[col] = df[col].map('{:g}'.format)
  print(df)

legend = {
  'MN': 'Model Name',
  'NV': 'Number of variables',
  'NC': 'Number of constraints',
  'OV': 'Known optimal value (or best known objective value)',
  'OS': 'Numerical optimal value returned by the solver',
  'OV': 'Known optimal value (or best known objective value)',
  'CV': 'Maximal constraint violation',
  'FE': 'Number of model function and constraint evaluations',
  'RT': 'Solver runtime (complete execution time including input '
        'and license verification time)'
  }
format_header('János D. Pintér and Victor Zverovich', legend, columns)
format_results(sys.argv[1])
