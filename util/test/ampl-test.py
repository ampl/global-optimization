# AMPL parser and AST tests

import ampl, copy
from cStringIO import StringIO
from mock import MagicMock

class MockVisitor: pass

def ref(name):
  "Create a reference."
  return ampl.Reference(name)

def test_ref():
  expr = ref('foo')
  assert type(expr) == ampl.Reference
  assert expr.name == 'foo'

def check_accept(node, method_name):
  "Check if node.accept(visitor) calls visitor.method_name(node)."
  visitor = MockVisitor()
  mock = MagicMock()
  setattr(visitor, method_name, mock)
  mock.return_value = 42
  assert node.accept(visitor) == 42
  mock.assert_called_with(node)

def test_reference():
  expr = ampl.Reference('foo')
  assert type(expr) == ampl.Reference
  assert expr.name == 'foo'
  check_accept(expr, 'visit_reference')

def test_subscript():
  sub = ref('foo')
  expr = ampl.SubscriptExpr('bar', sub)
  assert type(expr) == ampl.SubscriptExpr
  assert expr.name == 'bar'
  assert expr.subscript == sub
  check_accept(expr, 'visit_subscript')

def test_paren():
  arg = ref('a')
  expr = ampl.ParenExpr(arg)
  assert type(expr) == ampl.ParenExpr
  assert expr.arg == arg
  check_accept(expr, 'visit_paren')

def test_unary():
  arg = ref('a')
  expr = ampl.UnaryExpr('-', arg)
  assert type(expr) == ampl.UnaryExpr
  assert expr.op == '-'
  assert expr.arg == arg
  check_accept(expr, 'visit_unary')

def test_binary():
  lhs = ref('a')
  rhs = ref('b')
  expr = ampl.BinaryExpr('+', lhs, rhs)
  assert type(expr) == ampl.BinaryExpr
  assert expr.op == '+'
  assert expr.lhs == lhs
  assert expr.rhs == rhs
  check_accept(expr, 'visit_binary')

def test_if():
  condition = ref('a')
  then_expr = ref('b')
  else_expr = ref('c')
  expr = ampl.IfExpr(condition, then_expr, else_expr)
  assert type(expr) == ampl.IfExpr
  assert expr.condition == condition
  assert expr.then_expr == then_expr
  assert expr.else_expr == else_expr
  expr = ampl.IfExpr(condition, then_expr)
  assert expr.else_expr == None
  check_accept(expr, 'visit_if')

def test_call():
  arg0 = ref('a')
  arg1 = ref('b')
  expr = ampl.CallExpr('foo', [arg0, arg1])
  assert type(expr) == ampl.CallExpr
  assert expr.func_name == 'foo'
  assert expr.args == [arg0, arg1]
  check_accept(expr, 'visit_call')

def test_sum():
  indexing = ampl.Indexing(ref('a'))
  arg = ref('b')
  expr = ampl.SumExpr(indexing, arg)
  assert type(expr) == ampl.SumExpr
  assert expr.indexing == indexing
  assert expr.arg == arg
  check_accept(expr, 'visit_sum')

def test_indexing():
  index = 'a'
  set_expr = ref('b')
  expr = ampl.Indexing(set_expr, index)
  assert type(expr) == ampl.Indexing
  assert expr.index == index
  assert expr.set_expr == set_expr
  expr = ampl.Indexing(set_expr)
  assert expr.index == None
  assert expr.set_expr == set_expr
  check_accept(expr, 'visit_indexing')

def test_init():
  init = ref('a')
  attr = ampl.InitAttr(init)
  assert type(attr) == ampl.InitAttr
  assert attr.init == init
  check_accept(attr, 'visit_init')

def test_in():
  lb = ref('a')
  ub = ref('b')
  attr = ampl.InAttr(lb, ub)
  assert type(attr) == ampl.InAttr
  assert attr.lb == lb
  assert attr.ub == ub
  check_accept(attr, 'visit_in')

