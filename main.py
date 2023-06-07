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

    operandos = []
    operadores = []

    temporal = 0

    # Grammar rules and actions
    @_('DRAWING ID \n declaration')
    def program(self, p):
        for i in self.quadruples:
            print(i)

    @_('var_declaration func_declaration main')
    def declaration(self, p):
        return p[0]

    @_('var_type ID multiple_var \n', 'empty')
    def var_declaration(self, p):
        return p[0]

    @_('COMMA ID multiple_var', 'empty')
    def multiple_var(self, p):
        return p[0]

    @_('NUMBER', 'WORD', 'BOOL')
    def var_type(self, p):
        return p[0]

    @_('func_type FUNC ID OPEN_PTH parameter CLOSE_PTH \n stmnt END \n',
       'empty')
    def func_declaration(self, p):
        print(f'func_declaration {p[0]}')
        return p[0]

    @_('VOID', 'NUMBER', 'WORD', 'BOOL')
    def func_type(self, p):
        print(f'func_type {p[0]}')
        return p[0]

    @_('var_type ID multiple_parameters', 'empty')
    def parameter(self, p):
        print(f'parameter {p[0]}')
        return p[0]

    @_('COMMA parameter', 'empty')
    def multiple_parameters(self, p):
        print(f'multiple_parameters {p[0]}')
        return p[0]

    @_('var_assignation stmnt', 'func_call stmnt', 'read stmnt',
       'write stmnt', 'if_stmnt stmnt', 'while_stmnt stmnt', 'move_func stmnt',
       'pen_func stmnt', 'var_declaration_func stmnt', 'empty')
    def stmnt(self, p):
        #print(f'stmnt {p[0]}')
        return p[0]
      
    @_('var_type ID multiple_vars \n')
    def var_declaration_func(self, p):
        return p[0]

    @_('id e5 assign e6 expression \n')
    def var_assignation(self, p):
        #self.operandos.append(p[-1])
       # print(f'var assign {p[0]}')
        return p[0]

    @_('')
    def e5(self, p):
      self.operandos.append(p[-1])

    @_('')
    def e6(self, p):
      self.operadores.append(p[-1])

    @_('ID')
    def id(self, p):
      return p[0]

    @_('ASSIGN')
    def assign(self, p):
        return p[0]

    @_('variable', 'CTE_NUM', 'CTE_STR', 'cte_bool', 'func_call')
    def var_cte(self, p):
      #print(f'var_cte {p[-1]}')
      #self.operandos.append(p[-1])
      #print(p[0])
      return p[0]

    @_('TRUE', 'FALSE')
    def cte_bool(self, p):
        return p[0]

    @_('exp rel_op e4 exp', 'exp')
    def expression(self, p):
       return p[0]

    #Punto neuralgico para expression
    @_('')
    def e4(self, p):
      self.operadores.append(p[-1])
      print(f'e4 {self.operadores}')
      
    @_('termino term_op e3 termino q2', 'termino')
    def exp(self, p):
        return p[-1]

    #Punto neuralgico para exp
    @_('')
    def e3(self, p):
      self.operadores.append(p[-1])
      print(f'e3 {self.operadores}')

    #quads suma resta
    @_('')
    def q2(self,p):
      madeSum = False
      while len(self.operadores) > 0 and not madeSum:
        op = self.operadores.pop()
        if(op != '='):
          lo = self.operandos.pop()
          ro = self.operandos.pop()
          self.temporal = self.temporal + 1
          self.operandos.append(self.temporal)
        else:
          lo = self.operandos.pop()
          ro = None
          self.temporal = self.operandos.pop()
        print(f'q1 {lo, ro, op, self.temporal}')
        print(f'q1 append temp {self.operandos}')
        myQuad = Quadruple(lo, ro, op, self.temporal)
        self.quadruples.append(myQuad)
        if (op == '+' or op == '-'):
          madeSum = True

    @_('SUM', 'SUB')
    def term_op(self, p):
        return p[0]

    @_('factor fact_op e2 factor q1', 'factor q1')
    def termino(self, p):
        print('no cerooooooo')
        if (len(self.operandos) == 0):
          print('termino')
        return p[-1]

    #quads mult div
    @_('')
    def q1(self,p):
      if(len(self.operadores) > 0):
        op = self.operadores.pop()
        if(op != '='):
          lo = self.operandos.pop()
          ro = self.operandos.pop()
          self.temporal = self.temporal + 1
          self.operandos.append(self.temporal)
          print(f' 169 {self.operandos}')
          return
        else:
          lo = self.operandos.pop()
          ro = None  
          self.temporal = self.operandos.pop()
          print(f' 174 {len(self.operandos)}')  
          
        print(f'q1 {lo, ro, op, self.temporal}')
        print(f'q1 append temp {self.operandos}')
        myQuad = Quadruple(lo, ro, op, self.temporal)
        self.quadruples.append(myQuad)
  

    #Punto neuralgico para terminos
    @_('')
    def e2(self, p):
      print(p[-1])
      self.operadores.append(p[-1])
      print(f'e2 {self.operadores}')

    @_('MULT', 'DIV')
    def fact_op(self, p):
        return p[0]

    @_('open_pth expression close_pth', 'expression', 'var_cte e1')
    def factor(self, p):
        #print(f'factooor {p[0]}')
        return p[-1]

    #Punto neuralgico para todos los operandos
    @_('')
    def e1(self, p):
      if(p[-1] != None):
        self.operandos.append(p[-1])
        print(self.operandos)
      else:
        pass

    @_('OPEN_PTH')
    def open_pth(self, p):
      if(p[0] == '('):
        return None

    @_('CLOSE_PTH')
    def close_pth(self, p):
      if(p[0] == ')'):
        return None

    @_('AND', 'OR')
    def log_op(self, p):
        self.operadores.append(p[0])
        #print(self.operadores)
        return p[0]

    @_('LESS_THAN', 'MORE_THAN', 'DIFFERENT_TO', 'LESS_OR_EQ_THAN',
       'MORE_OR_EQ_THAN', 'EQUAL_TO')
    def rel_op(self, p):
        #print(f'rel_op {p[0]}')
        self.operadores.append(p[0])
        #print(self.operadores)

    @_('ID OPEN_PTH func_call_param CLOSE_PTH \n')
    def func_call(self, p):
        return p[0]

    @_('expression multiple_fc_param')
    def func_call_param(self, p):
        return p[0]

    @_('COMMA func_call_param', 'empty')
    def multiple_fc_param(self, p):
        return p[0]

    @_('READ OPEN_PTH variable multiple_vars CLOSE_PTH \n')
    def read(self, p):
        return p[0]

    @_('ID array')
    def variable(self, p):
        return p[0]

    @_('OPEN_SQR expression CLOSE_SQR matrix', 'empty')
    def array(self, p):
        return p[0]

    @_('OPEN_SQR expression CLOSE_SQR', 'empty')
    def matrix(self, p):
        return p[0]

    @_('COMMA variable', 'empty')
    def multiple_vars(self, p):
        return p[0]

    @_('WRITE OPEN_PTH expression CLOSE_PTH \n')
    def write(self, p):
        return p[0]

    @_('IF con_expression \n stmnt else_stmnt')
    def if_stmnt(self, p):
        return p[0]

    @_('\n ELSE \n stmnt END \n', '\n END \n')
    def else_stmnt(self, p):
        return p[0]

    @_('WHILE con_expression \n stmnt \n END \n')
    def while_stmnt(self, p):
        return p[0]

    @_('expression log_op expression')
    def con_expression(self, p):
        print(f'con_expression {p[0]}')

    @_('move_type OPEN_PTH func_call_param CLOSE_PTH')
    def move_func(self, p):
        print(f'move_func {p[0]}')

    @_('LEFT', 'RIGHT', 'FORWARD', 'CENTER')
    def move_type(self, p):
        print(f'move_type {p[0]}')

    @_('PEN_UP OPEN_PTH CLOSE_PTH \n', 'PEN_DOWN OPEN_PTH CLOSE_PTH \n')
    def pen_func(self, p):
        print(f'pen_func {p[0]}')

    @_('MAIN \n stmnt END')
    def main(self, p):
        print(f'main {p[0]}')

    @_('')
    def empty(self, p):
        pass


# Semantics

if __name__ == '__main__':
    lexer = MikuLexer()
    parser = MikuParser()
    filename = 'test_assign.txt'

    with open(filename) as fp:
        try:
            result = parser.parse(lexer.tokenize(fp.read()))
            print(result)
        except EOFError:
            pass
