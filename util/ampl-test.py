# AMPL parser and AST tests

import ampl
from cStringIO import StringIO
from mock import MagicMock

class MockVisitor: pass

def check_accept(node, method_name):
  "Check if node.accept(visitor) calls visitor.method_name(node)."
  visitor = MockVisitor()
  mock = MagicMock()
  setattr(visitor, method_name, mock)
  node.accept(visitor)
  mock.assert_called_with(node)

def test_reference():
  expr = ampl.Reference('foo')
  assert expr.name == 'foo'
  check_accept(expr, 'visit_reference')

def test_subscript():
  expr = ampl.SubscriptExpr('foo', 'bar')
  assert expr.name == 'foo'
  assert expr.subscript == 'bar'
  check_accept(expr, 'visit_subscript')

def test_paren():
  arg = ampl.Reference('a')
  expr = ampl.ParenExpr(arg)
  assert expr.arg == arg
  check_accept(expr, 'visit_paren')

def test_unary():
  arg = ampl.Reference('a')
  expr = ampl.UnaryExpr('-', arg)
  assert expr.op == '-'
  assert expr.arg == arg
  check_accept(expr, 'visit_unary')

def test_binary():
  lhs = ampl.Reference('a')
  rhs = ampl.Reference('b')
  expr = ampl.BinaryExpr('+', lhs, rhs)
  assert expr.op == '+'
  assert expr.lhs == lhs
  assert expr.rhs == rhs
  check_accept(expr, 'visit_binary')

def test_if():
  condition = ampl.Reference('a')
  then_expr = ampl.Reference('b')
  else_expr = ampl.Reference('c')
  expr = ampl.IfExpr(condition, then_expr, else_expr)
  assert expr.condition == condition
  assert expr.then_expr == then_expr
  assert expr.else_expr == else_expr
  expr = ampl.IfExpr(condition, then_expr)
  assert expr.else_expr == None
  check_accept(expr, 'visit_if')

def test_call():
  arg0 = ampl.Reference('a')
  arg1 = ampl.Reference('b')
  expr = ampl.CallExpr('foo', [arg0, arg1])
  assert expr.func_name == 'foo'
  assert expr.args == [arg0, arg1]
  check_accept(expr, 'visit_call')

def test_sum():
  indexing = ampl.Indexing(ampl.Reference('a'))
  arg = ampl.Reference('b')
  expr = ampl.SumExpr(indexing, arg)
  assert expr.indexing == indexing
  assert expr.arg == arg
  check_accept(expr, 'visit_sum')

def test_indexing():
  index = 'a'
  set_expr = ampl.Reference('b')
  expr = ampl.Indexing(set_expr, index)
  assert expr.index == index
  assert expr.set_expr == set_expr
  expr = ampl.Indexing(set_expr)
  assert expr.index == None
  assert expr.set_expr == set_expr
  check_accept(expr, 'visit_indexing')

def test_init():
  init = ampl.Reference('a')
  attr = ampl.InitAttr(init)
  assert attr.init == init
  check_accept(attr, 'visit_init')

def test_in():
  lb = ampl.Reference('a')
  ub = ampl.Reference('b')
  attr = ampl.InAttr(lb, ub)
  assert attr.lb == lb
  assert attr.ub == ub
  check_accept(attr, 'visit_in')

def test_decl():
  indexing = ampl.Indexing(ampl.Reference('a'))
  attrs = [ampl.InitAttr(ampl.Reference('a'))]
  decl = ampl.Decl('var', 'x', indexing, attrs)
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
  assert stmt.kind == 'model'
  check_accept(stmt, 'visit_include')

def test_data():
  param_names = ['a', 'b']
  values = [0, 1, 2, 3, 4, 5]
  stmt = ampl.DataStmt('param', 'S', param_names, values)
  assert stmt.kind == 'param'
  assert stmt.set_name == 'S'
  assert stmt.param_names == param_names
  assert stmt.values == values
  check_accept(stmt, 'visit_data')

def test_compound():
  nodes = [ampl.IncludeStmt('model'), ampl.Decl('var', 'x')]
  stmt = ampl.CompoundStmt(nodes)
  assert stmt.nodes == nodes
  check_accept(stmt, 'visit_compound')

def check_print(output, node):
  "Check if the output of pretty_print for the given AST node."
  stream = StringIO()
  ampl.pretty_print(stream, node)
  assert stream.getvalue() == output

def test_pretty_print():
  check_print('a', ampl.Reference('a'))
  check_print('a[b]', ampl.SubscriptExpr('a', 'b'))
  check_print('(a)', ampl.ParenExpr(ampl.Reference('a')))
  check_print('-a', ampl.UnaryExpr('-', ampl.Reference('a')))
  check_print('a + b', ampl.BinaryExpr('+', ampl.Reference('a'), ampl.Reference('b')))
  check_print('if a then b else c',
              ampl.IfExpr(ampl.Reference('a'), ampl.Reference('b'), ampl.Reference('c')))
  check_print('if a then b',
              ampl.IfExpr(ampl.Reference('a'), ampl.Reference('b'), None))
  check_print('f(a, b)', ampl.CallExpr('f', [ampl.Reference('a'), ampl.Reference('b')]))
  check_print('sum{s in S} x[s]', ampl.SumExpr(ampl.Indexing(ampl.Reference('S'), 's'),
                                               ampl.SubscriptExpr('x', 's')))
  check_print('{s in S}', ampl.Indexing(ampl.Reference('S'), 's'))
  check_print('{S}', ampl.Indexing(ampl.Reference('S')))
  check_print('= a', ampl.InitAttr(ampl.Reference('a')))
  check_print('in [a, b]', ampl.InAttr(ampl.Reference('a'), ampl.Reference('b')))
  check_print('var x{S} = a;\n', ampl.Decl('var', 'x', ampl.Indexing(ampl.Reference('S')),
                                           [ampl.InitAttr(ampl.Reference('a'))]))
  decl = ampl.Decl('minimize', 'o')
  decl.body = ampl.UnaryExpr('-', ampl.Reference('x'))
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
