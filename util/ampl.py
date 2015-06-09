# A basic AMPL parser and AST.
# Copyright (c) 2015, Victor Zverovich

import re

class Reference(object):
  "Reference"
  def __init__(self, name):
    self.name = name

  def accept(self, visitor):
    return visitor.visit_reference(self)

class SubscriptExpr(object):
  "Subscript expression"
  def __init__(self, name, subscript):
    self.name = name
    self.subscript = subscript

  def accept(self, visitor):
    return visitor.visit_subscript(self)

class ParenExpr(object):
  "Parenthesized expression"
  def __init__(self, arg):
    self.arg = arg

  def accept(self, visitor):
    return visitor.visit_paren(self)

class UnaryExpr(object):
  "Unary expression"
  def __init__(self, op, arg):
    self.op = op
    self.arg = arg

  def accept(self, visitor):
    return visitor.visit_unary(self)

class BinaryExpr(object):
  "Binary expression"
  def __init__(self, op, lhs, rhs):
    self.op = op
    self.lhs = lhs
    self.rhs = rhs

  def accept(self, visitor):
    return visitor.visit_binary(self)

class IfExpr(object):
  "If expression"
  def __init__(self, condition, then_expr, else_expr=None):
    self.condition = condition
    self.then_expr = then_expr
    self.else_expr = else_expr

  def accept(self, visitor):
    return visitor.visit_if(self)

class CallExpr(object):
  "Call expression"
  def __init__(self, func_name, args):
    self.func_name = func_name
    self.args = args

  def accept(self, visitor):
    return visitor.visit_call(self)

class SumExpr(object):
  "Sum expression"
  def __init__(self, indexing, arg):
    self.indexing = indexing
    self.arg = arg

  def accept(self, visitor):
    return visitor.visit_sum(self)

class Indexing(object):
  "Indexing expression"
  def __init__(self, set_expr, index=None):
    self.set_expr = set_expr
    self.index = index

  def accept(self, visitor):
    return visitor.visit_indexing(self)

class InitAttr(object):
  "Init attribute ``= init``"
  def __init__(self, init):
    self.init = init

  def accept(self, visitor):
    return visitor.visit_init(self)

class InAttr(object):
  "In attribute ``in [lb, ub]``"
  def __init__(self, lb, ub):
    self.lb = lb
    self.ub = ub

  def accept(self, visitor):
    return visitor.visit_in(self)

class Decl(object):
  "AMPL declaration"

  def __init__(self, kind, name, indexing=None, attrs=None):
    self.kind = kind
    self.name = name
    self.indexing = indexing
    self.body = None
    self.attrs = attrs if attrs else []

  def accept(self, visitor):
    return visitor.visit_decl(self)

class IncludeStmt(object):
  "Include statement such as include, model or data"

  def __init__(self, kind):
    self.kind = kind

  def accept(self, visitor):
    return visitor.visit_include(self)

class DataStmt(object):
  "Data statement"
  
  def __init__(self, kind, set_name, param_names, values):
    self.kind = kind
    self.set_name = set_name
    self.param_names = param_names
    self.values = values

  def accept(self, visitor):
    return visitor.visit_data(self)

class CompoundStmt(object):
  def __init__(self, nodes=None):
    self.nodes = nodes if nodes else []

  def accept(self, visitor):
    return visitor.visit_compound(self)

