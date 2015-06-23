# Benchmark utilities
# Copyright (c) 2015, Victor Zverovich

from __future__ import print_function
import ampl, glob, hashlib, itertools, math, os
import random, signal, tempfile, threading, time, yaml
from collections import OrderedDict
from contextlib import contextmanager
from datetime import datetime
from subprocess import check_call, Popen, PIPE, STDOUT

default_timeout = 1e9
repo_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def files(dirname, filenames):
  """
  Parses *filenames* which is a string containing one name per line, possibly
  ended with a # comment, and returns the list of names joined with *dirname*.
  Example:
    filenames = files('nlmodels', '''
      blend.mod
      branin.mod
      ''')
  """
  results = []
  for filename in filenames.splitlines():
    comment_pos = filename.find('#')
    if comment_pos != -1:
      filename = filename[:comment_pos]
    filename = filename.strip()
    if filename != '':
      results.append(os.path.join(dirname, filename))
  return results

def sha1_file(filename):
  "Computes a SHA-1 hash of file *filename*"
  blocksize = 65536
  hasher = hashlib.sha1()
  with open(filename, 'rb') as f:
    buf = f.read(blocksize)
    while len(buf) > 0:
      hasher.update(buf)
      buf = f.read(blocksize)
    return hasher.hexdigest()

def amplgsl_path():
  # Find amplgsl.
  for path in os.environ['PATH'].split(os.pathsep):
    amplgsl_path = os.path.join(path, 'amplgsl.dll')
    if os.path.exists(path):
      return amplgsl_path
  return ''

class AMPLError(Exception):
  def __init__(self, message):
    super(AMPLError, self).__init__(message)

class AMPL:
  def __init__(self, cwd=None):
    self.cwd = cwd

  def __enter__(self):
    self.process = Popen(['ampl', '-b'],
                         stdin=PIPE, stdout=PIPE, stderr=STDOUT, cwd=self.cwd)
    self.eval()
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.process.stdin.close();
    self.process.wait()

  def eval(self, ampl_code=None):
    if ampl_code:
      self.process.stdin.write('{} {}\n'.format(len(ampl_code) + 1, ampl_code))
    stdout = self.process.stdout
    results = []
    while True:
      header = stdout.readline()
      sep = header.index(' ')
      size = int(header[:sep])
      kind = header[sep + 1:].strip()
      output = stdout.read(size - len(header) + sep + 1)
      if kind.startswith('prompt'):
        return results
      results.append((kind, output))

  def eval_expr(self, ampl_expr):
    kind, output = self.eval('print {};'.format(ampl_expr))[0]
    if kind != 'print':
      raise AMPLError(output)
    # Remove trailing newline added by print.
    output = output[:-1]
    try:
      return float(output)
    except ValueError:
      return output

@contextmanager
def temp_nl_file(ampl_filename):
  """
  Translates *ampl_filename* with AMPL and generates a temporary NL file.
  Example:
    with temp_nl_file('test.ampl') as f:
      print(f.name)
  """
  dirname, filename = os.path.split(ampl_filename)
  with tempfile.NamedTemporaryFile(suffix='.nl') as f:
    check_call(['ampl', '-ob' + os.path.splitext(f.name)[0], filename], cwd=dirname)
    yield f

class NLHeader:
  def __init__(self):
    self.num_vars = 0
    self.num_cons = 0

def read_nl_header(nl_filename):
  "Read the NL header from the *nl_filename* file."
  header = NLHeader()
  with open(nl_filename, 'r') as f:
    f.readline()
    items = f.readline().split()
    header.num_vars = int(items[0])
    header.num_cons = int(items[1])
  return header

class Solution:
  def __init__(self):
    self.obj = float('nan')
    self.obj_error = None
    self.solve_result = None
    self.solve_message = None

def read_solution(ampl_filename, sol_filename):
  """
  Read the solution of the model *ampl_filename* from *sol_filename*
  and returns the objective value.
  """
  sol = Solution()
  dirname, filename = os.path.split(ampl_filename)
  with AMPL(dirname) as ampl:
    ampl.eval('model "{}";'.format(ampl_filename))
    ampl.eval('solution "{}";'.format(sol_filename))
    try:
      sol.obj = float(ampl.eval_expr('_obj[1]'))
    except AMPLError as e:
      sol.obj = 'nan'
      sol.obj_error = str(e)
    sol.solve_result = ampl.eval_expr('solve_result')
    sol.solve_message = ampl.eval_expr('solve_message')
  return sol

class SolveResult:
  def __init__(self, sol_filename, output, solution_time):
    # Solution (.sol) filename
    self.sol_filename = sol_filename
    # Solver output
    self.output = output
    # Solution time in seconds
    self.solution_time = solution_time

