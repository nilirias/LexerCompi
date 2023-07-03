from miku_lexer import *
from miku_parser import *
import sys

from read import run_vm

if __name__ == '__main__':
    lexer = MikuLexer()
    parser = MikuParser()
    filename = 'test_sumas.txt'
    print(f'compilando miku - {filename}')
    success = False

    if (len(sys.argv) > 1):
        filename = sys.argv[1]

    with open(filename) as fp:
        try:
            program_name, quads, funcdir, ctedir = parser.parse(lexer.tokenize(fp.read()))
            outfile = open(program_name + '.miku', 'w')

            outfile.write(str(funcdir) + '\n')

            for quad in quads:
                #print(str(quad))
                outfile.write(str(quad) + '\n')
            #print('Code compiled successfully to', program_name + '.miku')
            success = True
        except EOFError:
            pass
        finally:
            outfile.close()

    if (success):
        print("Running vm...\n\n")
        run_vm()