class PrettyPrinter:
  "Pretty printer for AMPL AST without precedence handling"

  def __init__(self, stream):
    self.stream = stream

  def visit_reference(self, expr):
    self.stream.write(expr.name)

  def visit_subscript(self, expr):
    self.stream.write(expr.name + '[')
    expr.subscript.accept(self)
    self.stream.write(']')

  def visit_paren(self, expr):
    self.stream.write('(')
    expr.arg.accept(self)
    self.stream.write(')')

  def visit_unary(self, expr):
    self.stream.write(expr.op)
    expr.arg.accept(self)

  def visit_binary(self, expr):
    expr.lhs.accept(self)
    self.stream.write(' ' + expr.op + ' ')
    expr.rhs.accept(self)

  def visit_if(self, expr):
    self.stream.write('if ')
    expr.condition.accept(self)
    self.stream.write(' then ')
    expr.then_expr.accept(self)
    if expr.else_expr:
      self.stream.write(' else ')
      expr.else_expr.accept(self)

  def visit_call(self, expr):
    self.stream.write(expr.func_name + '(')
    for i in range(len(expr.args)):
      if i != 0:
        self.stream.write(', ')
      expr.args[i].accept(self)
    self.stream.write(')')

  def visit_sum(self, expr):
    self.stream.write('sum')
    expr.indexing.accept(self)
    self.stream.write(' ')
    expr.arg.accept(self)

  def visit_indexing(self, expr):
    self.stream.write('{')
    if expr.index:
      self.stream.write(expr.index + ' in ')
    expr.set_expr.accept(self)
    self.stream.write('}')

  def visit_init(self, attr):
    self.stream.write('= ')
    attr.init.accept(self)

  def visit_in(self, attr):
    self.stream.write('in [')
    attr.lb.accept(self)
    self.stream.write(', ')
    attr.ub.accept(self)
    self.stream.write(']')

  def visit_decl(self, decl):
    self.stream.write(decl.kind + ' ' + decl.name)
    if decl.indexing:
      decl.indexing.accept(self)
    for attr in decl.attrs:
      self.stream.write(' ')
      attr.accept(self)
    if decl.body:
      self.stream.write(': ')
      decl.body.accept(self)
    self.stream.write(';\n')

  def visit_include(self, stmt):
    self.stream.write(stmt.kind + ';\n')

  def visit_data(self, stmt):
    self.stream.write(stmt.kind + ':\n')
    num_cols = len(stmt.param_names) + 1
    col_widths = [len(stmt.set_name)] + [len(n) for n in stmt.param_names]
    num_values = len(stmt.values)
    for i in range(num_values):
      col = i % num_cols
      col_widths[col] = max(col_widths[col], len(stmt.values[i]))

    def format_row(values, first_sep=' '):
      self.stream.write('{:>{}}'.format(values[0], col_widths[0]))
      for i in range(1, len(values)):
        self.stream.write('{}{:>{}}'.format(first_sep, values[i], col_widths[i]))
        first_sep = ' '

    format_row([stmt.set_name] + stmt.param_names, ':')
    self.stream.write(' :=\n')
    for i in range(0, num_values, num_cols):
      format_row(stmt.values[i:i + num_cols])
      self.stream.write('\n')
    self.stream.write(';\n')

  def visit_compound(self, stmt):
    for node in stmt.nodes:
      node.accept(self)

def pretty_print(stream, node):
  "Pretty print the AST node."
  node.accept(PrettyPrinter(stream))