def test_decl():
  indexing = ampl.Indexing(ref('a'))
  attrs = [ampl.InitAttr(ref('a'))]
  decl = ampl.Decl('var', 'x', indexing, attrs)
  assert type(decl) == ampl.Decl
  assert decl.kind == 'var'
  assert decl.name == 'x'
  assert decl.indexing == indexing
  assert decl.attrs == attrs
  assert decl.body == None
  decl = ampl.Decl('var', 'x', indexing)
  assert decl.attrs == []
  decl = ampl.Decl('var', 'x')
  assert decl.indexing == None
  check_accept(decl, 'visit_decl')

def test_include():
  stmt = ampl.IncludeStmt('model')
  assert type(stmt) == ampl.IncludeStmt
  assert stmt.kind == 'model'
  check_accept(stmt, 'visit_include')

def test_data():
  param_names = ['a', 'b']
  values = [0, 1, 2, 3, 4, 5]
  stmt = ampl.DataStmt('param', 'S', param_names, values)
  assert type(stmt) == ampl.DataStmt
  assert stmt.kind == 'param'
  assert stmt.set_name == 'S'
  assert stmt.param_names == param_names
  assert stmt.values == values
  check_accept(stmt, 'visit_data')

def test_compound():
  nodes = [ampl.IncludeStmt('model'), ampl.Decl('var', 'x')]
  stmt = ampl.CompoundStmt(nodes)
  assert type(stmt) == ampl.CompoundStmt
  assert stmt.nodes == nodes
  check_accept(stmt, 'visit_compound')

def check_print(output, node):
  "Check if the output of pretty_print for the given AST node."
  stream = StringIO()
  ampl.pretty_print(stream, node)
  real_output = stream.getvalue()
  assert real_output == output

def test_pretty_print():
  check_print('a', ref('a'))
  check_print('a[b]', ampl.SubscriptExpr('a', ref('b')))
  check_print('(a)', ampl.ParenExpr(ref('a')))
  check_print('-a', ampl.UnaryExpr('-', ref('a')))
  check_print('a + b', ampl.BinaryExpr('+', ref('a'), ref('b')))
  check_print('if a then b else c',
              ampl.IfExpr(ref('a'), ref('b'), ref('c')))
  check_print('if a then b',
              ampl.IfExpr(ref('a'), ref('b'), None))
  check_print('f(a, b)', ampl.CallExpr('f', [ref('a'), ref('b')]))
  check_print('sum{s in S} x[s]', ampl.SumExpr(ampl.Indexing(ref('S'), 's'),
                                               ampl.SubscriptExpr('x', ref('s'))))
  check_print('{s in S}', ampl.Indexing(ref('S'), 's'))
  check_print('{S}', ampl.Indexing(ref('S')))
  check_print('= a', ampl.InitAttr(ref('a')))
  check_print('in [a, b]', ampl.InAttr(ref('a'), ref('b')))
  check_print('var x{S} = a;\n', ampl.Decl('var', 'x', ampl.Indexing(ref('S')),
                                           [ampl.InitAttr(ref('a'))]))
  decl = ampl.Decl('minimize', 'o')
  decl.body = ampl.UnaryExpr('-', ref('x'))
  check_print('minimize o: -x;\n', decl)
  check_print('model;\n', ampl.IncludeStmt('model'))
  param_names = ['a', 'b']
  values = [str(n) for n in range(6)]
  check_print(
    'param:\n' +
    'S:a b :=\n' +
    '0 1 2\n' +
    '3 4 5\n' +
    ';\n', ampl.DataStmt('param', 'S', param_names, values))
  check_print('model;\nvar x;\n',
              ampl.CompoundStmt([ampl.IncludeStmt('model'), ampl.Decl('var', 'x')]))

