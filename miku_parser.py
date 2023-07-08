from sly import Parser
from sly.yacc import _decorator as _
from miku_lexer import MikuLexer
from miku_quadruple import Quadruple
from miku_funcdir import *
from miku_vardir import *
from miku_cte import *
from miku_semanticcube import checkOperator


def checkVarType(varDir):
    if ((varDir >= 1500 and varDir < 2000)
            or (varDir >= 3000 and varDir < 3500)
            or (varDir >= 4500 and varDir < 5000)):
        return 'number'

    if ((varDir >= 500 and varDir < 999) or (varDir >= 2000 and varDir < 2500)
            or (varDir >= 3500 and varDir < 4000)
            or (varDir >= 5000 and varDir < 5500)):
        return 'word'

    if ((varDir >= 1000 and varDir < 1500)
            or (varDir >= 2500 and varDir < 3000)
            or (varDir >= 4000 and varDir < 4500)
            or (varDir >= 5500 and varDir < 6000)):
        return 'bool'


def generateOpCuadruple(self, op):
    ro = self.operandos.pop()
    lo = self.operandos.pop()
    self.temporal = self.temporal + 1
    temporal = f't{self.temporal}'
    self.operandos.append(temporal)
    self.ctedir.add_cte(temporal, self.dir)

    loDir = self.vardir.get_var_address(lo)
    roDir = self.vardir.get_var_address(ro)

    lotype = checkVarType(loDir)
    rotype = checkVarType(roDir)

    tipotemp = checkOperator(rotype, lotype, op)
    if (tipotemp == 'number'):
        tempDir = self.numtemp
        self.vart[0] += 1
        self.numtemp = self.numtemp + 1
    elif (tipotemp == 'word'):
        tempDir = self.wordtemp
        self.vart[1] += 1
        self.wordtemp = self.wordtemp + 1
    elif (tipotemp == 'bool'):
        tempDir = self.booltemp
        self.vart[2] += 1
        self.booltemp = self.booltemp + 1

    if (tempDir >= 3000 and tempDir <= 4499):
        self.vardir.add_var(temporal, tempDir, 'temp')
    elif (tempDir >= 4500 and tempDir <= 5999):
        self.vardir.add_var(temporal, tempDir, 'cte')
    else:
        self.vardir.add_var(temporal, tempDir, 'var')

    # print(f'generateOpCuadruple: {lo} {op} {ro} : {temporal}')
    # print(f'generateOpCuadruple: {loDir} {op} {roDir} : {tempDir}')

    myQuad = Quadruple(loDir, roDir, op, tempDir)

    self.quadruples.append(myQuad)
    self.quadcount = self.quadcount + 1
    # print(f'| generateOpCuadruple {self.quadcount} |')


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

    funcjump = 0
    funcparamcont = 0
    funcquaddir = 0
    maindir = ''
    gotofdir = 0

    funcdir = FuncDir()
    vardir = VarDir()
    ctedir = CteDir()

    quadruples = []
    quadcount = 1

    tipotemp = ''

    myQuad = Quadruple(0, 0, 0, 0)
    conQuad = Quadruple(0, 0, 0, 0)
    paramaQuad = Quadruple(0, 0, 0, 0)

    operandos = []
    operadores = []
    returnquad = []
    jump = []
    funcdireccion = []

    temporal = 0
    paramCont = 0
    pcont = 0
    dir = 0

    contnum = 0
    contword = 0
    contbool = 0
    varc = []

    vart = [0, 0, 0]

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
        self.myQuad = Quadruple(None, None, 'GOTO', 1)
        self.quadruples.insert(0, self.myQuad)
        self.quadcount = self.quadcount + 1
        # print(f'| program {self.quadcount} |')
        # print('==========================')
        # print('- cuadruplos')
        # for i in self.quadruples:
        #     print(i)
        # print('- funcdir')
        # print(self.funcdir)
        # print('==========================')
        # print('- ctes')
        # print(self.ctedir)
        return (p.ID, self.quadruples, self.funcdir, self.ctedir)

    @_('var_declaration func_declaration main')
    def declaration(self, p):
        return p[0]

    @_('var_type addvartype ID varglobal multiple_var vd1 \n var_declaration',
       'empty')
    def var_declaration(self, p):
        return p[0]

    @_('')
    def varglobal(self, p):
        if (self.vartype == 'number'):
            self.dir = self.numglb
            self.numglb = self.numglb + 1

        if (self.vartype == 'word'):
            self.dir = self.wordglb
            self.wordglb = self.wordglb + 1

        if (self.vartype == 'bool'):
            self.dir = self.boolglb
            self.boolglb = self.boolglb + 1

        self.vardir.add_var(p[-1], self.dir)
        self.ctedir.add_cte(p[-1], self.dir)

    @_('')
    def addvartype(self, p):
        self.vartype = p[-1]

    @_('COMMA ID varglobal multiple_var', 'empty')
    def multiple_var(self, p):
        return p[0]

    @_('NUMBER', 'WORD', 'BOOL')
    def var_type(self, p):
        return p[0]

    @_(
        'FUNC resetvars func_type ftr ID fd1 OPEN_PTH parameter eracont CLOSE_PTH \n stmnt vd1 resettemp resetvarc END \n func_declaration',
        'empty')
    def func_declaration(self, p):
        return p[-1]

    @_('')
    def eracont(self, p):
        self.funcparamcont = self.funcparamcont + 1

    @_('')
    def resetvarc(self, p):
        self.funcdireccion.append(self.quadcount)
        self.contnum = 0
        self.contword = 0
        self.contbool = 0
        self.varc = [self.contnum, self.contword, self.contbool]

    @_('')
    def resetvars(self, p):
        self.numlcl = 1500
        self.wordlcl = 2000
        self.boollcl = 2500

    @_('')
    def resettemp(self, p):
        self.funcjump = 0
        self.numtemp = 3000
        self.wordtemp = 3500
        self.booltemp = 4000

    # function id
    @_('')
    def fd1(self, p):
        self.funcid = p[-1]

    @_('')
    def vd1(self, p):
        self.funcdir.add_func(self.funcid, self.functype, self.varc,
                              self.pcont, self.vart, self.quadcount - 1,
                              self.vardir)
        self.vardir = VarDir()
        return p[-1]

    @_('VOID', 'NUMBER', 'WORD', 'BOOL')
    def func_type(self, p):
        return p[-1]

    @_('')
    def ftr(self, p):
        if (p[-1] == 'void'):
            self.functype = 1
        elif (p[-1] == 'number'):
            self.functype = 2
        elif (p[-1] == 'word'):
            self.functype = 3
        elif (p[-1] == 'bool'):
            self.functype = 4
        elif (p[-1] == None):
            self.functype = 0
        return p[-1]

    @_('var_type addvartype ID varid multiple_parameters', 'empty')
    def parameter(self, p):
        self.pcont = self.pcont + 1
        return p[0]

    @_('COMMA parameter', 'empty')
    def multiple_parameters(self, p):
        return p[0]

    @_('var_assignation stmnt', 'var_declaration_func stmnt',
       'func_call stmnt', 'read stmnt', 'write stmnt', 'if_stmnt stmnt',
       'while_stmnt stmnt', 'move_func stmnt', 'pen_func stmnt',
       'returnf stmnt', 'empty')
    def stmnt(self, p):
        # self.quadcount = self.quadcount + 1
        # self.jump.append(self.quadcount)
        # print(f'| stmnt {self.jump} - {self.quadcount} |')
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
            self.contnum = self.contnum + 1
            self.varc = [self.contnum, self.contword, self.contbool]

        if (self.vartype == 'word'):
            self.dir = self.wordlcl
            self.wordlcl = self.wordlcl + 1
            self.contword = self.contword + 1
            self.varc = [self.contnum, self.contword, self.contbool]

        if (self.vartype == 'bool'):
            self.dir = self.boollcl
            self.boollcl = self.boollcl + 1
            self.contbool = self.contbool + 1
            self.varc = [self.contnum, self.contword, self.contbool]

        if (self.dir >= 3000 and self.dir <= 4499):
            self.vardir.add_var(p[-1], self.dir, 'temp')
        elif (self.dir >= 4500 and self.dir <= 5999):
            self.vardir.add_var(p[-1], self.dir, 'cte')
        else:
            self.vardir.add_var(p[-1], self.dir, 'var')
        self.ctedir.add_cte(p[-1], self.dir)

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

    @_('variable getvardir', 'CTE_NUM nvarcte', 'CTE_STR svarcte',
       'cte_bool bvarcte', 'func_call')
    def var_cte(self, p):
        # print(f'------- var_cte {p[1]}')
        return p[1]

    @_('')
    def getvardir(self, p):
        return p[-1]

    @_('')
    def nvarcte(self, p):
        if (not self.vardir.check_if_var_exists(p[-1])):
            self.dir = self.numcte
            self.numcte = self.numcte + 1
            if (self.dir >= 3000 and self.dir <= 4499):
                self.vardir.add_var(p[-1], self.dir, 'temp')
            elif (self.dir >= 4500 and self.dir <= 5999):
                self.vardir.add_var(p[-1], self.dir, 'cte')
            else:
                self.vardir.add_var(p[-1], self.dir, 'var')
            self.ctedir.add_cte(p[-1], self.dir)

        return p[-1]
        # return self.vardir

    @_('')
    def svarcte(self, p):
        if (not self.vardir.check_if_var_exists(p[-1])):
            self.dir = self.wordcte
            self.wordcte = self.wordcte + 1
            if (self.dir >= 3000 and self.dir <= 4499):
                self.vardir.add_var(p[-1], self.dir, 'temp')
            elif (self.dir >= 4500 and self.dir <= 5999):
                self.vardir.add_var(p[-1], self.dir, 'cte')
            else:
                self.vardir.add_var(p[-1], self.dir, 'var')
            self.ctedir.add_cte(p[-1], self.dir)
        return p[-1]
        # return self.vardir

    @_('')
    def bvarcte(self, p):
        self.dir = self.boolcte
        self.boolcte = self.boolcte + 1
        if (self.dir >= 3000 and self.dir <= 4499):
            self.vardir.add_var(p[-1], self.dir, 'temp')
        elif (self.dir >= 4500 and self.dir <= 5999):
            self.vardir.add_var(p[-1], self.dir, 'cte')
        else:
            self.vardir.add_var(p[-1], self.dir, 'var')
        self.ctedir.add_cte(p[-1], self.dir)
        return p[-1]
        # return self.vardir

    @_('TRUE', 'FALSE')
    def cte_bool(self, p):
        return p[0]

    @_('func_call q4 empty', 'expression rel_op exp q4 empty', 'exp q4 empty')
    def expression(self, p):
        # print('--- expression')
        return p[0]

    @_('')
    def q4(self, p):
        # print(f'---- q4 {self.operadores}')
        while len(self.operadores) > 0:
            op = self.operadores.pop()
            if (op == '>' or op == '<' or op == '<=' or op == '>='
                    or op == '==' or op == '<>'):
                generateOpCuadruple(self, op)
            else:
                self.operadores.append(op)
                return

    @_('exp term_op e3 termino q1', 'termino q1')
    def exp(self, p):
        # print('---- exp')
        return p[0]

    #Punto neuralgico para exp
    @_('')
    def e3(self, p):
        # print(f'----- e3 {p[-1]}')
        self.operadores.append(p[-1])

    #quads suma resta
    @_('')
    def q2(self, p):
        # print(f'------ q2 {self.operadores}')
        while len(self.operadores) > 0:
            op = self.operadores.pop()
            if (op == '*' or op == '/'):
                generateOpCuadruple(self, op)
            else:
                self.operadores.append(op)
                return

    @_('SUM', 'SUB')
    def term_op(self, p):
        # print('----- term_op')
        return p[0]

    @_('termino fact_op e2 factor q2', 'factor q2')
    def termino(self, p):
        # print('----- termino')
        return p[0]

