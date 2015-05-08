# The util module tests

from util import files

def test_files():
  f = files('foo', '''
    bar # comment
    baz
    ''')
  assert(f == ['foo/bar', 'foo/baz'])