def equal_nodes(lhs, rhs):
  "Compare AST nodes for equality."
  if type(lhs) != type(rhs):
    return False

  class Comparator:
    def visit_reference(self, expr):
      return lhs.name == rhs.name

    def visit_subscript(self, expr):
      return lhs.name == rhs.name and equal_nodes(lhs.subscript, rhs.subscript)

    def visit_paren(self, expr):
      return equal_nodes(lhs.arg, rhs.arg)

    def visit_unary(self, expr):
      return lhs.op == rhs.op and equal_nodes(lhs.arg, rhs.arg)

    def visit_binary(self, expr):
      return lhs.op == rhs.op and \
        equal_nodes(lhs.lhs, rhs.lhs) and equal_nodes(lhs.rhs, rhs.rhs)

    def visit_if(self, expr):
      return equal_nodes(lhs.condition, rhs.condition) and \
        equal_nodes(lhs.then_expr, rhs.then_expr) and \
          equal_nodes(lhs.else_expr, rhs.else_expr)

    def visit_call(self, expr):
      return lhs.func_name == rhs.func_name and \
          equal_node_lists(lhs.args, rhs.args)

    def visit_sum(self, expr):
      return equal_nodes(lhs.indexing, rhs.indexing) and \
          equal_nodes(lhs.arg, rhs.arg)

    def visit_indexing(self, expr):
      return lhs.index == rhs.index and equal_nodes(lhs.set_expr, rhs.set_expr)

    def visit_init(self, attr):
      return equal_nodes(lhs.init, rhs.init)

    def visit_in(self, attr):
      return equal_nodes(lhs.lb, rhs.lb) and equal_nodes(lhs.ub, rhs.ub)

    def visit_decl(self, decl):
      return lhs.kind == rhs.kind and lhs.name == rhs.name and \
        equal_nodes(lhs.indexing, rhs.indexing) and equal_nodes(lhs.body, rhs.body) and \
        equal_node_lists(lhs.attrs, rhs.attrs)

    def visit_include(self, stmt):
      return lhs.kind == rhs.kind

    def visit_data(self, stmt):
      return lhs.kind == rhs.kind and lhs.set_name == rhs.set_name and \
        lhs.param_names == rhs.param_names and lhs.values == rhs.values

    def visit_compound(self, stmt):
      return equal_node_lists(lhs.nodes, rhs.nodes)

  return True if lhs is None else lhs.accept(Comparator())

def equal_node_lists(lhs, rhs):
  "Compare lists of AST nodes for equality."
  if len(lhs) != len(rhs):
    return False
  for i, j in zip(lhs, rhs):
    if not equal_nodes(i, j):
      return False
  return True

def check_equal_nodes(node, *inequal_nodes):
  "Check if equal_nodes compares nodes recursively."
  assert equal_nodes(node, node)
  assert equal_nodes(node, copy.deepcopy(node))
  assert not equal_nodes(node, None)
  assert not equal_nodes(node, ref('x') if type(node) != ampl.Reference else ampl.CompoundStmt([]))
  for i in inequal_nodes:
    assert not equal_nodes(node, i)

