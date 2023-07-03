from miku_vardir import *
import json

class FuncDir:
    def __init__(self):
        self.funcs = []

    def add_func(self, name, ret, varc, params, vart, addr, var):
        self.funcs.append(FuncDirEntry(name, ret, varc, params, vart, addr, var))

    def get_func_addr(self, name):
        return [func.addr for func in self.funcs if func.name == name]

    def __str__(self):
      #print('vardir.__str__', json.dumps([str(i) for i in self.vars]))
      #return json.dumps([str(i) for i in self.vars])
      return json.dumps([json.loads(str(i)) for i in self.funcs])

class FuncDirEntry:
    def __init__(self, name, ret, varc, params, vart, addr, var):
      self.name = name #function name
      self.ret = ret #return type | 0 for main | 1 for void | 2 for number | 3 for word | 4 for bool
      self.varc = varc #count of variables (how many variables it has) [numbers, words, bools]
      self.params = params #count of parameters
      self.vart = vart #count of temporary variables
      self.addr = addr #direccion del cuadruplo
      self.var = var #pointer to the variable directory

    def __str__(self):
      # print('vardirentry.__str__', json.dumps({'name': self.name, 'addr': self.addr}))
      print('vardirentry.__str__', json.dumps({'name': self.name, 'ret': self.ret, 'varc': self.varc, 'params': self.params, 'vart': self.vart, 'addr': self.addr, 'var': str(self.var)}))
      return json.dumps({'name': self.name, 'ret': self.ret, 'varc': self.varc, 'params': self.params, 'vart': self.vart, 'addr': self.addr, 'var': json.loads(str(self.var))})
