# Benchmark utilities

import hashlib, os, signal, tempfile, threading, time
from contextlib import contextmanager
from subprocess import check_call, Popen, PIPE, STDOUT

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
    '''.format(ampl_filename, sol_filename))[0]
  obj = '_obj[1] = '
  for line in output.split('\n'):
    if line.startswith(obj):
      return float(line[len(obj):])
  return None

@contextmanager
def solve(ampl_filename, **kwargs):
  """
  Solves the AMPL problem given in *ampl_filename*.
  Example:
    solve('test.ampl', solver='minos', timeout=100)
  """
  with temp_nl_file(ampl_filename) as nl_file:
    sol_filename = os.path.splitext(nl_file.name)[0] + '.sol'
    timeout = kwargs.get('timeout', 1e9)
    done = threading.Event()
    def kill_on_timeout():
      if not done.wait(timeout):
        process.send_signal(signal.SIGINT)
    thread = threading.Thread(target=kill_on_timeout)
    start_time = time.time()
    try:
      process = Popen([kwargs.get('solver', 'minos'), nl_file.name, '-AMPL'],
                      stdout=PIPE, stderr=STDOUT)
      thread.start()
      process.communicate()
      elapsed_time = time.time() - start_time
      # Stop the timeout thread.
      done.set()
      thread.join()
      yield elapsed_time, sol_filename
    finally:
      # Remove the solution file if it exists.
      try:
        os.remove(sol_filename)
      except OSError:
        pass
