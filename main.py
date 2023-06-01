from sly import Parser
from sly.yacc import _decorator as _
from miku_lexer import MikuLexer
from miku_quadruple import Quadruple
#from miku_semanticcube import miku_semantic_cube as sm


class MikuParser(Parser):
  debugfile = 'parser.out'
  tokens = MikuLexer.tokens
  start = 'program'

  quadruples = []
  quadcount = 0

  myQuad = Quadruple(0, 0, 0, 0)
  t1 = 0

  operandos = []
  operadores = []

  # Grammar rules and actions
  @_('DRAWING ID declaration')
  def program(self, p):
    return 'program'
    ##print(f'program {p[0]}')

  @_('var_declaration func_declaration main')
  def declaration(self, p):
    return 'declaration'
    #print(f'declaration {p}')

  @_('var_type ID multiple_var \n')
  def var_declaration(self, p):
    return 'var_declaration'
    #print(f'var_declaration{p[0]}')

  @_('COMMA ID multiple_var', 'empty')
  def multiple_var(self, p):
    return 'multiple_var'
    #print(f'multiple_var {p[0]}')

  @_('NUMBER', 'WORD', 'BOOL')
  def var_type(self, p):
    return 'var_type'
    #print(f'var_type {p[0]}')

  @_('func_type FUNC ID OPEN_PTH parameter CLOSE_PTH \n stmnt END \n', 'empty')
  def func_declaration(self, p):
    return 'func_declaration'
    #print(f'func_declaration {p[0]}')

  @_('VOID', 'NUMBER', 'WORD', 'BOOL')
  def func_type(self, p):
    return 'func_type'
    #print(f'func_type {p[0]}')

  @_('var_type ID multiple_parameters', 'empty')
  def parameter(self, p):
    return 'parameter'
    #print(f'parameter {p[0]}')

  @_('COMMA parameter', 'empty')
  def multiple_parameters(self, p):
    return 'multiple_parameters'
    #print(f'multiple_parameters {p[0]}')

  @_('var_assignation stmnt', 'func_call stmnt', 'read stmnt', 'write stmnt',
     'if_stmnt stmnt', 'while_stmnt stmnt', 'move_func stmnt',
     'pen_func stmnt', 'var_declaration_func stmnt', 'empty')
  def stmnt(self, p):
    return 'stmnt'
    #print(f'stmnt {p[0]}')

  @_('var_type ID multiple_vars \n')
  def var_declaration_func(self, p):
    return 'var_declaration_func'

    #print(f'var_declaration_func {p[0]}')

  @_('ID ASSIGN expression \n')
  def var_assignation(self, p):
    return 'var_assignation'
    #print(f'var_assignation {p[0]}')
  
  @_('variable', 'CTE_NUM', 'CTE_STR', 'cte_bool', 'func_call')
  def var_cte(self, p):
    return p[0]
    #print(f'var_cte {p[0]}')

  @_('TRUE', 'FALSE')
  def cte_bool(self, p):
    return 'bool'
    #print(f'cte_bool {p[0]}')

  @_('exp rel_op exp', 'exp')
  def expression(self, p):
    return p[0]
    #print(f'expression {p[0]}')

  @_('termino e1 term_op e2 termino e1 quads1 ', 'termino')
  def exp(self, p):
    return p[0]
    #print(f'exp {p[0]}')

  @_('factor e1 fact_op factor e1 quads','factor')
  def termino(self, p):
    return p[0]
    #print(f'termino {p[0]}')

  @_('OPEN_PTH expression CLOSE_PTH', 'var_cte', 'term_op var_cte')
  def factor(self, p):
    if (p[0] == '('):
      return p[1]
    else:
      return p[0]
    #print(f'factor {p[0]}')

  @_('SUM', 'SUB')
  def term_op(self, p):
    return p[0]
    #print(f'term_op {p[0]}')
    
  @_('MULT', 'DIV')
  def fact_op(self, p):
    self.operadores.append(p[-1])
    # print(self.operadores)
    ##print(f'fact_op {p[0]}')

  @_('')
  def e1 (self,p):
    self.operandos.append(p[-1])
    # print(f'operandos {self.operandos}')

  @_('')
  def e2 (self,p):
    self.operadores.append(p[-1])
    # print(f'operadores {self.operadores}')

  @_('')
  def quads(self, p):
    t1 = 0
    myQuad = Quadruple(self.operandos.pop(), self.operandos.pop(), self.operadores.pop(), t1)
    print(myQuad)

  @_('')
  def quads1(self, p):
    t1 = 0
    myQuad = Quadruple(self.operandos.pop(), self.operandos.pop(), self.operadores.pop(), t1)
    print(myQuad)

  @_('AND', 'OR')
  def log_op(self, p):
    return 'log_op'
    #print(f'log_op "{p[0]}"')

  @_('LESS_THAN', 'MORE_THAN', 'DIFFERENT_TO', 'LESS_OR_EQ_THAN',
     'MORE_OR_EQ_THAN', 'EQUAL_TO')
  def rel_op(self, p):
    return 'rel_op'
    #print(f'rel_op {p[0]}')

  @_('ID OPEN_PTH func_call_param CLOSE_PTH \n')
  def func_call(self, p):
    return 'func_call'
    #print(f'func_call {p[0]}')

  @_('expression multiple_fc_param')
  def func_call_param(self, p):
    return 'func_call_param'
    #print(f'func_call param {p[0]}')

  @_('COMMA func_call_param', 'empty')
  def multiple_fc_param(self, p):
    return 'multiple_fc_param'
    #print(f'multiple_fc_param {p[0]}')

  @_('READ OPEN_PTH variable multiple_vars CLOSE_PTH \n')
  def read(self, p):
    return 'read'
    #print(f'read {p[0]}')

  @_('ID array')
  def variable(self, p):
    return p[0]
    #print(f'variable {p[0]}')

  @_('OPEN_SQR expression CLOSE_SQR matrix', 'empty')
  def array(self, p):
    return 'array'
    #print(f'array {p[0]}')

  @_('OPEN_SQR expression CLOSE_SQR', 'empty')
  def matrix(self, p):
    return 'matrix'
    #print(f'matrix {p[0]}')

  @_('COMMA variable', 'empty')
  def multiple_vars(self, p):
    return 'multiple_vars'
    #print(f'multiple_vars {p[0]}')

  @_('WRITE OPEN_PTH expression CLOSE_PTH \n')
  def write(self, p):
    return 'write'
    #print(f'write {p[0]}')

  # @_('COMMA expression', 'empty')
  # def multiple_expression(self, p):
  #   return 'multiple_expression'

  # @_('\n stmnt multiple_con_stmnt')
  # def multiple_con_stmnt(self, p):
  #   #print(f'multiple_con_stmnt {p[0]}')

  @_('IF con_expression \n stmnt else_stmnt')
  def if_stmnt(self, p):
    return 'if_stmnt'
    #print(f'if_stmnt {p[0]}')

  @_('\n ELSE \n stmnt END \n', '\n END \n')
  def else_stmnt(self, p):
    return 'else_stmnt'
    #print(f'else_stmnt {p[0]}')

  @_('WHILE con_expression \n stmnt \n END \n')
  def while_stmnt(self, p):
    return 'while_stmnt'
    #print(f'while_stmnt {p[0]}')

  @_('expression log_op expression')
  def con_expression(self, p):
    return 'con_expression'
    #print(f'con_expression {p[0]}')

  @_('move_type OPEN_PTH func_call_param CLOSE_PTH')
  def move_func(self, p):
    return 'move_func'
    #print(f'move_func {p[0]}')

  @_('LEFT', 'RIGHT', 'FORWARD', 'CENTER')
  def move_type(self, p):
    return 'move_type'
    #print(f'move_type {p[0]}')

  @_('PEN_UP OPEN_PTH CLOSE_PTH \n', 'PEN_DOWN OPEN_PTH CLOSE_PTH \n')
  def pen_func(self, p):
    return 'pen_func'
    #print(f'pen_func {p[0]}')

  @_('MAIN \n stmnt END')
  def main(self, p):
    return 'main'
    #print(f'main {p[0]}')

  @_('')
  def empty(self, p):
    pass


# Semantics

if __name__ == '__main__':
  lexer = MikuLexer()
  parser = MikuParser()
  filename = 'test.txt'

  with open(filename) as fp:
    try:
      result = parser.parse(lexer.tokenize(fp.read()))
      print(result)
    except EOFError:
      pass