def parse(input, name):
  "Parse AMPL code (kind of)."

  # Operator precedence
  UNKNOWN          =  0
  LOGICAL_OR       =  1 # || or
  ITERATED_LOGICAL =  2 # exists forall
  LOGICAL_AND      =  3 # && and
  RELATIONAL       =  4 # < <= = == <> != >= >
  MEMBERSHIP       =  5 # in  not in
  CONDITIONAL      =  6 # if then else
  CONCATENATION    =  7 # &
  UNION            =  8 # union diff symdiff
  CROSS            =  9 # cross
  SEQUENCE         = 10 # setof  .. by
  ADDITIVE         = 11 # + - less
  ITERATED         = 12 # sum prod product min max expectation
  MULTIPLICATIVE   = 13 # * / div mod
  UNARY            = 14 # + - ! not
  EXPONENTIATION   = 15 # ^ **
  
  precedence = {
    '||': LOGICAL_OR,
    'or': LOGICAL_OR,
    'in': MEMBERSHIP,
    '<' : RELATIONAL,
    '<=': RELATIONAL,
    '=' : RELATIONAL,
    '==': RELATIONAL,
    '<>': RELATIONAL,
    '!=': RELATIONAL,
    '<=': RELATIONAL,
    '>' : RELATIONAL,
    '&' : CONCATENATION,
    '+' : ADDITIVE,
    '-' : ADDITIVE,
    '*' : MULTIPLICATIVE,
    '/' : MULTIPLICATIVE
  }
  
  funcs = {
    'abs', 'acos', 'acosh', 'alias', 'asin', 'asinh', 'atan', 'atan2', 'atanh',
    'ceil', 'ctime', 'cos', 'exp', 'floor', 'log', 'log10', 'max', 'min',
    'precision', 'round', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'time', 'trunc'}

  def get_bin_op_precedence(op):
    return precedence.get(op, UNKNOWN)

  class Namespace: pass
  ns = Namespace()
  ns.pos = 0 # Current position in input
  space_re = re.compile(r'[ \t\r]*(#.*)?')
  token_re = re.compile(r'([a-zA-Z0-9_.]+|:=|<=|==|<>|!=|>=|\*\*|\|\||or|in|.)?')
  ns.token = None # Next token
  ns.lineno = 1

  def report_error(message):
    raise Exception('{}:{}: {}'.format(name, ns.lineno, message))
  
  def consume_token(expected_token=None):
    "Consume token."
    if expected_token and ns.token != expected_token:
      report_error("expected '{}'".format(expected_token))
    old_token = ns.token
    while True:
      m = space_re.match(input, ns.pos)
      ns.pos = m.end(0)
      if ns.pos < len(input) and input[ns.pos] == '\n':
        ns.lineno += 1
        ns.pos += 1
      else:
        break
    m = token_re.match(input, ns.pos)
    ns.pos = m.end(0)
    ns.token = m.group(0)
    return old_token

  def parse_set_expr():
    "Parse a set expression."
    return Reference(consume_token())

  def parse_indexing():
    "Parse an indexing expression."
    consume_token('{')
    index = None
    token = consume_token()
    if ns.token == 'in':
      consume_token()
      index = token
      expr = parse_set_expr()
    else:
      expr = Reference(token)
    consume_token('}')
    return Indexing(expr, index)

  def parse_unary_expr():
    "Parse a unary numeric expression."
    t = consume_token()
    if t == '-':
      return UnaryExpr('-', parse_unary_expr())
    elif t == '(':
      arg = parse_expr()
      consume_token(')')
      expr = ParenExpr(arg)
    elif t == 'sum':
      indexing = parse_indexing()
      arg = parse_expr(ITERATED + 1)
      return SumExpr(indexing, arg)
    elif t == 'if':
      condition = parse_expr()
      consume_token('then')
      then_expr = parse_expr(CONDITIONAL)
      else_expr = None
      if ns.token == 'else':
        consume_token('else')
        else_expr = parse_expr(CONDITIONAL)
      return IfExpr(condition, then_expr, else_expr)
    elif t in funcs:
      consume_token('(')
      arg = parse_expr()
      consume_token(')')
      expr = CallExpr(t, [arg])
    elif ns.token == '[':
      consume_token()
      subscript = parse_expr()
      consume_token(']')
      expr = SubscriptExpr(t, subscript)
    else:
      expr = Reference(t)
    if ns.token == '^' or ns.token == '**':
      op = consume_token()
      return BinaryExpr(op, expr, parse_unary_expr())
    return expr

  def parse_rhs_of_binary_expr(lhs, min_prec):
    next_token_prec = get_bin_op_precedence(ns.token)
    while True:
      if next_token_prec < min_prec:
        return lhs
      op = consume_token()
      rhs = parse_unary_expr()
      prec = next_token_prec
      next_token_prec = get_bin_op_precedence(ns.token)
      if prec < next_token_prec:
        rhs = parse_rhs_of_binary_expr(rhs, prec + 1)
        next_token_prec = get_bin_op_precedence(ns.token)
      assert prec >= next_token_prec
      lhs = BinaryExpr(op, lhs, rhs);

  def parse_expr(min_prec=UNKNOWN + 1):
    "Parse a numeric expression using operator-precedence parsing."
    lhs = parse_unary_expr()
    if lhs is None:
      return lhs
    return parse_rhs_of_binary_expr(lhs, min_prec)

  def parse_decl_start():
    kind = consume_token() # consume keyword
    name = consume_token()
    return Decl(kind, name, parse_indexing() if ns.token == '{' else None)

  def parse_param_or_var():
    "Parse a parameter or a variable declaration."
    decl = parse_decl_start()
    if ns.token == '=':
      consume_token()
      init = parse_expr(CONDITIONAL)
      decl.attrs.append(InitAttr(init))
    if ns.token == 'in':
      consume_token()
      consume_token('[')
      lb = parse_expr()
      consume_token(',')
      ub = parse_expr()
      consume_token(']')
      decl.attrs.append(InAttr(lb, ub))
    consume_token(';')
    return decl

  def parse_set():
    "Parse a set declaration."
    decl = parse_decl_start()
    consume_token(';')
    return decl

  def parse_obj():
    "Parse an objective declaration."
    decl = parse_decl_start()
    if ns.token == ':':
      consume_token()
      decl.body = parse_expr()
    consume_token(';')
    return decl

  def parse_model(compound):
    "Parse AMPL model returning True on EOF or False to switch to the data mode."
    while True:
      if not ns.token:
        return True
      if ns.token == 'param' or ns.token == 'var':
        compound.nodes.append(parse_param_or_var())
      elif ns.token == 'set':
        compound.nodes.append(parse_set())
      elif ns.token == 'minimize' or ns.token == 'maximize':
        compound.nodes.append(parse_obj())
      elif ns.token == 'data':
        kind = consume_token()
        consume_token(';')
        compound.nodes.append(IncludeStmt(kind))
        return False
      else:
        report_error('unknown token: ' + ns.token)

  def parse_data(compound):
    "Parse AMPL data returning True on EOF or False to switch to the model mode."
    while True:
      if not ns.token:
        return True
      if ns.token == 'param' or ns.token == 'var':
        kind = consume_token()
        consume_token(':')
        set_name = consume_token()
        consume_token(':')
        param_names = []
        while ns.token and ns.token != ':=':
          param_names.append(consume_token())
        consume_token()
        values = []
        while ns.token and ns.token != ';':
          values.append(consume_token())
        consume_token();
        compound.nodes.append(DataStmt(kind, set_name, param_names, values))
      else:
        return False
  
  consume_token()
  compound = CompoundStmt()
  while True:
    if parse_model(compound) or parse_data(compound):
      return compound
