# The util module tests

import os, tempfile, time, util
from subprocess import check_call, PIPE

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

def test_temp_nl_file():
  with tempfile.NamedTemporaryFile() as ampl_file:
    ampl_file.write('var x >= 42; minimize o: x;')
    ampl_file.flush()
    nl_filename = None
    with util.temp_nl_file(ampl_file.name) as nl_file:
      nl_filename = nl_file.name
      assert(nl_filename.endswith('.nl'))
      assert(os.path.exists(nl_filename))
    assert(not os.path.exists(nl_filename))

def test_read_solution():
  with tempfile.NamedTemporaryFile() as ampl_file:
    ampl_file.write('var x >= 42; minimize o: x;')
    ampl_file.flush()
    nl_filename = None
    with util.temp_nl_file(ampl_file.name) as nl_file:
      check_call([solver, nl_file.name, '-AMPL'], stdout=PIPE, stderr=PIPE)
      sol_filename = os.path.splitext(nl_file.name)[0] + '.sol'
      assert util.read_solution(ampl_file.name, sol_filename) == 42

def test_mock_solver():
  try:
    sol_filename = None
    with tempfile.NamedTemporaryFile(suffix='.nl') as nl_file:
      sol_filename = os.path.splitext(nl_file.name)[0] + '.sol'
      check_call(['./mock-solver', nl_file.name])
    assert(os.path.exists(sol_filename))
  finally:
    os.remove(sol_filename)

def test_solve():
  with tempfile.NamedTemporaryFile() as ampl_file:
    ampl_file.write('var x >= 42; minimize o: x;')
    ampl_file.flush()
    nl_filename = None
    sol_filename = None
    with util.solve(ampl_file.name, solver='./mock-solver') as (time, sf):
      nl_filename = os.path.splitext(sf)[0] + '.nl'
      sol_filename = sf
      assert(os.path.exists(nl_filename))
      assert(os.path.exists(sol_filename))
    assert(not os.path.exists(nl_filename))
    assert(not os.path.exists(sol_filename))
    # Check if files are deleted even in case of KeyboardInterrupt.
    caught = False
    try:
      with util.solve(ampl_file.name, solver='./mock-solver') as (time, sf):
        nl_filename = os.path.splitext(sf)[0] + '.nl'
        sol_filename = sf
        assert(os.path.exists(nl_filename))
        assert(os.path.exists(sol_filename))
        raise KeyboardInterrupt()
    except KeyboardInterrupt:
      caught = True
    assert(caught)
    assert(not os.path.exists(nl_filename))
    assert(not os.path.exists(sol_filename))

repo_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def test_solve_timeout():
  start_time = time.time()
  with util.solve(os.path.join(repo_dir, 'nlmodels', 'camel1u.mod'),
                  solver=solver, timeout=1) as sf:
    elapsed_time = time.time() - start_time
    assert elapsed_time >= 1 and elapsed_time < 2
