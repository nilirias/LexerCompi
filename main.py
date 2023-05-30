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

  myQuad = Quadruple(0,0,0,0)
  t1 = 0
  
  operandos = []
  operadores = []

  lo = 0
  ro = 0
  op = ''
  
  # precedence = (
  #      ('left', SUM, SUB),
  #      ('left', MULT, DIV),
  #   )

 # Grammar rules and actions
  @_('DRAWING ID declaration')
  def program(self, p):
    return 'program'
  
  @_('var_declaration func_declaration main')
  def declaration(self,p):
    return 'declaration'
  
  @_('var_type ID multiple_var \n')
  def var_declaration(self, p):
    return 'var_declaration'
  
  @_('COMMA ID multiple_var', 'empty')
  def multiple_var(self, p):
    return 'multiple_var'
  
  @_('NUMBER', 'WORD', 'BOOL')
  def var_type(self, p):
    return 'var_type'
  
  @_('func_type FUNC ID OPEN_PTH parameter CLOSE_PTH \n stmnt END \n','empty')
  def func_declaration(self, p):
    return 'func_declaration'
  
  @_('VOID', 'NUMBER', 'WORD', 'BOOL')
  def func_type(self, p):
    return 'func_type'
  
  @_('var_type ID multiple_parameters', 'empty')
  def parameter(self, p):
    return 'parameter'
  
  @_('COMMA parameter', 'empty')
  def multiple_parameters(self, p):
    return 'multiple_parameters'
  
  @_('var_assignation stmnt','func_call stmnt', 'read stmnt', 'write stmnt', 'if_stmnt stmnt', 'while_stmnt stmnt', 'move_func stmnt', 'pen_func stmnt', 'var_declaration_func stmnt', 'empty')
  def stmnt(self, p):
    return 'stmnt'

  @_('var_type ID multiple_vars \n')
  def var_declaration_func(self,p):
    return 'var_declaration_func'
  
  @_('ID ASSIGN var_cte \n', 'ID ASSIGN expression \n')
  def var_assignation(self, p):
    return 'var_assignation'
  
  @_('variable', 'CTE_NUM', 'CTE_STR', 'cte_bool', 'func_call')
  def var_cte(self, p):
    return p[0]

  @_('TRUE', 'FALSE')
  def cte_bool(self, p):
    return 'cte_bool'
  
  @_('complex_expr', 'var_cte', 'mult_expr')
  def expression(self, p):
    return p[0]
  
  @_('OPEN_PTH expression CLOSE_PTH')
  def mult_expr(self, p):
    return 'mult_expr'
  
  @_('expression e1 operator expression e2 quads')
  def complex_expr(self, p):
    return 'complex_expr'

  @_('')
  def e1(self, p):
    self.operandos.append(p[-1])
    print(self.operandos)

  @_('')
  def e2(self, p):
    self.operandos.append(p[-1])
    print(self.operandos)

  @_('')
  def quads(self, p):
    t1 = 0
    myQuad = Quadruple(self.operandos.pop(), self.operandos.pop(), self.operadores.pop(), t1)
    print(myQuad)
  
  @_('art_op', 'log_op', 'rel_op')
  def operator(self, p):
    return 'operator'
  
  @_('SUM', 'SUB', 'MULT', 'DIV')
  def art_op(self, p):
    self.operadores.append(p[-1])
    print(self.operadores)
    return 'art_op'
  
  @_('AND', 'OR')
  def log_op(self, p):
    return 'log_op'
  
  @_('LESS_THAN', 'MORE_THAN', 'DIFFERENT_TO', 'LESS_OR_EQ_THAN', 'MORE_OR_EQ_THAN', 'EQUAL_TO')
  def rel_op(self, p):
    return 'rel_op'
  
  @_('ID OPEN_PTH func_call_param CLOSE_PTH \n')
  def func_call(self, p):
    return 'func_call'
  
  @_('expression multiple_fc_param')
  def func_call_param(self, p):
    return 'func_call_param'
  
  @_('COMMA func_call_param', 'empty')
  def multiple_fc_param(self, p):
    return 'multiple_fc_param'
  
  @_('READ OPEN_PTH variable multiple_vars CLOSE_PTH \n')
  def read(self, p):
    return 'read'
  
  @_('ID array')
  def variable(self, p):
    return p[0]
  
  @_('OPEN_SQR expression CLOSE_SQR matrix', 'empty')
  def array(self, p):
    return 'array'
  
  @_('OPEN_SQR expression CLOSE_SQR', 'empty')
  def matrix(self, p):
    return 'matrix'
  
  @_('COMMA variable', 'empty')
  def multiple_vars(self, p):
    return 'multiple_vars'
  
  @_('WRITE OPEN_PTH expression multiple_expression CLOSE_PTH \n')
  def write(self, p):
    return 'write'
  
  @_('COMMA expression', 'empty')
  def multiple_expression(self, p):
    return 'multiple_expression'
  
  # @_('\n stmnt multiple_con_stmnt')
  # def multiple_con_stmnt(self, p):
  #   print(f'multiple_con_stmnt {p[0]}')
  
  @_('IF expression \n stmnt else_stmnt')
  def if_stmnt(self, p):
    return 'if_stmnt'
  
  @_('\n ELSE \n stmnt END \n', '\n END \n')
  def else_stmnt(self, p):
    return 'else_stmnt'
  
  @_('WHILE expression \n stmnt \n END \n')
  def while_stmnt(self, p):
    return 'while_stmnt'
  
  @_('move_type OPEN_PTH func_call_param CLOSE_PTH')
  def move_func(self, p):
    return 'move_func'
  
  @_('LEFT', 'RIGHT', 'FORWARD', 'CENTER')
  def move_type(self, p):
    return 'move_type'
  
  @_('PEN_UP OPEN_PTH CLOSE_PTH \n', 'PEN_DOWN OPEN_PTH CLOSE_PTH \n')
  def pen_func(self, p):
    return 'pen_func'
  
  @_('MAIN \n stmnt END')
  def main(self, p):
    return 'main'

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