def test_equal_nodes():
  assert equal_nodes(None, None)
  x = ref('x')
  y = ref('y')
  z = ref('z')
  ix = ampl.Indexing(x)
  iy = ampl.Indexing(y)
  check_equal_nodes(x, y)
  check_equal_nodes(ampl.ParenExpr(x), ampl.UnaryExpr('-', x))
  check_equal_nodes(ampl.UnaryExpr('-', x), ampl.UnaryExpr('+', x), ampl.UnaryExpr('-', y))
  check_equal_nodes(ampl.BinaryExpr('*', x, y), ampl.BinaryExpr('+', x, y),
                    ampl.BinaryExpr('*', y, y), ampl.BinaryExpr('*', x, x))
  check_equal_nodes(ampl.IfExpr(x, y, z), ampl.IfExpr(z, y, z),
                    ampl.IfExpr(x, x, z), ampl.IfExpr(x, y, y))
  check_equal_nodes(ampl.CallExpr('sin', [x]), ampl.CallExpr('cos', [x]),
                    ampl.CallExpr('sin', [y]), ampl.CallExpr('sin', [x, y]))
  check_equal_nodes(ampl.SumExpr(ix, x), ampl.SumExpr(iy, x), ampl.SumExpr(ix, y))
  check_equal_nodes(ix, iy)
  check_equal_nodes(ampl.Decl('var', 'x'), ampl.Decl('var', 'y'))
  check_equal_nodes(ampl.IncludeStmt('data'), ampl.IncludeStmt('model'))
  check_equal_nodes(ampl.DataStmt('param', 'S', ['a', 'b'], ['1', '2', '3']),
                    ampl.DataStmt('var', 'S', ['a', 'b'], ['1', '2', '3']),
                    ampl.DataStmt('param', 'T', ['a', 'b'], ['1', '2', '3']),
                    ampl.DataStmt('param', 'S', ['a'], ['1', '2', '3']),
                    ampl.DataStmt('param', 'S', ['a', 'c'], ['1', '2', '3']),
                    ampl.DataStmt('param', 'S', ['a', 'v'], ['1', '2']),
                    ampl.DataStmt('param', 'S', ['a', 'v'], ['1', '2', '4']))
  assert not equal_nodes(ampl.Decl('var', 'x'), ampl.CompoundStmt([]))

def test_equal_node_lists():
  assert equal_node_lists([], [])
  assert not equal_node_lists([], [ampl.Decl('var', 'x')])
  assert equal_node_lists([ampl.Decl('var', 'x')], [ampl.Decl('var', 'x')])
  assert not equal_node_lists([ampl.Decl('var', 'x')], [ampl.Decl('var', 'y')])
  assert not equal_node_lists([ampl.Decl('var', 'x')],
                              [ampl.Decl('var', 'x'), ampl.Decl('var', 'y')])

def check_parse(input, *nodes):
  assert equal_nodes(ampl.parse(input, 'in'), ampl.CompoundStmt(nodes))

def test_parse_decls():
  s_decl = ampl.Decl('set', 'S')
  indexing = ampl.Indexing(ref('S'))
  for kw in ['param', 'var', 'set', 'minimize', 'maximize']:
    check_parse(kw + ' a;', ampl.Decl(kw, 'a'))
    check_parse('set S; ' + kw + ' a{S};', s_decl, ampl.Decl(kw, 'a', indexing))

def test_parse_attrs():
  e1 = ampl.BinaryExpr('+', ref('x'), ref('y'))
  e2 = ampl.UnaryExpr('-', ref('x'))
  for kw in ['param', 'var']:
    check_parse(kw + ' a = x + y;',
                ampl.Decl(kw, 'a', None, [ampl.InitAttr(e1)]))
    check_parse(kw + ' a in [x + y, -x];',
                ampl.Decl(kw, 'a', None, [ampl.InAttr(e1, e2)]))

def test_parse_obj_body():
  decl = ampl.Decl('minimize', 'o')
  decl.body = ampl.BinaryExpr('+', ref('x'), ref('y'))
  check_parse('minimize o: x + y;', decl)

def check_parse_expr(input, expr):
  "Check parsing arithmetic expression."
  assert equal_nodes(ampl.parse('var x = {};'.format(input), 'in'),
                     ampl.CompoundStmt([ampl.Decl('var', 'x', None, [ampl.InitAttr(expr)])]))

def check_parse_lexpr(input, expr):
  "Check parsing logical expression."
  check_parse_expr('if {} then 1'.format(input), ampl.IfExpr(expr, ref('1')))

