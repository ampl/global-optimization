# -*- coding: utf-8 -*-
# Copyright (c) 2015, Victor Zverovich

"""Benchmark script

Usage:
  benchmark run <path>
  benchmark format <path>
"""

from __future__ import print_function
import docopt, glob, os, re, shutil, sys, tempfile, util, yaml
import pandas as pd
from collections import OrderedDict
from contextlib import contextmanager

LOG_DIR = 'logs'

def read_module(path):
  "Read a Python module with the benchmark configuration."
  module_dir, module_name = os.path.split(path)
  module_name = os.path.splitext(module_name)[0]
  sys.path.insert(0, module_dir)
  return __import__(module_name)

def log_filename(module, config):
  filename = config.solver
  if config.suffix:
    filename += '-' + config.suffix
  return os.path.join(LOG_DIR, module.__name__, filename + '.yaml')

@contextmanager
def get_inputs(module):
  inputs = module.inputs
  workdir = tempfile.mkdtemp()
  try:
    # If inputs is callable, call it to get inputs.
    if hasattr(inputs, '__call__'):
      print('Getting inputs...')
      inputs = inputs(workdir)
    yield(inputs)
  finally:
    shutil.rmtree(workdir)

def run_benchmark(path):
  """
  Run a benchmark.
  path: path to a Python module with the benchmark configuration
  """
  module = read_module(path)
  with get_inputs(module) as inputs:
    print('Running benchmark...')
    for c in module.configs:
      log = log_filename(module, c)
      log_dir = os.path.dirname(log)
      if not os.path.exists(log_dir):
        os.makedirs(log_dir)
      with util.Benchmark(log=log, timeout=module.timeout, solver=c.solver,
                          solver_options=c.solver_options, on_nl_file=c.on_nl_file) as b:
        for name, data in inputs.iteritems():
          print(name)
          b.run(data['path'])

def model_name(result):
  "Extracts the model name from a benchmark result."
  return os.path.splitext(os.path.split(result['model'])[1])[0]

def printed_model_name(result, inputs):
  "Returns model name with '*' if it is a maximization problem."
  name = model_name(result)
  if inputs[name]['obj_kind'] == 'maximize':
    name += '*'
  return name

def max_con_violation(result):
  solver = result['solver']
  solve_message = result['solve_message']
  m = None
  if solver == 'lgo':
    m = re.search(r'Maximum constraint violation (.+)', solve_message)
  elif solver == 'knitro':
    m = re.search(r'feasibility error (.+)', solve_message)
  return m.group(1) if m else '-'

def num_func_evals(result):
  solver = result['solver']
  num_evals = '-'
  if solver == 'lgo':
    m = re.search(r'(\d+) function (and constraint )?evaluations',
                  result['solve_message'])
    if m:
      num_evals = int(m.group(1))
  elif solver == 'minos':
    m = re.search(r'Nonlin evals: (.*)\.', result['solve_message'])
    if m:
      num_evals = 0
      for entry in m.group(1).split(','):
        num_evals += int(entry.split('=')[1])
  elif solver == 'knitro':
    m = re.search(r'(\d+) function evaluations', result['solve_message'])
    if m:
      num_evals = int(m.group(1))
  return num_evals

def check_obj(result, inputs, obj_tolerance):
  obj = result['obj']
  best_obj = inputs[model_name(result)]['best_obj']
  rel_error = abs(obj - best_obj) / (1 + abs(best_obj))
  solve_result = result['solve_result']
  solved = False
  if rel_error <= obj_tolerance:
    if solve_result.startswith('solved'):
      solved = True
    elif solve_result == 'limit' or solve_result == 'failure':
      # LGO returns solve_result = 'failure' on SIGINT so check if
      # max constraint violation is within tolerance.
      max_viol = max_con_violation(result)
      if max_viol == '-' or float(max_viol) <= 1e-8:
        solved = True
  return (solved, rel_error)

def obj_status(result, inputs, obj_tolerance):
  solved, rel_error = check_obj(result, inputs, obj_tolerance)
  status = ' ' if solved else '?'
  input = inputs[model_name(result)]
  sign = 1 if input['obj_kind'] == 'minimize' else -1
  obj = sign * result['obj']
  best_obj = sign * input['best_obj']
  if obj < best_obj and rel_error > 1e-6:
    status += '!'
  return status

# Read the log and get the number of variables and constraints
# for each problem.
def read_log(filename, inputs, excludes=[]):
  results = [r for r in yaml.load(open(filename, 'r')) if model_name(r) not in excludes]
  for result in results:
    if not result['solve_message']:
      result['solve_message'] = ''
    # Convert values such as 1e-8 to float since YAML doesn't do it.
    result['obj'] = float(result['obj'])
  return results

def write_header(stream, authors, legend):
  stream.write(authors)
  stream.write('\n\n')
  stream.write('Legend\n')
  for c in legend:
    if legend[c]:
      stream.write('{}  {}\n'.format(c , legend[c]))
  stream.write('\n')

