# AMPL parser and AST tests

import ampl
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
