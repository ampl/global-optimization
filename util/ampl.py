# A basic AMPL parser and AST.

import re

class Reference:
  "Reference expression"
  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return self.name
  
  def accept(self, visitor):
    visitor.visit_reference(self)

class SubscriptExpr:
  "Subscript expression"
  def __init__(self, name, subscript):
    self.name = name
    self.subscript = subscript

  def __repr__(self):
    return '{}[{}]'.format(self.name, self.subscript)

  def accept(self, visitor):
    visitor.visit_subscript(self)

class ParenExpr:
  "Parenthesized expression"
  def __init__(self, arg):
    self.arg = arg

  def __repr__(self):
    return '({})'.format(str(self.arg))
  
  def accept(self, visitor):
    visitor.visit_paren(self)

class UnaryExpr:
  "Unary expression"
  def __init__(self, op, arg):
    self.op = op
    self.arg = arg

  def __repr__(self):
    return self.op + str(self.arg)

  def accept(self, visitor):
    visitor.visit_unary(self)

class BinaryExpr:
  "Binary expression"
  def __init__(self, op, lhs, rhs):
    self.op = op
    self.lhs = lhs
    self.rhs = rhs

  def __repr__(self):
    return '{} {} {}'.format(self.lhs, self.op, self.rhs)

  def accept(self, visitor):
    visitor.visit_binary(self)

class IfExpr:
  "If expression"
  def __init__(self, condition, true_expr, false_expr):
    self.condition = condition
    self.true_expr = true_expr
    self.false_expr = false_expr

  def __repr__(self):
    return 'if {} then {} else {}'.format(
      self.condition, self.true_expr, self.false_expr)

  def accept(self, visitor):
    visitor.visit_if(self)

class Indexing:
  "Indexing expression"
  def __init__(self, index, set_expr):
    self.index = index
    self.set_expr = set_expr

  def __repr__(self):
    result = ''
    if self.index:
      result += self.index + ' in '
    return '{' + result + str(self.set_expr) + '}'

  def accept(self, visitor):
    visitor.visit_indexing(self)

class SumExpr:
  "Sum expression"
  def __init__(self, indexing, arg):
    self.indexing = indexing
    self.arg = arg

  def __repr__(self):
    return 'sum{} {}'.format(self.indexing, self.arg)

  def accept(self, visitor):
    visitor.visit_sum(self)

class CallExpr:
  "Call expression"
  def __init__(self, func_name, arg):
    self.func_name = func_name
    self.arg = arg

  def __repr__(self):
    return '{}({})'.format(self.func_name, self.arg)

  def accept(self, visitor):
    visitor.visit_call(self)

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

  def __init__(self, kind, name, indexing=None, attrs=[]):
    self.kind = kind
    self.name = name
    self.indexing = indexing
    self.body = None
    self.attrs = attrs

  def __repr__(self):
    result = self.kind + ' ' + self.name
    for attr in self.attrs:
      result += ' ' + str(attr)
    if self.indexing:
      result += str(self.indexing)
    if self.body:
      result += ': ' + str(self.body)
    return result + ';'

class IncludeStmt:
  "Include statement such as include, model or data"

  def __init__(self, kind):
    self.kind = kind

  def __repr__(self):
    return self.kind + ';'

class DataStmt:
  "Data statement"
  
  def __init__(self, kind, set_name, param_names, values):
    self.kind = kind
    self.set_name = set_name
    self.param_names = param_names
    self.values = values

  def format_row(self, values, col_widths, first_sep=' '):
    result = '{:>{}}'.format(values[0], col_widths[0])
    for i in range(1, len(values)):
      result += '{}{:>{}}'.format(first_sep, values[i], col_widths[i])
      first_sep = ' '
    return result

  def __repr__(self):
    result = self.kind + ':\n'
    num_cols = len(self.param_names) + 1
    col_widths = [len(self.set_name)] + [len(n) for n in self.param_names]
    num_values = len(self.values)
    for i in range(num_values):
      col = i % num_cols
      col_widths[col] = max(col_widths[col], len(self.values[i]))
    result += self.format_row([self.set_name] + self.param_names, col_widths, ':')
    result += ' :=\n'
    for i in range(0, num_values, num_cols):
      result += self.format_row(self.values[i:i + num_cols], col_widths) + '\n'
    return result

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
    '<' : RELATIONAL,
    '<=': RELATIONAL,
    '=' : RELATIONAL,
    '==': RELATIONAL,
    '<>': RELATIONAL,
    '!=': RELATIONAL,
    '<=': RELATIONAL,
    '>' : RELATIONAL,
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

  # Current position in input.
  class Namespace: pass
  ns = Namespace()
  ns.pos = 0
  space_re = re.compile(r'[ \t\r]*(#.*)?')
  token_re = re.compile(r'([a-zA-Z0-9_.]+|:=|<=|==|<>|!=|>=|.)?')
  ns.token = None # Next token
  ns.lineno = 1

  def report_error(message):
    print(token)
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
    expr = consume_token()
    if ns.token == 'in':
      consume_token()
      index = expr
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
    elif t == 'if':
      condition = parse_expr()
      consume_token('then')
      true_expr = parse_expr(CONDITIONAL)
      false_expr = None
      if ns.token == 'else':
        consume_token('else')
        false_expr = parse_expr(CONDITIONAL)
      return IfExpr(condition, true_expr, false_expr)
    elif t in funcs:
      consume_token('(')
      arg = parse_expr()
      consume_token(')')
      expr = CallExpr(t, arg)
    else:
      if ns.token == '[':
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

  def parse_param_or_var():
    "Parse a parameter or a variable declaration."
    kind = consume_token() # consume keyword
    name = consume_token()
    indexing = parse_indexing() if ns.token == '{' else None
    attrs = []
    if ns.token == '=':
      consume_token()
      init = parse_expr()
      attrs.append(InitAttr(init))
    if ns.token == 'in':
      consume_token()
      consume_token('[')
      lb = parse_expr()
      consume_token(',')
      ub = parse_expr()
      consume_token(']')
      attrs.append(InAttr(lb, ub))
    consume_token(';')
    return Decl(kind, name, indexing, attrs)

  def parse_set():
    "Parse a set declaration."
    kind = consume_token() # consume 'set'
    name = consume_token()
    consume_token(';')
    return Decl(kind, name)

  def parse_obj():
    "Parse an objective declaration."
    kind = consume_token() # consume keyword
    name = consume_token()
    obj = Decl(kind, name)
    token = consume_token()
    if token == ':':
      obj.body = parse_expr()
    consume_token(';')
    return obj

  def parse_model(nodes):
    "Parse AMPL model returning True on EOF or False to switch to the data mode."
    while True:
      if not ns.token:
        return True
      if ns.token == 'param' or ns.token == 'var':
        nodes.append(parse_param_or_var())
      elif ns.token == 'set':
        nodes.append(parse_set())
      elif ns.token == 'minimize' or ns.token == 'maximize':
        nodes.append(parse_obj())
      elif ns.token == 'data':
        kind = consume_token()
        consume_token(';')
        nodes.append(IncludeStmt(kind))
        return False
      else:
        report_error('unknown token: ' + ns.token)

  def parse_data(nodes):
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
        nodes.append(DataStmt(kind, set_name, param_names, values))
      else:
        return False
  
  consume_token()
  nodes = []
  while True:
    if parse_model(nodes) or parse_data(nodes):
      return nodes
