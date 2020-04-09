from collections import namedtuple

OpEntry = namedtuple("OpEntry", "decode func name type")


def rm_letters(string):
    """ Remove Letters from a string """
    result = ''.join(i for i in string if not i.isalpha())
    return result


class Cpu:
    def __init__(self):
        self.stack = [0]*16
        self.sp = 0
        self.pc = 0
        self.v = [0]*16
        self.i = 0
        self.dt = 0
        self.st = 0
        self.mem = [0]*256

        self.op = Opcode(self)

    def execute(self, inst, val):
        print(inst.name)
        self.pc += inst.func(val)

    def step(self, num):
        print('{:016b}'.format(self.mem[self.pc]))
        inst, val = self.op.fetch('{:016b}'.format(self.mem[self.pc]))
        self.execute(inst, val)
        print("PC : {}".format(self.pc))



class Opcode:
    def __init__(self, cpu):
        self.cpu = cpu

        self.op_lookup = [
            OpEntry("0000000011100000", self.op_cls, "CLS", 0),
            OpEntry("0000000011101110", self.op_ret, "RET", 1),
            OpEntry("0000nnnnnnnnnnnn", self.op_sys, "SYS", 2),
            OpEntry("0001nnnnnnnnnnnn", lambda x: self.op_jp(0, x), "JP", 2),
            OpEntry("0010nnnnnnnnnnnn", self.op_call, "CALL", 2),
            OpEntry("0011xxxxkkkkkkkk", lambda x: self.op_se(0, x), "SE", 3),
            OpEntry("0100xxxxkkkkkkkk", lambda x: self.op_sne(0, x), "SNE", 3),
            OpEntry("0101xxxxyyyy0000", lambda x: self.op_se(1, x), "SE", 4),
            OpEntry("0110xxxxkkkkkkkk", lambda x: self.op_ld(0, x), "LD", 3),
            OpEntry("0111xxxxkkkkkkkk", lambda x: self.op_add(0, x), "ADD", 3),
            OpEntry("1000xxxxyyyy0000", lambda x: self.op_ld(1, x), "LD", 4),
            OpEntry("1000xxxxyyyy0001", self.op_or, "OR", 4),
            OpEntry("1000xxxxyyyy0010", self.op_and, "AND", 4),
            OpEntry("1000xxxxyyyy0011", self.op_xor, "XOR", 4),
            OpEntry("1000xxxxyyyy0100", lambda x: self.op_add(1, x), "ADD", 4),
            OpEntry("1000xxxxyyyy0101", self.op_sub, "SUB", 4),
            OpEntry("1000xxxxyyyy0110", self.op_shr, "SHR", 4),
            OpEntry("1000xxxxyyyy0111", self.op_subn, "SUBN", 4),
            OpEntry("1000xxxxyyyy1110", self.op_shl, "SHL", 4),
            OpEntry("1001xxxxyyyy0000", lambda x: self.op_sne(1, x), "SNE", 4),
            OpEntry("1010nnnnnnnnnnnn", lambda x: self.op_ld(2, x), "LD", 2),
            OpEntry("1011nnnnnnnnnnnn", lambda x: self.op_jp(1, x), "JP", 2),
            OpEntry("1100xxxxkkkkkkkk", self.op_rnd, "RND", 3),
            OpEntry("1101xxxxyyyynnnn", self.op_drw, "DRW", 5),
            OpEntry("1110xxxx10011110", self.op_skp, "SKP", 6),
            OpEntry("1110xxxx10100001", self.op_sknp, "SKNP", 6),
            OpEntry("1111xxxx00000111", lambda x: self.op_ld(3, x), "LD", 6),
            OpEntry("1111xxxx00001010", lambda x: self.op_ld(4, x), "LD", 6),
            OpEntry("1111xxxx00010101", lambda x: self.op_ld(5, x), "LD", 6),
            OpEntry("1111xxxx00011000", lambda x: self.op_ld(6, x), "LD", 6),
            OpEntry("1111xxxx00011110", lambda x: self.op_add(1, x), "ADD", 6),
            OpEntry("1111xxxx00101001", lambda x: self.op_ld(7, x), "LD", 6),
            OpEntry("1111xxxx00110011", lambda x: self.op_ld(8, x), "LD", 6),
            OpEntry("1111xxxx01010101", lambda x: self.op_ld(9, x), "LD", 6),
            OpEntry("1111xxxx01100101", lambda x: self.op_ld(10, x), "LD", 6)
        ]

        self.decode_keys = [rm_letters(x.decode) for x in self.op_lookup]

    def op_break(self, opcode, decode):
        """ Break-up the Opcode"""
        tmp_dict = {x: '' for x in set(decode) if x not in ('0', '1')}
        tmp_dict['s'] = ''
        for item, key in zip(opcode, decode):
            if key in tmp_dict:
                tmp_dict[key] += item
            else:
                tmp_dict['s'] += item
        return tmp_dict

    def fetch(self, opcode):
        """ Get the items for the opcode """
        tmp_decode = [self.op_break(opcode, x.decode)['s'] for x in self.op_lookup]
        op_idx = [x == y for x, y in zip(tmp_decode, self.decode_keys)].index(True)
        tmp_v = self.op_break(opcode, self.op_lookup[op_idx].decode)
        op_v = {x: int(y, 2) for x, y in zip(tmp_v.keys(), tmp_v.values()) if x != "s"}
        return self.op_lookup[op_idx], op_v

    def op_cls(self, arg):
        return 1

    def op_ret(self, arg):
        ret_v = self.cpu.stack[self.cpu.sp]
        self.cpu.sp -= 1
        return ret_v

    def op_call(self, arg):
        self.cpu.sp += 1
        self.cpu.stack[self.cpu.sp] = self.cpu.pc
        return arg['n']

    def op_sys(self, arg):
        return 1

    def op_jp(self, idx, arg):
        tmp = [
            arg['n'],
            arg['n'] + self.cpu.v[0]
        ]
        self.cpu.pc = tmp[idx]
        return 0

    def op_se(self, idx, arg):
        tmp = [
            [1, 2][self.cpu.v[arg['x']] == arg['k']],
            [1, 2][self.cpu.v[arg['x']] == self.cpu.v[arg['y']]],
        ]
        ret_v = tmp[idx]
        return ret_v

    def op_sne(self, idx, arg):
        tmp = [
            [1, 2][self.cpu.v[arg['x']] != arg['k']],
            [1, 2][self.cpu.v[arg['x']] != self.cpu.v[arg['y']]],
        ]
        ret_v = tmp[idx]
        return ret_v

    def op_ld(self, idx, arg):
        if idx == 0:
            self.cpu.v[arg['x']] = arg['k']
        elif idx == 1:
            self.cpu.v[arg['x']] = self.cpu.v[arg['y']]
        elif idx == 2:
            self.cpu.i = arg['n']
        elif idx == 3:
            self.cpu.v[arg['x']] = self.cpu.dt
        elif idx == 4:  # Key Press
            pass
        elif idx == 5:
            self.cpu.dt = self.cpu.v[arg['x']]
        elif idx == 6:
            self.cpu.st = self.cpu.v[arg['x']]
        return ret_v

    def op_add(self, args):
        pass

    def op_or(self, args):
        pass

    def op_and(self, args):
        pass

    def op_xor(self, args):
        pass

    def op_sub(self, args):
        pass

    def op_shr(self, args):
        pass

    def op_subn(self, args):
        pass

    def op_shl(self, args):
        pass

    def op_rnd(self, args):
        pass

    def op_drw(self, args):
        pass

    def op_skp(self, args):
        pass

    def op_sknp(self, args):
        pass

    addr_lookup = [
        None,
        None,

    ]


if __name__ == "__main__":
    cpu = Cpu()
    cpu.mem[0] = 0x1002
    cpu.mem[1] = 0x1000
    cpu.mem[2] = 0x100A
    cpu.step(1)
    cpu.step(1)
    cpu.step(1)
