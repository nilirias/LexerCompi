from sly import Parser
from sly.yacc import _decorator as _
from miku_lexer import MikuLexer
from miku_quadruple import Quadruple
from miku_funcdir import *
from miku_vardir import *
from miku_semanticcube import checkOperator
import re

class MikuParser(Parser):
    debugfile = 'parser.out'
    tokens = MikuLexer.tokens
    start = 'program'
    id = ''
    varidd = ''
    funcid = ''
    functype = ''
    vartype = ''
    operador = ''
    
    funcdir = FuncDir()
    vardir = VarDir()

    quadruples = []
    quadcount = 1

    lotype = ''
    rotype = ''

    tipotemp = ''

    myQuad = Quadruple(0, 0, 0, 0)
    conQuad = Quadruple(0, 0, 0, 0) 
    paramaQuad = Quadruple(0,0,0,0)

    operandos = []
    operadores = []
    returnquad = []
    jump = []

    temporal = 0
    paramCont = 0
    pcont = 0
    dir = 0

    numglb = 0
    wordglb = 500
    boolglb = 1000

    numlcl = 1500
    wordlcl = 2000
    boollcl = 2500

    numtemp = 3000
    wordtemp = 3500
    booltemp = 4000

    numcte = 4500
    wordcte = 5000
    boolcte = 5500

    # Grammar rules and actions
    @_('DRAWING ID fd1 \n declaration')
    def program(self, p):
        for i in self.quadruples:
            print(i)
        # print('# function directory #')
        print(self.funcdir)
        # print('# var directory #')
        # print(self.vardir)

        return (self.funcid, self.quadruples)

    @_('var_declaration vd1 func_declaration main')
    def declaration(self, p):
        return p[0]

    @_('var_type addvartype ID varglobal multiple_var \n var_declaration', 'empty')
    def var_declaration(self, p):
        return p[0]

    @_('')
    def varglobal(self, p):
      if (self.vartype == 'number'):
        self.dir = self.numglb
        self.numglb = self.numglb + 1
        
      if (self.vartype == 'word'):
        self.dir = self.wordglb
        self.wordglb = self.wordglb + 1.
        
      if (self.vartype == 'bool'):
        self.dir = self.boolglb
        self.boolglb = self.boolglb + 1

      self.vardir.add_var(p[-1], self.dir)
      
    @_('')
    def addvartype(self, p):
      self.vartype = p[-1]

    @_('COMMA ID varglobal multiple_var', 'empty')
    def multiple_var(self, p):
        return p[0]

    @_('NUMBER', 'WORD', 'BOOL')
    def var_type(self, p):
        return p[0]

    @_('FUNC resetvars func_type ID fd1 OPEN_PTH parameter CLOSE_PTH \n stmnt vd1 END \n func_declaration',
       'empty')
    def func_declaration(self, p):
        return p[-1]

    @_('')
    def resetvars(self, p):
      self.numlcl = 1500
      self.wordlcl = 2000
      self.boollcl = 2500

    @_('')
    def resettemp(self, p):
      self.numtemp = 3000
      self.wordtemp = 3500
      self.booltemp = 4000
      
    # function id
    @_('')
    def fd1(self, p):
      self.funcid = p[-1]

    @_('')
    def vd1(self, p):
        self.funcdir.add_func(self.funcid, self.functype, 'varc', self.pcont, 'vart', self.vardir)
        self.vardir = VarDir()
        return p[-1]
  
    @_('VOID', 'NUMBER', 'WORD', 'BOOL')
    def func_type(self, p):
        self.functype = p[-1]
        #return p[0]

    @_('var_type addvartype ID varid multiple_parameters', 'empty')
    def parameter(self, p):
        self.pcont = self.pcont + 1
        return p[0]

    @_('COMMA parameter', 'empty')
    def multiple_parameters(self, p):
        return p[0]

    @_('var_assignation stmnt', 'func_call stmnt', 'read stmnt', 'write stmnt',
       'if_stmnt stmnt', 'while_stmnt stmnt', 'move_func stmnt',
       'pen_func stmnt', 'var_declaration_func stmnt', 'returnf stmnt', 'empty')
    def stmnt(self, p):
        return p[0]

    @_('RETURN expression')
    def returnf(self, p):
      return p[0]

    @_('var_type addvartype ID varid multiple_vars \n')
    def var_declaration_func(self, p):
        return p[0]
      
    @_('')
    def varid(self, p):
      if (self.vartype == 'number'):
        self.dir = self.numlcl
        self.numlcl = self.numlcl + 1
        #print(p[-1], self.numlcl)
        
      if (self.vartype == 'word'):
        self.dir = self.wordlcl
        self.wordlcl = self.wordlcl + 1
        #print(p[-1], self.wordlcl)
        
      if (self.vartype == 'bool'):
        self.dir = self.boollcl
        self.boollcl = self.boollcl + 1
        #print(p[-1], self.boollcl)
      self.vardir.add_var(p[-1], self.dir)

    @_('ID e5 assign e6 expression q3 \n')
    def var_assignation(self, p):
        return p[0]

    @_('')
    def e5(self, p):
        self.operandos.append(p[-1])

    @_('')
    def e6(self, p):
        self.operadores.append(p[-1])

    @_('ASSIGN')
    def assign(self, p):
        return p[0]

    @_('variable', 'CTE_NUM nvarcte', 'CTE_STR svarcte', 'cte_bool bvarcte', 'func_call')
    def var_cte(self, p):
        return p[0]

    @_('')
    def nvarcte(self, p):
      self.dir = self.numcte
      self.numcte = self.numcte + 1
      self.vardir.add_var(p[-1], self.dir)

    @_('')
    def svarcte(self, p):
      self.dir = self.wordcte
      self.wordcte = self.wordcte + 1
      self.vardir.add_var(p[-1], self.dir)

    @_('')
    def bvarcte(self, p):
      self.dir = self.boolcte
      self.boolcte = self.boolcte + 1
      self.vardir.add_var(p[-1], self.dir)

    @_('TRUE', 'FALSE')
    def cte_bool(self, p):
        return p[0]

    @_('exp rel_op exp q4', 'exp q4', 'func_call q4')
    def expression(self, p):
        return p[-1]

    @_('')
    def q4(self, p):
        while len(self.operadores) > 0:
            op = self.operadores.pop()
            if (op == '>' or op == '<' or op == '<=' or op == '>='
                    or op == '==' or op == '<>'):
                lo = self.operandos.pop()
                ro = self.operandos.pop()
                self.temporal = self.temporal + 1
                self.operandos.append(self.temporal)
                #print(f'239 {lo}')
                if((self.vardir.get_var_address(lo) >= 1500 and self.vardir.get_var_address(lo) < 2000) or (self.vardir.get_var_address(lo) >= 3000 and self.vardir.get_var_address(lo) < 3500) or (self.vardir.get_var_address(lo) >= 4500 and self.vardir.get_var_address(lo) < 5000)): 
                  self.lotype = 'number'

                if((self.vardir.get_var_address(lo) >= 500 and self.vardir.get_var_address(lo) < 999) or (self.vardir.get_var_address(lo) >= 2000 and self.vardir.get_var_address(lo) < 2500) or (self.vardir.get_var_address(lo) >= 3500 and self.vardir.get_var_address(lo) < 4000) or (self.vardir.get_var_address(lo) >= 5000 and self.vardir.get_var_address(lo) < 5500)):
                  self.lotype = 'word'

                if((self.vardir.get_var_address(lo) >= 1000 and self.vardir.get_var_address(lo) < 1500) or (self.vardir.get_var_address(lo) >= 2500 and self.vardir.get_var_address(lo) < 3000) or (self.vardir.get_var_address(lo) >= 4000 and self.vardir.get_var_address(lo) < 4500) or (self.vardir.get_var_address(lo) >= 5500 and self.vardir.get_var_address(lo) < 6000)):
                  self.lotype = 'bool'
                  
                if((self.vardir.get_var_address(ro) >= 1500 and self.vardir.get_var_address(ro) < 2000) or 
 (self.vardir.get_var_address(ro) >= 3000 and self.vardir.get_var_address(ro) < 3500) or (self.vardir.get_var_address(ro) >= 4500 and self.vardir.get_var_address(ro) < 5000)): 
                  self.rotype = 'number'

                if((self.vardir.get_var_address(ro) >= 500 and self.vardir.get_var_address(ro) < 1000) or (self.vardir.get_var_address(ro) >= 2000 and self.vardir.get_var_address(ro) < 2500) or (self.vardir.get_var_address(ro) >= 3500 and self.vardir.get_var_address(ro) < 4000) or (self.vardir.get_var_address(ro) >= 5000 and self.vardir.get_var_address(ro) < 5500)):
                  self.rotype = 'word'

                if((self.vardir.get_var_address(ro) >= 1000 and self.vardir.get_var_address(ro) < 1500) or (self.vardir.get_var_address(ro) >= 2500 and self.vardir.get_var_address(ro) < 3000) or (self.vardir.get_var_address(ro) >= 4000 and self.vardir.get_var_address(ro) < 4500) or (self.vardir.get_var_address(ro) >= 5500 and self.vardir.get_var_address(ro) < 6000)):
                  self.rotype = 'bool'
                  
                #print(self.rotype, self.lotype, op)
                tipotemp = checkOperator(self.rotype, self.lotype, op)
                if(tipotemp == 'number'):
                  myQuad = Quadruple(lo, ro, op, self.numtemp)
                  self.numtemp = self.numtemp + 1
                elif(tipotemp == 'word'):
                  myQuad = Quadruple(lo, ro, op, self.wordtemp)
                  self.wordtemp = self.wordtemp + 1
                elif(tipotemp == 'bool'):
                  myQuad = Quadruple(lo, ro, op, self.booltemp)
                  self.booltemp = self.booltemp + 1

                #print(f'272 {self.quadruples}')
                self.quadruples.append(myQuad)
                self.quadcount = self.quadcount + 1
            else:
                self.operadores.append(op)
                return

    @_('termino term_op e3 termino q1', 'termino q1')
    def exp(self, p):
        return p[-1]

    #Punto neuralgico para exp
    @_('')
    def e3(self, p):
        self.operadores.append(p[-1])

    #quads suma resta
    @_('')
    def q2(self, p):
        while len(self.operadores) > 0:
            op = self.operadores.pop()
            if (op == '*' or op == '/'):
                lo = self.operandos.pop()
                ro = self.operandos.pop()
                self.temporal = self.temporal + 1
                self.operandos.append(self.temporal)
                #print(f'296 {lo}')
                if((self.vardir.get_var_address(lo) >= 1500 and self.vardir.get_var_address(lo) < 2000) or (self.vardir.get_var_address(lo) >= 3000 and self.vardir.get_var_address(lo) < 3500) or (self.vardir.get_var_address(lo) >= 4500 and self.vardir.get_var_address(lo) < 5000)): 
                  self.lotype = 'number'

                if((self.vardir.get_var_address(lo) >= 500 and self.vardir.get_var_address(lo) < 999) or (self.vardir.get_var_address(lo) >= 2000 and self.vardir.get_var_address(lo) < 2500) or (self.vardir.get_var_address(lo) >= 3500 and self.vardir.get_var_address(lo) < 4000) or (self.vardir.get_var_address(lo) >= 5000 and self.vardir.get_var_address(lo) < 5500)):
                  self.lotype = 'word'

                if((self.vardir.get_var_address(lo) >= 1000 and self.vardir.get_var_address(lo) < 1500) or (self.vardir.get_var_address(lo) >= 2500 and self.vardir.get_var_address(lo) < 3000) or (self.vardir.get_var_address(lo) >= 4000 and self.vardir.get_var_address(lo) < 4500) or (self.vardir.get_var_address(lo) >= 5500 and self.vardir.get_var_address(lo) < 6000)):
                  self.lotype = 'bool'
                  
                if((self.vardir.get_var_address(ro) >= 1500 and self.vardir.get_var_address(ro) < 2000) or 
 (self.vardir.get_var_address(ro) >= 3000 and self.vardir.get_var_address(ro) < 3500) or (self.vardir.get_var_address(ro) >= 4500 and self.vardir.get_var_address(ro) < 5000)): 
                  self.rotype = 'number'

                if((self.vardir.get_var_address(ro) >= 500 and self.vardir.get_var_address(ro) < 1000) or (self.vardir.get_var_address(ro) >= 2000 and self.vardir.get_var_address(ro) < 2500) or (self.vardir.get_var_address(ro) >= 3500 and self.vardir.get_var_address(ro) < 4000) or (self.vardir.get_var_address(ro) >= 5000 and self.vardir.get_var_address(ro) < 5500)):
                  self.rotype = 'word'

                if((self.vardir.get_var_address(ro) >= 1000 and self.vardir.get_var_address(ro) < 1500) or (self.vardir.get_var_address(ro) >= 2500 and self.vardir.get_var_address(ro) < 3000) or (self.vardir.get_var_address(ro) >= 4000 and self.vardir.get_var_address(ro) < 4500) or (self.vardir.get_var_address(ro) >= 5500 and self.vardir.get_var_address(ro) < 6000)):
                  self.rotype = 'bool'
                  
                #print(self.rotype, self.lotype, op)
                tipotemp = checkOperator(self.rotype, self.lotype, op)
                if(tipotemp == 'number'):
                  myQuad = Quadruple(lo, ro, op, self.numtemp)
                  self.numtemp = self.numtemp + 1
                elif(tipotemp == 'word'):
                  myQuad = Quadruple(lo, ro, op, self.wordtemp)
                  self.wordtemp = self.wordtemp + 1
                elif(tipotemp == 'bool'):
                  myQuad = Quadruple(lo, ro, op, self.booltemp)
                  self.booltemp = self.booltemp + 1
                
                #print(f'330 {self.quadruples}')
                self.quadruples.append(myQuad)
                self.quadcount = self.quadcount + 1
            else:
                self.operadores.append(op)
                return

    @_('SUM', 'SUB')
    def term_op(self, p):
        return p[-1]

    @_('factor fact_op e2 factor q2', 'factor q2')
    def termino(self, p):
        return p[-1]