@contextmanager
def solve(ampl_filename, **kwargs):
  """
  Solves the AMPL problem given in *ampl_filename*.
  Example:
    with solve('test.ampl', solver='lgo', solver_options={'opmode': 3},
               env={'AMPLFUNC': 'path/to/amplgsl.dll'}, timeout=100,
               on_nl_file=update_options) as result:
      print(result.output)
  """
  with temp_nl_file(ampl_filename) as nl_file:
    on_nl_file = kwargs.get('on_nl_file')
    if on_nl_file:
      on_nl_file(nl_file, kwargs)
    sol_filename = os.path.splitext(nl_file.name)[0] + '.sol'
    # Prepare the solver command.
    command = [kwargs.get('solver', 'minos'), nl_file.name, '-AMPL']
    for name, value in kwargs.get('solver_options', {}).iteritems():
      command.append('{}={}'.format(name, value))
    # Create the timeout thread.
    timeout = kwargs.get('timeout', default_timeout)
    done = threading.Event()
    def kill_on_timeout():
      if not done.wait(timeout):
        process.send_signal(signal.SIGINT)
      # Wait for additional 10 seconds for the solver to stop and kill it
      # if it doesn't.
      if not done.wait(10):
        process.kill()
    thread = threading.Thread(target=kill_on_timeout)
    # Invoke the solver.
    start_time = time.time()
    try:
      process = Popen(command, stdout=PIPE, stderr=STDOUT, env=kwargs.get('env'))
      thread.start()
      try:
        output = process.communicate()[0]
        solution_time = time.time() - start_time
      finally:
        # Stop the timeout thread.
        done.set()
      thread.join()
      yield SolveResult(sol_filename, output, solution_time)
    finally:
      # Remove the solution file if it exists.
      try:
        os.remove(sol_filename)
      except OSError:
        pass

class Benchmark:
  "A solver benchmark"

  def __init__(self, **kwargs):
    # AMPL solver name
    self.solver = kwargs.get('solver')
    # A dict of solver options
    self.solver_options = kwargs.get('solver_options', {})
    # Solver timeout in seconds
    self.timeout = kwargs.get('timeout', default_timeout)
    # Log filename
    self.log_filename = kwargs.get('log', 'benchmark-log.yaml')
    # Callback called after .nl file is written
    self.on_nl_file = kwargs.get('on_nl_file')
    # Only pass PATH to the solver to avoid environment variables
    # interference with solver options.
    self.env = {}
    self.env['PATH'] = os.environ['PATH']
    self.env['AMPLFUNC'] = amplgsl_path()

  def __enter__(self):
    self.log = open(self.log_filename, 'w')
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.log.close()

  # model: AMPL model filename relative to the repository root
  def run(self, model):
    """
    Runs the benchmark by translating the AMPL *model* into NL format,
    passing it to solver, reading the solution and writing it to log.
    """
    ampl_filename = os.path.join(repo_dir, model)
    start = datetime.now()
    with solve(ampl_filename, solver=self.solver, solver_options=self.solver_options,
               env=self.env, timeout=self.timeout, on_nl_file=self.on_nl_file) as result:
      sol = read_solution(ampl_filename, result.sol_filename)
      self.write_log(model=model, sha=sha1_file(ampl_filename), start=start,
                     time=result.solution_time, output=result.output, solution=sol)

  def write_log_multiline(self, key, text):
    self.log.write('  {}: '.format(key))
    if text:
      self.log.write('|\n')
      for line in text.splitlines():
        self.log.write('    {}\n'.format(line))
    else:
      self.log.write('{}\n'.format(text))

  def write_log(self, **kwargs):
    self.log.write('- model: {}\n'.format(kwargs.get('model')))
    # Write SHA-1 hash of the AMPL file to be able to track which version
    # of the model was used.
    self.log.write('  sha: {}\n'.format(kwargs.get('sha')))
    self.log.write('  solver: {}\n'.format(self.solver))
    if len(self.solver_options) > 0:
      self.log.write('  solver_options:\n')
      for name, value in self.solver_options.iteritems():
        self.log.write('    {}: {}\n'.format(name, value))
    self.log.write('  start: {}\n'.format(kwargs.get('start')))
    time = kwargs.get('time')
    self.log.write('  time: {}\n'.format(time))
    self.log.write('  timeout: {}\n'.format(time >= self.timeout))
    sol = kwargs.get('solution')
    self.log.write('  obj: {}\n'.format(sol.obj))
    if sol.obj_error:
      self.write_log_multiline('obj_error', sol.obj_error)
    solve_result = sol.solve_result
    if solve_result == '?':
      solve_result = "'" + solve_result + "'"
    self.log.write('  solve_result: {}\n'.format(solve_result))
    self.write_log_multiline('solve_message', sol.solve_message)
    self.write_log_multiline('output', kwargs.get('output').replace('\b', ''))
    self.log.write('\n')
    self.log.flush()

def find_obj(nodes):
  for i in range(len(nodes)):
    node = nodes[i]
    if isinstance(node, ampl.Decl) and (node.kind == 'minimize' or node.kind == 'maximize'):
      return i

