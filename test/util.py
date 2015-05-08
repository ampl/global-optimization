# Test utilities

import hashlib, os, tempfile
from contextlib import contextmanager
from subprocess import check_call, Popen, PIPE

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
  for filename in filenames.split('\n'):
    comment_pos = filename.find('#')
    if comment_pos != -1:
      filename = filename[:comment_pos]
    filename = filename.strip()
    if filename != '':
      results.append(os.path.join(dirname, filename))
  return results

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
def solve_nl(nl_filename, solver):
  "Solves the NL problem given in *nl_filename* with the specified solver."
  sol_filename = os.path.splitext(nl_filename)[0] + '.sol'
  p = None
  try:
    p = Popen([solver, nl_filename, '-AMPL'], stdout=PIPE)
    p.communicate()
    yield sol_filename
  finally:
    if p:
      # Wait for the child process to terminate in case communicate() was
      # interrupted by SIGINT.
      p.wait()
    # Remove solution file if it exists.
    try:
      os.remove(sol_filename)
    except OSError:
      pass

def solve(ampl_filename, **kwargs):
  """
  Solves the AMPL problem given in *ampl_filename*.
  The *solver* arguments specifies the solver to use.
  The default solver is `minos`.
  Example:
    solve('test.ampl', solver='couenne')
  """
  solver = kwargs.get('solver', 'minos')
  with temp_nl_file(ampl_filename) as nl_file:
    with solve_nl(nl_file.name, solver) as sol_filename:
      pass # TODO: yield sol_filename
