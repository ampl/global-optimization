# The util module tests

import os, tempfile, util

def test_files():
  f = util.files('foo', '''
    bar # comment
    baz
    ''')
  assert(f == ['foo/bar', 'foo/baz'])

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