class RenamingVisitor:
  def __init__(self, names):
    self.names = names

  def visit_reference(self, expr):
    expr.name = self.names.get(expr.name, expr.name)

  def visit_subscript(self, expr):
    self.visit_reference(expr)

  def visit_paren(self, expr):
    expr.arg.accept(self)

  def visit_unary(self, expr):
    expr.arg.accept(self)

  def visit_binary(self, expr):
    expr.lhs.accept(self)
    expr.rhs.accept(self)

  def visit_if(self, expr):
    expr.condition.accept(self)
    expr.then_expr.accept(self)
    expr.else_expr.accept(self)

  def visit_call(self, expr):
    for arg in expr.args:
      arg.accept(self)

  def visit_sum(self, expr):
    expr.indexing.accept(self)
    expr.arg.accept(self)

  def visit_indexing(self, expr):
    expr.set_expr.accept(self)

def prepare_for_merge(model, suffix):
  suffix = str(suffix)
  path = model['path']
  with open(os.path.join(repo_dir, path), 'r') as f:
    nodes = ampl.parse(f.read(), path).nodes
    # Rename declarations.
    names = {}
    visitor = RenamingVisitor(names)
    for n in nodes:
      if isinstance(n, ampl.Decl):
        new_name = n.name + suffix
        names[n.name] = new_name
        n.name = new_name
        if n.indexing:
          n.indexing.accept(visitor)
        if n.body:
          n.body.accept(visitor)
      if isinstance(n, ampl.DataStmt):
        n.set_name = n.set_name + suffix
        n.param_names = [name + suffix for name in n.param_names]
    # Find the first objective and partition the nodes around it.
    obj_index = find_obj(nodes)
    # Add objective offset to make the optimal value nonnegative.
    obj = nodes[obj_index]
    sign = 1 if obj.kind == 'minimize' else -1
    best_obj = sign * model['best_obj']
    offset = math.ceil(abs(min(0.0, best_obj)))
    obj.body = ampl.ParenExpr(obj.body)
    if obj.kind == 'maximize':
      obj.body = ampl.UnaryExpr('-', obj.body)
    if offset > 0:
      obj.body = ampl.ParenExpr(ampl.BinaryExpr('+', obj.body, ampl.Reference(str(offset))))
    return nodes[:obj_index], obj, nodes[obj_index + 1:], best_obj + offset

def merge_models(models):
  """
  Merge given AMPL models into a single one using product composition
  of objective functions.
  For example, two models
    minimize o: f1(x);
  and
    minimize o: f2(x);
  are combined into a single model
    minimize o: f1(x1) * f2(x2);
  """
  merged_head = []
  merged_tail = []
  merged_best_obj = 1
  merged_obj = ampl.Decl('minimize', 'f')
  for i in range(len(models)):
    head, obj, tail, best_obj = prepare_for_merge(models[i], i + 1)
    merged_head += head
    merged_tail += tail
    merged_best_obj *= best_obj
    if merged_obj.body:
      merged_obj.body = ampl.BinaryExpr('*', merged_obj.body, obj.body)
    else:
      merged_obj.body = obj.body
  # Invert sign if objectives are of different kinds.
  return ampl.CompoundStmt(merged_head + [merged_obj] + merged_tail), merged_best_obj

def random_combination_with_replacement(iterable, r):
  "Random selection from itertools.combinations_with_replacement(iterable, r)"
  pool = tuple(iterable)
  n = len(pool)
  indices = sorted(random.randrange(n) for i in xrange(r))
  return tuple(pool[i] for i in indices)

def get_problem_combinator(index, n, num_problems=None):
  """
  Returns a function that combines *n* problems from *index* to get the given
  number of combined problems selected at random.
  """
  index = index.values()
  pool = range(len(index))
  if num_problems is None:
    # Get all combinations.
    combinations = [i for i in itertools.combinations_with_replacement(pool, n)]
  else:
    # Set seed to make sure that pseudo-random sequence is reproducible.
    random.seed(0)
    combinations = set()
    while len(combinations) < num_problems:
      combinations.add(random_combination_with_replacement(pool, n))
  def combine_problems(dirname):
    composite_index = OrderedDict()
    for indices in combinations:
      merged_model, best_obj = merge_models([index[i] for i in indices])
      name = '-'.join(['{:02}'.format(i + 1) for i in indices])
      filename = name + '.mod'
      path = os.path.join(dirname, filename)
      with open(path, 'w') as f:
        ampl.pretty_print(f, merged_model)
      composite_index[name] = {'best_obj': best_obj, 'path': path}
    return composite_index
  return combine_problems

def load_index(*dirs):
  """
  Load problem index.
  Example:
    index = load_index('casado', 'hansen')
  """
  index = OrderedDict()
  for dirname in dirs:
    with open(os.path.join(repo_dir, dirname, 'index.yaml')) as f:
      items = sorted(yaml.load(f).items())
      for k, v in items:
        v['path'] = os.path.join(dirname, k + '.mod')
      index.update(items)
  for k, v in index.iteritems():
    # Convert values such as 1e-8 to float since YAML treats them as strings.
    v['best_obj'] = float(v['best_obj'])
  return index

class Config:
  def __init__(self, solver, solver_options={}, **kwargs):
    self.solver = solver
    self.solver_options = solver_options
    self.suffix = kwargs.get('suffix')
    self.on_nl_file = kwargs.get('on_nl_file')
