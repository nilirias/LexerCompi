from os import DirEntry, read, getcwd
from pathlib import Path
import io
import sys
from direcciones import *
import json


class Memory:

    def __init__(self, num, word, bool, memoryType):
        self.ints = [None] * int(num)
        self.strings = [None] * int(word)
        self.bools = [None] * int(bool)
        self.memoryType = memoryType

    def insert_num(self, arr_num):
        for idx, values in enumerate(arr_num):
            self.ints[idx] = int(values)

    def insert_word(self, arr_word):
        for idx, values in enumerate(arr_word):
            self.strings[idx] = values

    def insert_bools(self, arr_bools):
        for idx, values in enumerate(arr_bools):
            self.bools[idx] = values == 'true'

    def get_value_of_address(self, address):
        # print(f'get_value_of_address address: {address} | {self.memoryType}')
        # print(
        #     f'get_value_of_address address: {self.bools} | {self.strings} | {self.ints}'
        # )
        if address >= dir_memoria[self.memoryType][2]:
            return self.bools[address - dir_memoria[self.memoryType][2]]
        elif address >= dir_memoria[self.memoryType][1]:
            return self.strings[address - dir_memoria[self.memoryType][1]]
        else:
            return self.ints[address - dir_memoria[self.memoryType][0]]

    def set_value_in_address(self, address, value):
        # print("--------------------------------")
        # print(
        #     f'set_value_in_address address: {address} | {value} | {self.memoryType}'
        # )
        # print(
        #     f'set_value_in_address address: {dir_memoria[self.memoryType][2]} | {dir_memoria[self.memoryType][1]} | {dir_memoria[self.memoryType][0]}'
        # )
        # print(
        #     f'set_value_in_address address: {self.bools} | {self.strings} | {self.ints}'
        # )
        if address >= dir_memoria[self.memoryType][2]:
            self.bools[address - dir_memoria[self.memoryType][2]] = value
        elif address >= dir_memoria[self.memoryType][1]:
            self.strings[address - dir_memoria[self.memoryType][1]] = value
        else:
            self.ints[address - dir_memoria[self.memoryType][0]] = value
        # print(
        #     f'set_value_in_address address: {self.bools} | {self.strings} | {self.ints}'
        # )
        # print("--------------------------------")


# var globales
memories = []
pila_cuadruplos = []


def filter_ctes(cte):
    return cte["type"] == "cte"


def get_var_type_memory(address):
    if address >= dir_memoria[3][0]:
        return 3
    elif address >= dir_memoria[2][0]:
        return 2
    elif address >= dir_memoria[1][0]:
        return 1
    else:
        return 0


def getValueFromAddress(address):
    type = get_var_type_memory(address)

    if type == 1 or type == 2:
        return memories[type][-1].get_value_of_address(address)
    else:
        return memories[type].get_value_of_address(address)


def setValueInAddress(address, value):
    type = get_var_type_memory(address)

    if type == 1 or type == 2:
        memories[type][-1].set_value_in_address(address, value)
    else:
        memories[type].set_value_in_address(address, value)


def era(funcdir, funcion):
    # print('era', funcion)
    func = [func for func in funcdir if func['quad'] == funcion][0]
    lclmem = Memory(func['varc'][0], func['varc'][1], func['varc'][2], 1)
    tempmem = Memory(func['vart'][0], func['vart'][1], func['vart'][2], 2)

    memories[1].append(lclmem)
    memories[2].append(tempmem)


def param(valorAddr, destinoAddr):
    type = get_var_type_memory(valorAddr)
    # print(' param' ,type, memories[3].ints)
    if type == 1 or type == 2:
        valor = memories[type][-2].get_value_of_address(valorAddr)
    else:
        valor = memories[type].get_value_of_address(valorAddr)

    memories[1][-1].set_value_in_address(destinoAddr, valor)


