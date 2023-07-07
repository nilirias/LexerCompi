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
        if address > dir_memoria[self.memoryType][2]:
            return self.bools[address - dir_memoria[self.memoryType][2]]
        elif address > dir_memoria[self.memoryType][1]:
            return self.strings[address - dir_memoria[self.memoryType][1]]
        else:
            return self.ints[address - dir_memoria[self.memoryType][0]]

    def set_value_in_address(self, address, value):
        # print(f'set_value_in_address address: {address} | {value}')
        if address > dir_memoria[self.memoryType][2]:
            self.bools[address % dir_memoria[self.memoryType][2]] = value
        elif address > dir_memoria[self.memoryType][1]:
            self.strings[address % dir_memoria[self.memoryType][1]] = value
        else:
            self.ints[address % dir_memoria[self.memoryType][0]] = value


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


def run_vm():
    obj_file_name = 'test.miku'
    ip = 0

    with open(obj_file_name) as f:
        funcdir = json.loads(f.readline().strip())

        ctes = list(filter(filter_ctes, funcdir[0]['var']))

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

        glb_var_mem = Memory(0, 0, 0, 0)
        lcl_var_mem = Memory(funcdir[-1]['varc'][0], funcdir[-1]['varc'][1],
                             funcdir[-1]['varc'][2], 1)
        tmp_var_mem = Memory(funcdir[-1]['vart'][0], funcdir[-1]['vart'][1],
                             funcdir[-1]['vart'][2], 2)
        cte_var_mem = Memory(ctesEra[0], ctesEra[1], ctesEra[2], 3)

        # print("-------- llenando memoria constantes")
        for s in ctes:
            # print(s)
            cte_var_mem.set_value_in_address(int(s["addr"]), s['name'])
        # print("-------- termino llenando memoria constantes")

        memories = [glb_var_mem, lcl_var_mem, tmp_var_mem, cte_var_mem]

        while (ip < len(quads)):
            # print(f'------- cuadruplo | {quads[ip]}')
            op, left, right, res = quads[ip].strip().split()
            if (op == '+' or op == '-' or op == '*' or op == '/'):
                leftInt = int(left)
                rightInt = int(right)
                resInt = int(res)
                valueLeft = memories[get_var_type_memory(
                    leftInt)].get_value_of_address(leftInt)
                valueRight = memories[get_var_type_memory(
                    rightInt)].get_value_of_address(rightInt)

                if op == "+":
                    value = valueLeft + valueRight
                elif op == "-":
                    value = valueLeft - valueRight
                elif op == "*":
                    value = valueLeft * valueRight
                elif op == "/":
                    value = valueLeft / valueRight

                # print("value", op, valueLeft, valueRight, value)

                memories[get_var_type_memory(resInt)].set_value_in_address(
                    resInt, value)
            elif (op == "="):
                leftInt = int(left)
                resInt = int(res)
                # print(resInt)
                memories[get_var_type_memory(resInt)].set_value_in_address(
                    resInt, memories[get_var_type_memory(
                        leftInt)].get_value_of_address(leftInt))
            elif (op == "write"):
                print(memories[get_var_type_memory(
                    int(left))].get_value_of_address(int(left)))
            elif (op == "gotof"):
                print("gotof :)))")
                if (not memories[get_var_type_memory(
                        int(left))].get_value_of_address(int(left))):
                    ip = int(res) - 1
            elif (op == "goto"):
                print("goto :)))")
                ip = int(res) - 1
            ip += 1


if __name__ == '__main__':
    run_vm()
