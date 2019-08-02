######
# PyChip8

# Author: Jake Robinson
# Date  : 08/01/2019

# Running through a list of CPUs to emulate. Trying a few things to learn
# a process to do these emulations easy.

# Verison:
# 0.0 - First commit, adding comments and other starting things
min_ver, maj_ver = 0,0

DEBUG = 1

ROM = {}  # Im not sure if I like the RAM being a list

class CPU():
    ''' Handles the opcodes and the register values '''
    def __init__(self):
        # Registers
        self.I  = 0
        self.PC = 0x200
        self.STACK = {}
        self.SP = 0
        self.V  = {'{:X}'.format(x) : '0' for x in range(16)}

    def decode(self, opcode):
        # Just going to be a large if statment
        # There might be a way to do this with
        # dictionaries, but this will work for now
        if opcode[0] == '0':  # 2 instructions
            if opcode == '00E0':
                if DEBUG: print("[DEBUG] opcode[00E0] - clear the display")
            elif opcode == '00EE':
                if DEBUG: print("[DEBUG] opcode[00EE] - return from a subroutine")
                # The interpreter sets the PC to the address at the top of the
                # stack, then subtracts 1 from the stack pointer
                self.PC = self.STACK[self.SP]
                self.SP = self.SP - 1

        elif opcode[0] == '1':  # 1 instruction
            if DEBUG: print("[DEBUG] opcode[1nnn] JP {}".format(opcode[1:]))
            self.PC = int(opcode[1:], 16)
            
        elif opcode[0] == '2':  # 1 instruction
            if DEBUG: print("[DEBUG] opcode[2nnn] CALL {}".format(opcode[1:]))
            self.SP = self.SP + 1
            self.STACK[self.SP] = self.PC
            self.PC = int(opcode[1:], 16)
            
        elif opcode[0] == '3':  # 1 instruction
            if DEBUG:
                print("[DEBUG] opcode[3xkk] SE V{}, {}".format(opcode[1], opcode[2:]))
            if self.V[opcode[1]] == int(opcode[2:], 16):
                self.PC = self.PC + 4
            else:
                self.PC = self.PC + 2
                
        elif opcode[0] == '4':  # 1 instruction
            if DEBUG:
                print("[DEBUG] opcode[4xkk] SNE V{}, {}".format(opcode[1], opcode[2:]))
            if self.V[opcode[1]] != int(opcode[2:], 16):
                self.PC = self.PC + 4
            else:
                self.PC = self.PC + 2
                
        elif opcode[0] == '5':  # 1 instruction
            if DEBUG:
                print("[DEBUG] opcode[5xy0] SE V{}, V{}".format(opcode[1], opcode[2]))
            if self.V[opcode[1]] == self.V[opcode[2]]:
                self.PC = self.PC + 4
            else:
                self.PC = self.PC + 2
                
        elif opcode[0] == '6':  # 1 instruction
            if DEBUG:
                print("[DEBUG] opcode[6xkk] LD V{}<-{}".format(opcode[1], opcode[2:]))
            self.V[opcode[1]] = int(opcode[2:], 16)
            self.PC = self.PC + 2
            
        elif opcode[0] == '7':  # 1 instruction
            if DEBUG:print("[DEBUG] opcode[7xkk] ADD V{}, {}".format(opcode[1], opcode[2:]))
            self.V[opcode[1]] = self.V[opcode[1]] + int(opcode[2:], 16)
            self.PC = self.PC + 2
            
        elif opcode[0] == '8':  # 8 instruction
            pass
        elif opcode[0] == '9':  # 1 instruction
            if DEBUG: print("[DEBUG] opcode[9xy0] SNE V{}, V{}".format(opcode[1], opcode[2]))
            if self.V[opcode[1]] != self.V[opcode[2]]:
                self.PC = self.PC + 4
            else:
                self.PC = self.PC + 2

        elif opcode[0] == 'A':  # 1 instruction
            if DEBUG: print("[DEBUG] opcode[Annn] LD I, {}".format(opcode[1:]))
            self.I = int(opcode[1:], 16)
            self.PC = self.PC + 2
            
        elif opcode[0] == 'B':  # 1 instruction
            pass
        elif opcode[0] == 'C':  # 1 instruciton
            pass
        elif opcode[0] == 'D':  # 1 instruction
            if DEBUG: print("[DEBUG] opcode[Dxyn]")
            self.PC = self.PC + 2
            
        elif opcode[0] == 'E':  # 2 instruction
            pass
        elif opcode[0] == 'F':  # 9 instruction
            pass


with open('./pong.ch8', 'rb') as f:
    raw_data = f.read()

# load the RAM
for num, item in enumerate([(x,y) for x,y in zip(raw_data[::2], raw_data[1::2])]):
    ROM[(num*2)+0x200] = "{:02X}{:02X}".format(ord(item[0]), ord(item[1]))


cpu = CPU()

while(True):
    if DEBUG: print("[DEBUG] PC: {:03X}".format(cpu.PC))
    if DEBUG: print("[DEBUG] OPCODE: {}".format(ROM[cpu.PC]))
    cpu.decode(ROM[cpu.PC])
    

if __name__ == "__main__":
    print("Python Chip 8 Emulator")
    print("Verison: {}.{}".format(maj_ver, min_ver))