#quads mult div

    @_('')
    def q1(self, p):
        # print(f'----- q1 {self.operadores}')
        if (len(self.operadores) > 0):
            op = self.operadores.pop()
            if (op == '+' or op == '-'):
                generateOpCuadruple(self, op)
            else:
                self.operadores.append(op)

    @_('')
    def q3(self, p):
        if (len(self.operadores) > 0):
            op = self.operadores.pop()
            if (op == '='):
                lo = self.operandos.pop()
                temp = self.operandos.pop()
                loDir = self.vardir.get_var_address(lo)
                tempDir = self.vardir.get_var_address(temp)
                myQuad = Quadruple(loDir, None, op, tempDir)
                self.quadruples.append(myQuad)
                self.quadcount = self.quadcount + 1
                print(f'| q3 {self.quadcount} |')
            else:
                self.operadores.append(op)

    #Punto neuralgico para terminos
    @_('')
    def e2(self, p):
        # print('------ e2')
        self.operadores.append(p[-1])

    @_('MULT', 'DIV')
    def fact_op(self, p):
        # print('------ factor_op')
        return p[0]

    @_('open_pth expression close_pth', 'var_cte e1')
    def factor(self, p):
        # print('------ factor')
        return p[0]

    #Punto neuralgico para todos los operandos
    @_('')
    def e1(self, p):
        # print(f'------- e1 {p[-1]}')
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
        # print('--- log_op')
        return p[0]

    @_('LESS_THAN', 'MORE_THAN', 'DIFFERENT_TO', 'LESS_OR_EQ_THAN',
       'MORE_OR_EQ_THAN', 'EQUAL_TO')
    def rel_op(self, p):
        # print('---- rel_op', p[-1])
        self.operadores.append(p[-1])

    @_('ID func1 OPEN_PTH func_call_param CLOSE_PTH func3 \n')
    def func_call(self, p):
        self.id = p.ID
        return p[-1]

    #regresa tamano
    @_('')
    def func1(self, p):
        self.id = p[-1]
        self.myQuad = Quadruple(None, None, 'ERA',
                                self.funcparamcont)  #ERA | | | SIZE
        self.quadruples.append(self.myQuad)
        self.quadcount = self.quadcount + 1
        print(f'func1 {self.quadcount}')

    @_('expression func2 multiple_fc_param')
    def func_call_param(self, p):
        return p[0]

    @_('')
    def func2(self, p):
        self.paramCont = self.paramCont + 1
        param = self.operandos.pop()
        paramdir = self.vardir.get_var_address(param)
        self.paramQuad = Quadruple(paramdir, None, 'PARAM',
                                   self.paramCont)  # PARAM | ADDR | | #PARAM
        self.quadruples.append(self.paramQuad)
        self.quadcount = self.quadcount + 1

    @_('')
    def func3(self, p):
        self.myQuad = Quadruple(self.id, None, 'GOSUB',
                                self.funcdir.get_func_addr(
                                    self.id))  #GOSUB | NAME | | INIT ADDR
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

    @_('WRITE OPEN_PTH expression CLOSE_PTH wr2 \n')
    def write(self, p):
        return p[0]

    @_('')
    def wr2(self, p):
        lo = self.operandos.pop()
        loDir = self.vardir.get_var_address(lo)
        self.myQuad = Quadruple(loDir, None, 'write', None)
        self.quadcount = self.quadcount + 1
        self.quadruples.append(self.myQuad)
        print(f'| wr2 {self.quadcount} |')
        #print(self.myQuad)

    @_('IF con_expression if1 \n stmnt if2 else_stmnt')
    def if_stmnt(self, p):
        # print('- if_stmnt')
        return p[0]

    @_('')
    def if1(self, p):
        # self.gotofdir = self.quadcount
        self.conQuad = Quadruple(None, None, 'gotof', None)
        self.returnquad.append(len(self.quadruples))
        self.quadcount = self.quadcount + 1
        self.quadruples.append(self.conQuad)
        print(f'-- if1 {self.quadcount}')

    @_('')
    def if2(self, p):
        # print('-- if2')
        # self.operandos.append(self.temporal)
        valor = self.vardir.get_var_address(f't{self.temporal}')
        print(f'| if2... {valor} {self.jump} {self.quadcount} |')
        self.conQuad = Quadruple(valor, None, 'gotof', self.quadcount + 1)
        # self.quadcount = self.quadcount + 1
        idx = self.returnquad.pop()
        self.quadruples[idx] = self.conQuad

    @_('\n ELSE if3 \n stmnt if4 END \n', '\n END \n')
    def else_stmnt(self, p):
        # print('-- else_stmnt')
        return p[0]

    @_('')
    def if3(self, p):
        print('--- if3')
        self.conQuad = Quadruple(None, None, 'goto', None)
        # self.quadcount = self.quadcount + 1
        self.returnquad.append(len(self.quadruples))
        self.quadruples.append(self.conQuad)

    @_('')
    def if4(self, p):
        print(f'--- if4 {self.quadcount}')
        # self.jump.append(self.quadcount)
        print(f'--- if4 {self.jump}')
        self.operandos.append(self.temporal)
        self.conQuad = Quadruple(self.operandos.pop(), None, 'goto',
                                 self.quadcount + 1)
        idx = self.returnquad.pop()
        self.quadruples[idx] = self.conQuad

    @_('WHILE w1 con_expression w2 \n stmnt \n w3 END \n')
    def while_stmnt(self, p):
        return p[0]

    @_('')
    def w1(self, p):
        self.jump.append(self.quadcount)
        print(f'| w1 {self.jump} |')

    @_('')
    def w2(self, p):
        self.myQuad = Quadruple(self.operandos.pop(), None, 'gotof', None)
        self.returnquad.append(len(self.quadruples))
        self.quadruples.append(self.myQuad)
        self.jump.append(self.quadcount - 1)
        print(f'| w2 {self.jump} |')

    @_('')
    def w3(self, p):
        self.jump.append(self.quadcount - 1)
        print(f'| w3 {self.jump} |')
        self.operandos.append(self.temporal)
        self.conQuad = Quadruple(self.operandos.pop(), None, 'gotof',
                                 self.jump.pop())
        idx = self.returnquad.pop()
        self.quadruples[idx] = self.conQuad
        self.conQuad = Quadruple(None, None, 'gotot', self.jump.pop())
        self.quadruples.append(self.conQuad)

    @_('expression log_op e7 expression q5', 'expression q5')
    def con_expression(self, p):
        # print('-- con_expression')
        return p[-1]

    @_('')
    def e7(self, p):
        # print(f'--- e7 {p[-1]}')
        self.operadores.append(p[-1])

    @_('')
    def q5(self, p):
        # print('--- q5')
        while len(self.operadores) > 0:
            op = self.operadores.pop()
            if (op.lower() == 'and' or op.lower() == 'or'):
                generateOpCuadruple(self, op)
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

    @_('MAIN fd1 ftr resetvars \n sq1 stmnt vd1 END')
    def main(self, p):
        return p[0]

    @_('')
    def sq1(self, p):
        # self.quadcount = self.quadcount + 1
        # self.jump.append(self.quadcount)
        print(f'| sq1 {self.jump} {self.quadcount}|')

    @_('')
    def empty(self, p):
        pass


# if __name__ == '__main__':
#     lexer = MikuLexer()
#     parser = MikuParser()
#     filename = 'test.txt'

#     with open(filename) as fp:
#         try:
#             result = parser.parse(lexer.tokenize(fp.read()))
#         except EOFError:
#             pass