#quads mult div
    @_('')
    def q1(self, p):
        if (len(self.operadores) > 0):
            op = self.operadores.pop()
            if (op == '+' or op == '-'):
                lo = self.operandos.pop()
                ro = self.operandos.pop()
                self.temporal = self.temporal + 1
                self.operandos.append(self.temporal)
                # print(f'sumas {lo} {ro}')
                # print(self.vardir.get_var_address(lo))
                if((self.vardir.get_var_address(lo) >= 1500 and self.vardir.get_var_address(lo) < 2000) or (self.vardir.get_var_address(lo) >= 3000 and self.vardir.get_var_address(lo) < 3500) or (self.vardir.get_var_address(lo) >= 4500 and self.vardir.get_var_address(lo) < 5000)): 
                  self.lotype = 'number'

                if((self.vardir.get_var_address(lo) >= 500 and self.vardir.get_var_address(lo) < 999) or (self.vardir.get_var_address(lo) >= 2000 and self.vardir.get_var_address(lo) < 2500) or (self.vardir.get_var_address(lo) >= 3500 and self.vardir.get_var_address(lo) < 4000) or (self.vardir.get_var_address(lo) >= 5000 and self.vardir.get_var_address(lo) < 5500)):
                  self.lotype = 'word'

                if((self.vardir.get_var_address(lo) >= 1000 and self.vardir.get_var_address(lo) < 1500) or (self.vardir.get_var_address(lo) >= 2500 and self.vardir.get_var_address(lo) < 3000) or (self.vardir.get_var_address(lo) >= 4000 and self.vardir.get_var_address(lo) < 4500) or (self.vardir.get_var_address(lo) >= 5500 and self.vardir.get_var_address(lo) < 6000)):
                  self.lotype = 'bool'
                  
                if((self.vardir.get_var_address(ro) >= 1500 and self.vardir.get_var_address(ro) < 2000) or 
 (self.vardir.get_var_address(ro) >= 3000 and self.vardir.get_var_address(ro) < 3500) or (self.vardir.get_var_address(ro) >= 4500 and self.vardir.get_var_address(ro) < 5000)): 
                  self.rotype = 'number'

                if((self.vardir.get_var_address(ro) >= 500 and self.vardir.get_var_address(ro) < 1000) or (self.vardir.get_var_address(ro) >= 2000 and self.vardir.get_var_address(ro) < 2500) or (self.vardir.get_var_address(ro) >= 3500 and self.vardir.get_var_address(ro) < 4000) or (self.vardir.get_var_address(ro) >= 5000 and self.vardir.get_var_address(ro) < 5500)):
                  self.rotype = 'word'

                if((self.vardir.get_var_address(ro) >= 1000 and self.vardir.get_var_address(ro) < 1500) or (self.vardir.get_var_address(ro) >= 2500 and self.vardir.get_var_address(ro) < 3000) or (self.vardir.get_var_address(ro) >= 4000 and self.vardir.get_var_address(ro) < 4500) or (self.vardir.get_var_address(ro) >= 5500 and self.vardir.get_var_address(ro) < 6000)):
                  self.rotype = 'bool'

                #print(self.lotype, self.rotype)
                tipotemp = checkOperator(self.rotype, self.lotype, op)
                if(tipotemp == 'number'):
                  self.myQuad = Quadruple(lo, ro, op, self.numtemp)
                  self.numtemp = self.numtemp + 1
                elif(tipotemp == 'word'):
                  self.myQuad = Quadruple(lo, ro, op, self.wordtemp)
                  self.wordtemp = self.wordtemp + 1
                elif(tipotemp == 'bool'):
                  self.myQuad = Quadruple(lo, ro, op, self.booltemp)
                  self.booltemp = self.booltemp + 1

                #print(f'386 {self.myQuad}')
                self.quadruples.append(self.myQuad)
                self.quadcount = self.quadcount + 1
            else:
                self.operadores.append(op)

    @_('')
    def q3(self, p):
        if (len(self.operadores) > 0):
            op = self.operadores.pop()
            if (op == '='):
                lo = self.operandos.pop()
                ro = None
                temp = self.operandos.pop() 
                myQuad = Quadruple(lo, ro, op, (self.vardir.get_var_address(temp)))
                self.quadruples.append(myQuad)
                self.quadcount = self.quadcount + 1
            else:
                self.operadores.append(op)

    #Punto neuralgico para terminos
    @_('')
    def e2(self, p):
        self.operadores.append(p[-1])

    @_('MULT', 'DIV')
    def fact_op(self, p):
        return p[0]

    @_('open_pth expression close_pth', 'var_cte e1', 'expression')
    def factor(self, p):
        return p[-1]

    #Punto neuralgico para todos los operandos
    @_('')
    def e1(self, p):
        if (p[-1] != None):
            self.operandos.append(p[-1])
        else:
            pass

    @_('OPEN_PTH')
    def open_pth(self, p):
        if (p[0] == '('):
            self.operadores.append('(')
            return None

    @_('CLOSE_PTH')
    def close_pth(self, p):
        if (p[0] == ')'):
            (f'closepath {self.operadores.pop()}')
            return None

    @_('AND', 'OR')
    def log_op(self, p):
        return p[0]

    @_('LESS_THAN', 'MORE_THAN', 'DIFFERENT_TO', 'LESS_OR_EQ_THAN',
       'MORE_OR_EQ_THAN', 'EQUAL_TO')
    def rel_op(self, p):
        self.operadores.append(p[-1])

    @_('ID OPEN_PTH func1 func_call_param CLOSE_PTH func3 \n')
    def func_call(self, p):
        self.id = p.ID
        return p[0]

    @_('')
    def func1(self, p):
      self.myQuad = Quadruple(self.id, None, 'ERA', None)
      self.quadruples.append(self.myQuad)
      self.quadcount = self.quadcount + 1

    @_('expression func2 multiple_fc_param')
    def func_call_param(self, p):
        return p[0]

    @_('')
    def func2(self, p):
      self.paramCont = self.paramCont + 1
      self.paramQuad = Quadruple(self.operandos.pop(), None, 'PARAM', self.paramCont)
      self.quadruples.append(self.paramQuad)
      self.quadcount = self.quadcount + 1

    @_('')
    def func3(self, p):
      self.myQuad = Quadruple(self.id, None, 'GOSUB', None)
      self.quadruples.append(self.myQuad)
      self.quadcount = self.quadcount + 1

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

    @_('COMMA variable varid multiple_vars', 'empty')
    def multiple_vars(self, p):
        return p[0]

    @_('WRITE OPEN_PTH expression CLOSE_PTH \n')
    def write(self, p):
        return p[0]

    @_('IF con_expression if1 \n stmnt if2 else_stmnt')
    def if_stmnt(self, p):
        return p[0]
      
    @_('')
    def if1(self, p):
      self.conQuad = Quadruple(None, None, 'gotof', None)
      self.returnquad.append(len(self.quadruples))
      self.quadruples.append(self.conQuad)
      
    @_('')
    def if2(self, p):
      self.jump.append(self.quadcount-1)
      self.operandos.append(self.temporal)
      self.conQuad = Quadruple(self.operandos.pop(), None, 'gotof', self.jump.pop())
      idx = self.returnquad.pop()
      self.quadruples[idx] = self.conQuad

    @_('\n ELSE if3 \n stmnt if4 END \n', '\n END \n')
    def else_stmnt(self, p):
        return p[0]

    @_('')
    def if3(self, p):
        self.conQuad = Quadruple(None, None, 'gotov', None)
        self.returnquad.append(len(self.quadruples))
        self.quadruples.append(self.conQuad)
      
    @_('')
    def if4(self, p):
      self.jump.append(self.quadcount-1)
      self.operandos.append(self.temporal)
      self.conQuad = Quadruple(self.operandos.pop(), None, 'gotov', self.jump.pop())
      idx = self.returnquad.pop()
      self.quadruples[idx] = self.conQuad
  
    @_('WHILE w1 con_expression w2 \n stmnt \n w3 END \n')
    def while_stmnt(self, p):
        return p[0]

    @_('')
    def w1(self, p):
      self.jump.append(self.quadcount)

    @_('')
    def w2(self, p):
      self.myQuad = Quadruple(self.operandos.pop(), None, 'gotof', None) 
      self.returnquad.append(len(self.quadruples))
      self.quadruples.append(self.myQuad)
      self.jump.append(self.quadcount-1)

    @_('')
    def w3(self, p):
      self.jump.append(self.quadcount-1)
      self.operandos.append(self.temporal)
      self.conQuad = Quadruple(self.operandos.pop(), None, 'gotof', self.jump.pop())
      idx = self.returnquad.pop()
      self.quadruples[idx] = self.conQuad
      self.conQuad = Quadruple(None, None, 'gotot', self.jump.pop())
      self.quadruples.append(self.conQuad)
  
    @_('expression q5 log_op e7 expression q5', 'expression q5')
    def con_expression(self, p):
        return p[-1]

    @_('')
    def e7(self, p):
        self.operadores.append(p[-1])

    @_('')
    def q5(self, p):
        while len(self.operadores) > 0:
            op = self.operadores.pop()
            if (op.lower() == 'and' or op.lower() == 'or'):
                lo = self.operandos.pop()
                ro = self.operandos.pop()
                self.temporal = self.temporal + 1
                self.operandos.append(self.temporal)
                if((self.vardir.get_var_address(lo) >= 1500 and self.vardir.get_var_address(lo) < 2000) or (self.vardir.get_var_address(lo) >= 3000 and self.vardir.get_var_address(lo) < 3500) or (self.vardir.get_var_address(lo) >= 4500 and self.vardir.get_var_address(lo) < 5000)): 
                  self.lotype = 'number'

                if((self.vardir.get_var_address(lo) >= 500 and self.vardir.get_var_address(lo) < 999) or (self.vardir.get_var_address(lo) >= 2000 and self.vardir.get_var_address(lo) < 2500) or (self.vardir.get_var_address(lo) >= 3500 and self.vardir.get_var_address(lo) < 4000) or (self.vardir.get_var_address(lo) >= 5000 and self.vardir.get_var_address(lo) < 5500)):
                  self.lotype = 'word'

                if((self.vardir.get_var_address(lo) >= 1000 and self.vardir.get_var_address(lo) < 1500) or (self.vardir.get_var_address(lo) >= 2500 and self.vardir.get_var_address(lo) < 3000) or (self.vardir.get_var_address(lo) >= 4000 and self.vardir.get_var_address(lo) < 4500) or (self.vardir.get_var_address(lo) >= 5500 and self.vardir.get_var_address(lo) < 6000)):
                  self.lotype = 'bool'
                  
                if((self.vardir.get_var_address(ro) >= 1500 and self.vardir.get_var_address(ro) < 2000) or 
 (self.vardir.get_var_address(ro) >= 3000 and self.vardir.get_var_address(ro) < 3500) or (self.vardir.get_var_address(ro) >= 4500 and self.vardir.get_var_address(ro) < 5000)): 
                  self.rotype = 'number'

                if((self.vardir.get_var_address(ro) >= 500 and self.vardir.get_var_address(ro) < 1000) or (self.vardir.get_var_address(ro) >= 2000 and self.vardir.get_var_address(ro) < 2500) or (self.vardir.get_var_address(ro) >= 3500 and self.vardir.get_var_address(ro) < 4000) or (self.vardir.get_var_address(ro) >= 5000 and self.vardir.get_var_address(ro) < 5500)):
                  self.rotype = 'word'

                if((self.vardir.get_var_address(ro) >= 1000 and self.vardir.get_var_address(ro) < 1500) or (self.vardir.get_var_address(ro) >= 2500 and self.vardir.get_var_address(ro) < 3000) or (self.vardir.get_var_address(ro) >= 4000 and self.vardir.get_var_address(ro) < 4500) or (self.vardir.get_var_address(ro) >= 5500 and self.vardir.get_var_address(ro) < 6000)):
                  self.rotype = 'bool'
                  
                #print(self.rotype, self.lotype, op)
                tipotemp = checkOperator(self.rotype, self.lotype, op)
                if(tipotemp == 'number'):
                  myQuad = Quadruple(lo, ro, op, self.numtemp)
                  self.numtemp = self.numtemp + 1
                elif(tipotemp == 'word'):
                  myQuad = Quadruple(lo, ro, op, self.wordtemp)
                  self.wordtemp = self.wordtemp + 1
                elif(tipotemp == 'bool'):
                  self.booltemp = self.booltemp + 1
                #print(self.quadruples)
                self.quadruples.append(myQuad)
                self.quadcount = self.quadcount + 1
              
            else:
                self.operadores.append(op)
                return

    @_('move_type OPEN_PTH func_call_param CLOSE_PTH')
    def move_func(self, p):
        return p[0]

    @_('LEFT', 'RIGHT', 'FORWARD', 'CENTER')
    def move_type(self, p):
        return p[0]

    @_('PEN_UP OPEN_PTH CLOSE_PTH \n', 'PEN_DOWN OPEN_PTH CLOSE_PTH \n')
    def pen_func(self, p):
        return p[0]
      
    @_('MAIN fd1 resetvars \n stmnt vd1 END')
    def main(self, p):
        return p[0]

    @_('')
    def empty(self, p):
        pass


# if __name__ == '__main__':
#     lexer = MikuLexer()
#     parser = MikuParser()
#     filename = 'test_assign.txt'

#     with open(filename) as fp:
#         try:
#             result = parser.parse(lexer.tokenize(fp.read()))
#         except EOFError:
#             pass
