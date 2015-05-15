# Benchmark utilities

import hashlib, os, signal, tempfile, threading, time
from contextlib import contextmanager
from subprocess import check_call, Popen, PIPE, STDOUT

default_timeout = 1e9

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

class Solution:
  def __init__(self):
    self.obj = float('nan')
    self.solve_result = None
    self.solve_message = None

def read_solution(ampl_filename, sol_filename):
  """
  Read the solution of the model *ampl_filename* from *sol_filename*
  and returns the objective value.
  """
  dirname, filename = os.path.split(ampl_filename)
  p = Popen('ampl', cwd=dirname, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
  output = p.communicate('''
    model "{}";
    solution "{}";
    display _obj[1];
    display solve_result;
    print solve_message;
    '''.format(ampl_filename, sol_filename))[0]
  obj = '_obj[1] = '
  solve_result = 'solve_result = '
  sol = Solution()
  for line in output.splitlines():
    if sol.solve_message is not None:
      if line:
        sol.solve_message += line + '\n'
    elif line.startswith(obj):
      sol.obj = float(line[len(obj):])
    elif line.startswith(solve_result):
      sol.solve_result = line[len(solve_result):]
      sol.solve_message = ''
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
    with solve('test.ampl', solver='lgo', solver_options={'opmode': 3}, timeout=100) as result:
      print(result.output)
  """
  with temp_nl_file(ampl_filename) as nl_file:
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
    thread = threading.Thread(target=kill_on_timeout)
    # Invoke the solver.
    start_time = time.time()
    try:
      process = Popen(command, stdout=PIPE, stderr=STDOUT)
      thread.start()
      output = process.communicate()[0]
      solution_time = time.time() - start_time
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

repo_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

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
    with solve(ampl_filename, solver=self.solver, solver_options=self.solver_options,
                    timeout=self.timeout) as result:
      sol = read_solution(ampl_filename, result.sol_filename)
      self.write_log(model=model, sha=sha1_file(ampl_filename),
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
    time = kwargs.get('time')
    self.log.write('  time: {}\n'.format(time))
    self.log.write('  timeout: {}\n'.format(time >= self.timeout))
    sol = kwargs.get('solution')
    self.log.write('  obj_value: {}\n'.format(sol.obj))
    self.log.write('  solve_result: {}\n'.format(sol.solve_result))
    self.write_log_multiline('solve_message', sol.solve_message)
    self.write_log_multiline('output', kwargs.get('output'))
    self.log.write('\n')
    self.log.flush()
