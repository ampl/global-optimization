# A basic AMPL parser and AST.

import re

class ParenExpr:
  "Parenthesized expression"
  def __init__(self, arg):
    self.arg = arg

  def __repr__(self):
    return '({})'.format(str(self.arg))

class UnaryExpr:
  "Unary expression"
  def __init__(self, op, arg):
    self.op = op
    self.arg = arg

  def __repr__(self):
    return self.op + str(self.arg)

class BinaryExpr:
  "Binary expression"
  def __init__(self, op, lhs, rhs):
    self.op = op
    self.lhs = lhs
    self.rhs = rhs

  def __repr__(self):
    return '{} {} {}'.format(self.lhs, self.op, self.rhs)

class Indexing:
  "Indexing expression"
  def __init__(self, index, set_expr):
    self.index = index
    self.set_expr = set_expr

  def __repr__(self):
    return '{{{} in {}}}'.format(self.index, self.set_expr)

class SumExpr:
  "Sum expression"
  def __init__(self, indexing, arg):
    self.indexing = indexing
    self.arg = arg

  def __repr__(self):
    return 'sum {} {}'.format(self.indexing, self.arg)

class CallExpr:
  "Call expression"
  def __init__(self, func_name, arg):
    self.func_name = func_name
    self.arg = arg

  def __repr__(self):
    return '{}({})'.format(self.func_name, self.arg)

class InitAttr:
  "Init attribute (= init)"
  def __init__(self, init):
    self.init = init

  def __repr__(self):
    return '= {}'.format(self.init)

class InAttr:
  "In attribute (in [lb, ub])"
  def __init__(self, lb, ub):
    self.lb = lb
    self.ub = ub

  def __repr__(self):
    return 'in [{}, {}]'.format(self.lb, self.ub)

class Decl:
  "AMPL declaration"

  def __init__(self, kind, name, attrs=[]):
    self.kind = kind
    self.name = name
    self.body = None
    self.attrs = attrs

  def __repr__(self):
    result = self.kind + ' ' + self.name
    for attr in self.attrs:
      result += ' ' + str(attr)
    if self.body:
      result += ': ' + str(self.body)
    return result + ';'

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
    '+': ADDITIVE,
    '-': ADDITIVE,
    '*': MULTIPLICATIVE,
    '/': MULTIPLICATIVE
  }
  
  funcs = {
    'abs', 'acos', 'acosh', 'alias', 'asin', 'asinh', 'atan', 'atan2', 'atanh',
    'ceil', 'ctime', 'cos', 'exp', 'floor', 'log', 'log10', 'max', 'min',
    'precision', 'round', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'time', 'trunc'}

  def get_bin_op_precedence(op):
    return precedence.get(op, UNKNOWN)

  # Current position in input.
  pos = 0
  space_re = re.compile(r'[ \t\r]*(#.*)?')
  token_re = re.compile(r'([a-zA-Z0-9_.]+|.)?')
  token = None # Next token
  lineno = 1

  def report_error(message):
    raise Exception('{}:{}: {}'.format(name, lineno, message))
  
  def consume_token(expected_token=None):
    "Consume token."
    nonlocal pos, token, lineno
    if expected_token and token != expected_token:
      report_error("expected '{}'".format(expected_token))
    old_token = token
    while True:
      m = space_re.match(input, pos)
      pos = m.end(0)
      if pos < len(input) and input[pos] == '\n':
        lineno += 1
        pos += 1
      else:
        break
    m = token_re.match(input, pos)
    pos = m.end(0)
    token = m.group(0)
    return old_token

  def parse_set_expr():
    "Parse a set expression."
    return consume_token()

  def parse_indexing():
    "Parse an indexing expression."
    consume_token('{')
    index = consume_token()
    consume_token('in')
    expr = parse_set_expr()
    consume_token('}')
    return Indexing(index, expr)

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
    elif t in funcs:
      consume_token('(')
      arg = parse_expr()
      consume_token(')')
      expr = CallExpr(t, arg)
    else:
      expr = t
    if token == '^' or token == '**':
      op = consume_token()
      return BinaryExpr(op, expr, parse_unary_expr())
    return expr

  def parse_rhs_of_binary_expr(lhs, min_prec):
    next_token_prec = get_bin_op_precedence(token)
    while True:
      if next_token_prec < min_prec:
        return lhs
      op = consume_token()
      rhs = parse_unary_expr()
      prec = next_token_prec
      next_token_prec = get_bin_op_precedence(token)
      if prec < next_token_prec:
        rhs = parse_rhs_of_binary_expr(rhs, prec + 1)
        next_token_prec = get_bin_op_precedence(token)
      assert prec >= next_token_prec
      lhs = BinaryExpr(op, lhs, rhs);

  def parse_expr(min_prec=UNKNOWN + 1):
    "Parse a numeric expression using operator-precedence parsing."
    lhs = parse_unary_expr()
    if lhs is None:
      return lhs
    return parse_rhs_of_binary_expr(lhs, min_prec)

  def parse_param_or_var():
    "Parse a parameter or a variable declaration."
    kind = consume_token() # consume keyword
    name = consume_token()
    attrs = []
    if token == '=':
      consume_token()
      init = parse_expr()
      attrs.append(InitAttr(init))
    if token == 'in':
      consume_token()
      consume_token('[')
      lb = parse_expr()
      consume_token(',')
      ub = parse_expr()
      consume_token(']')
      attrs.append(InAttr(lb, ub))
    consume_token(';')
    return Decl(kind, name, attrs)

  def parse_set():
    "Parse a set declaration."
    kind = consume_token() # consume 'set'
    name = consume_token()
    consume_token(';')
    return Decl(kind, name)

  def parse_obj():
    "Parse an objective declaration."
    consume_token() # consume keyword
    name = consume_token()
    obj = Decl('minimize', name)
    token = consume_token()
    if token == ':':
      obj.body = parse_expr()
    consume_token(';')
    return obj

  decls = []
  consume_token()
  while True:
    if not token:
      break
    elif token == 'param' or token == 'var':
      decls.append(parse_param_or_var())
    elif token == 'set':
      decls.append(parse_set())
    elif token == 'minimize':
      decls.append(parse_obj())
    else:
      report_error('unknown token: ' + token)
  return decls