def run_vm():
    obj_file_name = 'test.miku'
    ip = 0

    with open(obj_file_name) as f:
        funcdir = json.loads(f.readline().strip())
        varg = json.loads(f.readline().strip())

        # print(f'varg {varg}')
        # print(f'funcdir {funcdir}')

        ctes = list(filter(filter_ctes, funcdir[-1]['var']))

        ctesEra = [0, 0, 0]
        for s in ctes:
            dir = s['addr']
            if dir >= dir_memoria[3][2]:
                ctesEra[2] += 1
            elif dir >= dir_memoria[3][1]:
                ctesEra[1] += 1
            else:
                ctesEra[0] += 1

        quads = f.readlines()

        glb_var_mem = Memory(varg[0], varg[1], varg[2], 0)
        lcl_var_mem = [
            Memory(funcdir[-1]['varc'][0], funcdir[-1]['varc'][1],
                   funcdir[-1]['varc'][2], 1)
        ]
        tmp_var_mem = [
            Memory(funcdir[-1]['vart'][0], funcdir[-1]['vart'][1],
                   funcdir[-1]['vart'][2], 2)
        ]
        cte_var_mem = Memory(ctesEra[0], ctesEra[1], ctesEra[2], 3)
        # print('cte_var_mem', cte_var_mem.insert_bools, ctesEra)

        # print("-------- llenando memoria constantes")
        for s in ctes:
            # print(s)
            cte_var_mem.set_value_in_address(int(s["addr"]), s['name'])
        # print("-------- termino llenando memoria constantes")

        memories.append(glb_var_mem)
        memories.append(lcl_var_mem)
        memories.append(tmp_var_mem)
        memories.append(cte_var_mem)

        while (ip < len(quads)):
            print(f'------- cuadruplo | {quads[ip]}')
            op, left, right, res = quads[ip].strip().split()
            if (op == '+' or op == '-' or op == '*' or op == '/' or op == '=='
                    or op == ">" or op == "<" or op == ">=" or op == "<="):

                valueLeft = getValueFromAddress(int(left))
                valueRight = getValueFromAddress(int(right))

                if op == "+":
                    value = valueLeft + valueRight
                elif op == "-":
                    value = valueLeft - valueRight
                elif op == "*":
                    value = valueLeft * valueRight
                elif op == "/":
                    value = valueLeft / valueRight
                elif op == "==":
                    value = valueLeft == valueRight
                elif op == ">":
                    value = valueLeft > valueRight
                elif op == "<":
                    value = valueLeft < valueRight
                elif op == ">=":
                    value = valueLeft >= valueRight
                elif op == "<=":
                    value = valueLeft <= valueRight

                # print("value", op, valueLeft, valueRight, value)

                setValueInAddress(int(res), value)
            elif (op == "="):
                # print(resInt)
                setValueInAddress(int(res), getValueFromAddress(int(left)))
            elif (op == "write"):
                print(getValueFromAddress(int(left)))
            elif (op == "gotof"):
                # print(f"gotof {ip}")
                if (not getValueFromAddress(int(left))):
                    # print(f"cambiar {ip}")
                    ip = int(res) - 1
                # print(f'gotof {ip}')
            elif (op == "gotot"):
                print(f'gotot | {quads[ip]}')
                # print(f"gotof {ip}")
                if (getValueFromAddress(int(left))):
                    # print(f"cambiar {ip}")
                    ip = int(res) - 1
                # print(f'gotof {ip}')

            elif (op == "goto"):
                # print(f'goto {ip}')
                ip = int(res) - 1
                # print(f'goto {ip}')
            elif (op == 'ERA'):
                era(funcdir, int(res))
            elif (op == 'PARAM'):
                param(int(left), int(res))
                # print('param', getValueFromAddress(int(res)))
            elif (op == 'GOSUB'):
                pila_cuadruplos.append(ip)
                ip = int(res) - 1
            elif (op == 'return'):
                setValueInAddress(int(res), getValueFromAddress(int(left)))
                ip = pila_cuadruplos.pop()
                memories[1].pop()
                memories[2].pop()
            else:
                print(f'| missing cuadruplo {quads[ip]} |')
            ip += 1


if __name__ == '__main__':
    run_vm()
