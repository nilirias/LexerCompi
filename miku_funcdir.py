from miku_vardir import *

class FuncDir:
    def __init__(self):
        self.funcs = []

    def add_func(self, name, ret, varc, params, vart, var):
        self.funcs.append(FuncDirEntry(name, ret, varc, params, vart, var))
  
    def __str__(self):
            return '\n'.join(str(i) for i in self.funcs)

class FuncDirEntry:
    def __init__(self, name, ret, varc, params, vart, var):
      self.name = name #function name
      self.ret = ret #return type
      self.varc = varc #count of variables (how many variables it has)
      self.params = params #count of parameters
      self.vart = vart #count of temporary variables
      self.var = var #pointer to the variable directory

    def __str__(self):
        return f'{self.name} {self.ret} {self.varc} {self.params} {self.vart} {self.var}'