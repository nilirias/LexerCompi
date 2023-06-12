class VarDir:
    def __init__(self):
        self.vars = []

    def add_var(self, name, addr, dim1, dim2):
      if all(entry.name != name for entry in self.vars):
        self.vars.append(VarDirEntry(name, addr, dim1, dim2))

    def var_count(self):
        return len(self.vars)
  
    def __str__(self):
            return '\n'.join(str(i) for i in self.vars)

class VarDirEntry:
    def __init__(self, name, addr, dim1, dim2):
      self.name = name #variable name
      self.addr = addr #address
      self.dim1 = dim1 #array
      self.dim2 = dim2 #matrix

    def __str__(self):
        return f'{self.name} {self.addr} {self.dim1} {self.dim2}'