def write_results(stream, results, inputs, columns, obj_tolerance):
  df = pd.DataFrame({
    # Model Name
    'MN': [printed_model_name(r, inputs) for r in results],
    # Number of variables
    'NV': [inputs[model_name(r)]['num_vars'] for r in results],
    # Number of constraints
    'NC': [inputs[model_name(r)]['num_cons'] for r in results],
    # Best known objective value
    'OV': [inputs[model_name(r)]['best_obj'] for r in results],
    # Objective value returned by the solver
    'OS': [r['obj'] for r in results],
    # Maximal constraint violation
    'CV': [max_con_violation(r) for r in results],
    # Number of function evaluations
    'FE': [num_func_evals(r) for r in results],
    # Solver runtime
    'RT': [r['time'] for r in results],
    ' ':  [obj_status(r, inputs, obj_tolerance) for r in results]
    }, index=range(1, len(results) + 1), columns=columns)
  for col in ['OV', 'OS']:
    df[col] = df[col].map('{:g}'.format)
  stream.write(df.to_string())
  stream.write('\n')

def write_summary(stream, results, inputs, obj_tolerance):
  stream.write('\nSummary of results\n')
  stream.write('Number of test problems: {}\n'.format(len(results)))
  solver = results[0]['solver']
  if solver == 'lgo':
    opmode = results[0]['solver_options']['opmode']
  total_time = 0
  normalized_func_evals = 0
  num_solved = 0
  num_unsolved = 0
  solved_rel_error = 0
  unsolved_rel_error = 0
  for r in results:
    total_time += r['time']
    if solver == 'lgo' and r['solver_options']['opmode'] != opmode:
      raise Exception('Inconsistent opmode')
    model = model_name(r)
    nvars = inputs[model]['num_vars']
    ncons = inputs[model]['num_cons']
    modc = (nvars + ncons) * (nvars + ncons + 1) / 2 + (nvars + ncons) + 1
    nfe = num_func_evals(r)
    if nfe != '-':
      normalized_func_evals += nfe / modc
    solved, rel_error = check_obj(r, inputs, obj_tolerance)
    if solved:
      solved_rel_error += rel_error
      num_solved += 1
    else:
      unsolved_rel_error += rel_error
      num_unsolved += 1
  if solver == 'lgo':
    stream.write('LGO operational mode: {}\n'.format(opmode))
    stream.write('Relative error tolerance for successful solution: {}\n'.format(obj_tolerance))
  stream.write('Number of successful solutions: {} of {}\n'.format(num_solved, len(results)))
  avg_solved_rel_error = '{:.2}'.format(solved_rel_error / num_solved) if num_solved != 0 else '-'
  stream.write('Average relative error of solutions found: {}\n'.format(avg_solved_rel_error))
  avg_unsolved_rel_error = '{:.2}'.format(unsolved_rel_error / num_unsolved) if num_unsolved != 0 else '-'
  stream.write('Average relative error of unsolved problems: {}\n'.format(avg_unsolved_rel_error))
  if solver == 'lgo':
    stream.write('Average normalized number of function evaluations (FE/modc): {}\n'.
                 format(normalized_func_evals / len(results)))
    stream.write('where modc is the estimated model complexity\n')
    stream.write('modc = (nvars + ncons) * (nvars + ncons + 1) / 2 + (nvars + ncons) + 1\n')
  stream.write('Total solver runtime (seconds): {:.2f}\n'.format(total_time))

legend = OrderedDict([
  ('MN', 'Model Name'),
  ('NV', 'Number of variables'),
  ('NC', 'Number of constraints'),
  ('OV', 'Known optimal value (or best known objective value)'),
  ('OS', 'Numerical optimal value returned by the solver'),
  ('OV', 'Known optimal value (or best known objective value)'),
  ('CV', 'Maximal constraint violation'),
  ('FE', 'Number of model function and constraint evaluations'),
  ('RT', 'Solver runtime (complete execution time including input '
         'and license verification time)'),
  (' ' , None)
  ])

def format_logs(path):
  module = read_module(path)
  with get_inputs(module) as inputs:
    print('Getting problem information...')
    for input in inputs.values():
      ampl_filename = input['path']
      print(os.path.basename(ampl_filename))
      dirname, filename = os.path.split(ampl_filename)
      if not os.path.isabs(dirname):
        dirname = os.path.join(util.repo_dir, dirname)
      with util.AMPL(dirname) as ampl:
        ampl.eval('model {};'.format(filename))
        input['num_vars'] = ampl.eval_expr('_snvars')
        input['num_cons'] = ampl.eval_expr('_sncons')
        objname = ampl.eval_expr('_objname[1]')
        input['obj_kind'] = ampl.eval('show {};'.format(objname))[0][1].split()[0]
    for c in module.configs:
      log = log_filename(module, c)
      print('Parsing ' + log)
      results = read_log(log, inputs)
      if 'result_filter' in dir(module):
        results = filter(module.result_filter, results)
      print('Formatting results...')
      output_filename = os.path.splitext(log)[0] + '.txt'
      obj_tolerance = 0.0001
      with open(output_filename, 'w') as f:
        write_header(f, 'János D. Pintér and Victor Zverovich', legend)
        write_results(f, results, inputs, legend.keys(), obj_tolerance)
        write_summary(f, results, inputs, obj_tolerance)

def run():
  args = docopt.docopt(__doc__)
  if args['run']:
    run_benchmark(args['<path>'])
  elif args['format']:
    format_logs(args['<path>'])
