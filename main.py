from mvp import *
from miku_lexer import *
from miku_parser import *
import sys

def parse_func_dir(func_dir, outfile):
    for func_name in func_dir:
        parsed_str = func_name + ' '
        for key in func_dir[func_name]:
            if key == 'params' and func_dir[func_name][key] == '':
                func_dir[func_name][key] = '-'
            if key == 'return_type':
                types = [None, 'int', 'float', 'string', 'bool', 'void']
                func_dir[func_name][key] = types.index(
                    func_dir[func_name][key]) - 1
            parsed_str += str(func_dir[func_name][key]) + ' '
        outfile.write(parsed_str + '\n')

if __name__ == '__main__':
  lexer = MikuLexer()
  parser = MikuParser()
  filename = 'test_assign.txt'

  if(len(sys.argv) > 1):
      filename = sys.argv[1]

  with open(filename) as fp:
      try:
          program_name, quads = parser.parse(
              lexer.tokenize(fp.read()))
          outfile = open(program_name + '.miku', 'w')
          # parse_func_dir(func_dir, outfile)
          # outfile.write('#\n')
          # parse_constant_table(constant_table, outfile)
          # outfile.write('#\n')
          for quad in quads:
              outfile.write(str(quad) + '\n')
          print('Code compiled successfully to', program_name + '.miku')
      except EOFError:
          pass