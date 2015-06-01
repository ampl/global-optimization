#!/usr/bin/env python
# Merge multiple AMPL problems into a single one.
# For example, two problems
#   minimize o: f1(x);
# and
#   minimize o: f2(x);
# are combined into a single problem
#   minimize o: f1(x1) + f2(x2);

from __future__ import print_function
import ampl, glob, os, util

def find_obj(nodes):
  for i in range(len(nodes)):
    node = nodes[i]
    if isinstance(node, ampl.Decl) and (node.kind == 'minimize' or node.kind == 'maximize'):
      return i

class RenamingVisitor:
  def __init__(self, names):
    self.names = names

  def visit_reference(self, expr):
    expr.name = self.names.get(expr.name, expr.name)

  def visit_subscript(self, expr):
    self.visit_reference(expr)

  def visit_paren(self, expr):
    expr.arg.accept(self)

  def visit_unary(self, expr):
    expr.arg.accept(self)

  def visit_binary(self, expr):
    expr.lhs.accept(self)
    expr.rhs.accept(self)

  def visit_if(self, expr):
    expr.condition.accept(self)
    expr.true_expr.accept(self)
    expr.false_expr.accept(self)

  def visit_call(self, expr):
    expr.arg.accept(self)

  def visit_sum(self, expr):
    expr.indexing.accept(self)
    expr.arg.accept(self)

  def visit_indexing(self, expr):
    expr.set_expr.accept(self)

def parse(model, suffix):
  suffix = str(suffix)
  with open(os.path.join(util.repo_dir, model), 'r') as f:
    nodes = ampl.parse(f.read(), model)
    # Rename declarations.
    names = {}
    visitor = RenamingVisitor(names)
    for n in nodes:
      if type(n) is ampl.Decl:
        new_name = n.name + suffix
        names[n.name] = new_name
        n.name = new_name
        if n.body:
          n.body.accept(visitor)
    # Find the first objective and partition the nodes around it.
    obj_index = find_obj(nodes)
    return nodes[:obj_index], nodes[obj_index], nodes[obj_index + 1:]

def print_ast(nodes):
  for node in nodes:
    print(node)

models = util.get_models('casado', 'hansen')
for m1 in models:
  for m2 in models:
    print(m1, m2)
    head1, obj1, tail1 = parse(m1, 1)
    head2, obj2, tail2 = parse(m2, 2)
    obj = ampl.Decl('minimize', 'f')
    # Invert sign if objectives are of different kinds.
    obj.body = ampl.BinaryExpr('*', ampl.ParenExpr(obj1.body), ampl.ParenExpr(obj2.body))
    if obj1.kind != obj2.kind:
      obj.body = ampl.UnaryExpr('-', obj.body)
    print_ast(head1 + head2 + [obj] + tail1 + tail2)