def test_parse_expr():
  check_parse_expr('42', ref('42'))
  check_parse_expr('-x', ampl.UnaryExpr('-', ref('x')))
  check_parse_expr('(x)', ampl.ParenExpr(ref('x')))
  check_parse_expr('sum{S} x', ampl.SumExpr(ampl.Indexing(ref('S')), ref('x')))
  check_parse_expr('sum{s in S} x', ampl.SumExpr(ampl.Indexing(ref('S'), 's'), ref('x')))
  check_parse_expr('if x then y', ampl.IfExpr(ref('x'), ref('y')))
  check_parse_expr('if x then y else z', ampl.IfExpr(ref('x'), ref('y'), ref('z')))
  for f in ['abs', 'acos', 'acosh', 'alias', 'asin', 'asinh', 'atan', 'atan2', 'atanh',
            'ceil', 'ctime', 'cos', 'exp', 'floor', 'log', 'log10', 'max', 'min',
            'precision', 'round', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'time', 'trunc']:
    check_parse_expr(f + '(x)', ampl.CallExpr(f, [ref('x')]))
  check_parse_expr('x[y]', ampl.SubscriptExpr('x', ref('y')))
  for op in ['^', '**', '+', '-', '*', '/']:
    check_parse_expr('x ' + op + ' y', ampl.BinaryExpr(op, ref('x'), ref('y')))
  for op in ['||', 'or', 'in', '<', '<=', '=', '==', '<>', '!=', '<=', '>']:
    check_parse_lexpr('x ' + op + ' y', ampl.BinaryExpr(op, ref('x'), ref('y')))

def test_parse_expr_precedence():
  x = ref('x')
  y = ref('y')
  z = ref('z')
  check_parse_lexpr('(x || y)', ampl.ParenExpr(ampl.BinaryExpr('||', x, y)))
  idx = ampl.Indexing(ref('S'))
  check_parse_lexpr('sum{S} x * y', ampl.SumExpr(idx, ampl.BinaryExpr('*', x, y)))
  check_parse_lexpr('sum{S} x + y', ampl.BinaryExpr('+', ampl.SumExpr(idx, x), y))
  check_parse_expr('if x || y then z', ampl.IfExpr(ampl.BinaryExpr('||', x, y), z))
  check_parse_expr('if x then y & z', ampl.IfExpr(x, ampl.BinaryExpr('&', y, z)))
  check_parse_lexpr('if x then y in S', ampl.BinaryExpr('in', ampl.IfExpr(x, y), ref('S')))
  check_parse_expr('if x then y else x & z', ampl.IfExpr(x, y, ampl.BinaryExpr('&', x, z)))
  check_parse_lexpr('if x then y else z in S', ampl.BinaryExpr('in', ampl.IfExpr(x, y, z), ref('S')))
  check_parse_expr('sin(if x then y)', ampl.CallExpr('sin', [ampl.IfExpr(x, y)]))
  check_parse_expr('a[if x then y]', ampl.SubscriptExpr('a', ampl.IfExpr(x, y)))
  check_parse_lexpr('x || y > z', ampl.BinaryExpr('||', x, ampl.BinaryExpr('>', y, z)))
  check_parse_lexpr('x || y in z', ampl.BinaryExpr('||', x, ampl.BinaryExpr('in', y, z)))
  
  
def test_parse_associativity():
  x = ref('x')
  y = ref('y')
  z = ref('z')
  check_parse_lexpr('x + y + z', ampl.BinaryExpr('+', ampl.BinaryExpr('+', x, y), z))
  check_parse_lexpr('x + y - z', ampl.BinaryExpr('-', ampl.BinaryExpr('+', x, y), z))
  check_parse_lexpr('x * y * z', ampl.BinaryExpr('*', ampl.BinaryExpr('*', x, y), z))
  check_parse_lexpr('x * y / z', ampl.BinaryExpr('/', ampl.BinaryExpr('*', x, y), z))
  check_parse_lexpr('x ^ y ^ z', ampl.BinaryExpr('^', x, ampl.BinaryExpr('^', y, z)))

def test_parse_data():
  check_parse('data;', ampl.IncludeStmt('data'))
  check_parse(
    '''
    data;
    param:
    S: a b :=
    1  2 3;
    ''',
    ampl.IncludeStmt('data'), ampl.DataStmt('param', 'S', ['a', 'b'], ['1', '2', '3']))
