# The util module tests

import os, tempfile, time, util, yaml
from contextlib import contextmanager
from subprocess import check_call, check_output, PIPE

solver = 'couenne'

def test_files():
  f = util.files('foo', '''
    bar # comment
    baz
    ''')
  assert(f == ['foo/bar', 'foo/baz'])

def test_sha1_file():
  with tempfile.NamedTemporaryFile() as f:
    f.write('some useful content')
    f.flush()
    assert(util.sha1_file(f.name) == '4f7a376f6110cb8aad4f02e319b52f7325d63a83')

@contextmanager
def temp_ampl_file(content='var x >= 42; minimize o: x;'):
  with tempfile.NamedTemporaryFile() as ampl_file:
    ampl_file.write(content)
    ampl_file.flush()
    yield ampl_file

def test_temp_nl_file():
  with temp_ampl_file() as ampl_file:
    nl_filename = None
    with util.temp_nl_file(ampl_file.name) as nl_file:
      nl_filename = nl_file.name
      assert(nl_filename.endswith('.nl'))
      assert(os.path.exists(nl_filename))
    assert(not os.path.exists(nl_filename))

def test_read_solution():
  with temp_ampl_file() as ampl_file:
    nl_filename = None
    with util.temp_nl_file(ampl_file.name) as nl_file:
      check_call([solver, nl_file.name, '-AMPL'], stdout=PIPE, stderr=PIPE)
      sol_filename = os.path.splitext(nl_file.name)[0] + '.sol'
      sol = util.read_solution(ampl_file.name, sol_filename)
      assert sol.obj == 42
      assert sol.solve_result == 'solved'
      assert 'couenne' in sol.solve_message

def test_mock_solver():
  try:
    sol_filename = None
    with tempfile.NamedTemporaryFile(suffix='.nl') as nl_file:
      sol_filename = os.path.splitext(nl_file.name)[0] + '.sol'
      command = ['./mock-solver', nl_file.name]
      assert check_output(command).rstrip() == str(command)
    assert(os.path.exists(sol_filename))
  finally:
    os.remove(sol_filename)

def test_solve():
  with temp_ampl_file() as ampl_file:
    nl_filename = None
    sol_filename = None
    with util.solve(ampl_file.name, solver='./mock-solver') as result:
      sol_filename = result.sol_filename
      nl_filename = os.path.splitext(sol_filename)[0] + '.nl'
      assert(os.path.exists(nl_filename))
      assert(os.path.exists(sol_filename))
    assert(not os.path.exists(nl_filename))
    assert(not os.path.exists(sol_filename))

def test_solve_interrupt():
  with temp_ampl_file() as ampl_file:
    # Check if files are deleted even in case of KeyboardInterrupt.
    caught = False
    try:
      with util.solve(ampl_file.name, solver='./mock-solver') as result:
        sol_filename = result.sol_filename
        nl_filename = os.path.splitext(sol_filename)[0] + '.nl'
        assert(os.path.exists(nl_filename))
        assert(os.path.exists(sol_filename))
        raise KeyboardInterrupt()
    except KeyboardInterrupt:
      caught = True
    assert(caught)
    assert(not os.path.exists(nl_filename))
    assert(not os.path.exists(sol_filename))

def test_solve_on_nl_file():
  nl_filename = []
  solver_options = {'foo': 0}
  def on_nl_file(nl_file):
    nl_filename.append(nl_file.name)
    assert os.path.exists(nl_file.name)
    solver_options['foo'] = 42
  with temp_ampl_file() as ampl_file:
    with util.solve(ampl_file.name, solver='./mock-solver',
                    solver_options=solver_options, on_nl_file=on_nl_file) as result:
      sol_filename = result.sol_filename
      assert nl_filename[0] == os.path.splitext(sol_filename)[0] + '.nl'
      assert 'foo=42' in result.output

repo_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def test_solve_timeout():
  start_time = time.time()
  with util.solve(os.path.join(repo_dir, 'nlmodels', 'camel1u.mod'),
                  solver=solver, timeout=1) as result:
    elapsed_time = time.time() - start_time
    assert elapsed_time >= 1 and elapsed_time < 2

def test_solver_options():
  with temp_ampl_file() as ampl_file:
    with util.solve(ampl_file.name, solver='./mock-solver',
                    solver_options={'foo': 42, 'bar': 'baz'}) as result:
      assert result.output.endswith("'-AMPL', 'foo=42', 'bar=baz']\n")

def test_benchmark():
  b = util.Benchmark()
  assert b.solver == None
  assert b.timeout == 1e9
  assert b.log_filename == 'benchmark-log.yaml'
  def on_nl_file(nl_file):
    b.solver_options['answer'] = 42
  b = util.Benchmark(solver='testsolver', timeout=11, log='test.log', on_nl_file=on_nl_file)
  assert b.solver == 'testsolver'
  assert b.timeout == 11
  assert b.log_filename == 'test.log'
  assert not os.path.exists('test.log')
  assert b.on_nl_file == on_nl_file
  with temp_ampl_file() as ampl_file:
    with tempfile.NamedTemporaryFile() as log_file:
      with util.Benchmark(solver='./mock-solver', solver_options={'answer': 42},
                          log=log_file.name) as b:
        assert log_file.read() == ''
        b.run(ampl_file.name)
      log = yaml.load(log_file.read())
      assert len(log) == 1
      entry = log[0]
      assert entry['model'] == ampl_file.name
      assert entry['sha'] == util.sha1_file(ampl_file.name)
      assert entry['solver'] == './mock-solver'
      assert entry['solver_options'] == {'answer': 42}
      assert entry['start']
      assert float(entry['time']) > 0
      assert not entry['timeout']
      assert float(entry['obj'])
      assert entry['solve_result']
      assert entry['solve_message']
      assert entry['output'].endswith("'-AMPL', 'answer=42']\n")
