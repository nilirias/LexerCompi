class VarDir:
    def __init__(self):
        self.vars = []

    def add_var(self, name, addr):
      if all(entry.name != name for entry in self.vars):
        self.vars.append(VarDirEntry(name, addr))

    def var_count(self):
        return len(self.vars)

    def get_var_address(self, name):
        print('gva',name,self.vars)
        return [var.addr for var in self.vars if var.name == name][0]

    def __str__(self):
            return '\n'.join(str(i) for i in self.vars)

class VarDirEntry:
    def __init__(self, name, addr):
      self.name = name #variable name
      self.addr = addr #address
      # self.dim1 = dim1 #array
      # self.dim2 = dim2 #matrix

    def __str__(self):
        return f'{self.name} {self.addr}'