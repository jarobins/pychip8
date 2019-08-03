######
# PyChip8

# Author: Jake Robinson
# Date  : 08/01/2019

# Running through a list of CPUs to emulate. Trying a few things to learn
# a process to do these emulations easy.

# Verison:
# 0.0 - First commit, adding comments and other starting things
from random import randint

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
        if opcode[0] == '0':  # ######################################
            if opcode == '00E0':
                # Clear the display
                if DEBUG: print("[DEBUG][00E0] CLS")
            elif opcode == '00EE':
                # The interpreter sets the PC to the address at the top of the
                # stack, then subtracts 1 from the stack pointer
                if DEBUG: print("[DEBUG][00EE] RET")
                self.PC = self.STACK[self.SP]
                self.SP = self.SP - 1

        elif opcode[0] == '1':  # ######################################
            # Jump to the location a nnn
            if DEBUG: print("[DEBUG][1nnn] JP {}".format(opcode[1:]))
            self.PC = int(opcode[1:], 16)
            
        elif opcode[0] == '2':  # ######################################
            # Call the subroutine as nnn
            if DEBUG: print("[DEBUG][2nnn] CALL {}".format(opcode[1:]))
            self.SP = self.SP + 1
            self.STACK[self.SP] = self.PC
            self.PC = int(opcode[1:], 16)
            
        elif opcode[0] == '3':  # ######################################
            if DEBUG:
                print("[DEBUG][3xkk] SE V{}, {}".format(opcode[1], opcode[2:]))
            if self.V[opcode[1]] == int(opcode[2:], 16):
                self.PC = self.PC + 4
            else:
                self.PC = self.PC + 2
                
        elif opcode[0] == '4':  # ######################################
            if DEBUG:
                print("[DEBUG][4xkk] SNE V{}, {}".format(opcode[1], opcode[2:]))
            if self.V[opcode[1]] != int(opcode[2:], 16):
                self.PC = self.PC + 4
            else:
                self.PC = self.PC + 2
                
        elif opcode[0] == '5':  # ######################################
            if DEBUG:
                print("[DEBUG][5xy0] SE V{}, V{}".format(opcode[1], opcode[2]))
            if self.V[opcode[1]] == self.V[opcode[2]]:
                self.PC = self.PC + 4
            else:
                self.PC = self.PC + 2
                
        elif opcode[0] == '6':  # 1 instruction
            if DEBUG:
                print("[DEBUG][6xkk] LD V{}<-{}".format(opcode[1], opcode[2:]))
            self.V[opcode[1]] = int(opcode[2:], 16)
            self.PC = self.PC + 2
            
        elif opcode[0] == '7':  # ######################################
            if DEBUG:print("[DEBUG][7xkk] ADD V{}, {}".format(opcode[1], opcode[2:]))
            self.V[opcode[1]] = self.V[opcode[1]] + int(opcode[2:], 16)
            self.PC = self.PC + 2
            
        elif opcode[0] == '8':  # 8 instruction
            if opcode[3] == '0':
                if DEBUG: print("[DEBUG][8xy0] V{}<-V{}".format(opcode[1], opcode[2]))
                self.V[opcode[1]] = self.V[opcode[2]]
            elif opcode[3] == '1':
                if DEBUG: print("[DEBUG][8xy1] V{}<-V{}|V{}".format(opcode[1],
                                                                    opcode[1],
                                                                    opcode[2]))
                self.V[opcode[1]] = self.V[opcode[1]] | self.V[opcode[2]]
            elif opcode[3] == '2':
                if DEBUG: print("[DEBUG][8xy2] V{}<-V{}&V{}".format(opcode[1],
                                                                    opcode[1],
                                                                    opcode[2]))
                self.V[opcode[1]] = self.V[opcode[1]] & self.V[opcode[2]]
            elif opcode[3] == '3':
                if DEBUG: print("[DEBUG][8xy3] V{}<-V{}^V{}".format(opcode[1],
                                                                    opcode[1],
                                                                    opcode[2]))
                self.V[opcode[1]] = self.V[opcode[1]] ^ self.V[opcode[2]]
            elif opcode[3] == '4':
                if DEBUG: print("[DEBUG][8xy4] V{}<-V{}+V{}".format(opcode[1],
                                                                    opcode[1],
                                                                    opcode[2]))
                self.V[opcode[1]] = self.V[opcode[1]] + self.V[opcode[2]]
                if self.V[opcode[1]] > 255:
                    self.V[opcode['F']] = 1
                self.V[opcode[1]] = self.V[opcode[1]] % 256
            elif opcode[3] == '5':
                if DEBUG: print("[DEBUG][8xy5] V{}<-V{}-V{}".format(opcode[1],
                                                                    opcode[1],
                                                                    opcode[2]))
                if self.V[opcode[1]] > self.V[opcode[2]]:
                    self.V[opcode['F']] = 1
                self.V[opcode[1]] = self.V[opcode[1]] - self.V[opcode[2]]
            elif opcode[3] == '6':
                if DEBUG: print("[DEBUG][8xy6] V{}>>2".format(opcode[1],
                                                              opcode[1]))
                self.V[opcode['F']] = self.V[opcode[1]] % 2
                self.V[opcode[1]] = self.V[opcode[1]] >> 2
            elif opcode[3] == '7':
                if DEBUG: print("[DEBUG][8xy7] V{}<-V{}-V{}".format(opcode[1],
                                                                    opcode[2],
                                                                    opcode[1]))
                if self.V[opcode[1]] > self.V[opcode[2]]:
                    self.V[opcode['F']] = 1
                self.V[opcode[1]] = self.V[opcode[1]] - self.V[opcode[2]]
            elif opcode[3] == 'E':
                pass
            self.PC = self.PC + 2
                
        elif opcode[0] == '9':  # ######################################
            if DEBUG: print("[DEBUG][9xy0] SNE V{}, V{}".format(opcode[1], opcode[2]))
            if self.V[opcode[1]] != self.V[opcode[2]]:
                self.PC += 4
            else:
                self.PC += 2

        elif opcode[0] == 'A':  # ######################################
            if DEBUG: print("[DEBUG][Annn] LD I, {}".format(opcode[1:]))
            self.I = int(opcode[1:], 16)
            self.PC += 2
            
        elif opcode[0] == 'B':  # ######################################
            if DEBUG: print("[DEBUG][Bnnn] JP {:0X}+V0".format(opcode[1:]))
            self.PC = int(opcode[1:], 16) + self.V['0']
        elif opcode[0] == 'C':  # ######################################
            if DEBUG: print("[DEBUG][Cxkk] V{}<-RND&{:02X}".format(opcode[1],
                                                                   opcode[2:]))
            self.V[opcode[1]] = randint(0, 255) & int(opcode[2:], 16)
            self.PC += 2
            
        elif opcode[0] == 'D':  # ######################################
            if DEBUG: print("[DEBUG][Dxyn]")
            self.PC = self.PC + 2
            
        elif opcode[0] == 'E':  # ######################################
            if opcode[2:] == '9E':
                if DEBUG: print("[DEBUG][Ex9E] SKP V{}".format(opcode[1]))
            if opcode[2:] == 'A1':
                if DEBUG: print("[DEBUG][ExA1] SKNP V{}".format(opcode[1]))
            self.PC += 2
        elif opcode[0] == 'F':  # ######################################
            if opcode[2:] == '07':
                if DEBUG: print("[DEBUG][Fx07] LD V{}<-DT".format(opcode[1]))
            if opcode[2:] == '0A':
                if DEBUG: print("[DEBUG][Fx0A] LD V{}<-K".format(opcode[1]))
            if opcode[2:] == '15':
                if DEBUG: print("[DEBUG][Fx15] LD DT<-V{}".format(opcode[1]))
            if opcode[2:] == '18':
                if DEBUG: print("[DEBUG][Fx18] LD ST<-V{}".format(opcode[1]))
            if opcode[2:] == '1E':
                if DEBUG: print("[DEBUG][Fx1E] ADD I<-I+V{}".format(opcode[1]))
            if opcode[2:] == '29':
                if DEBUG: print("[DEBUG][Fx29] LD I<-V{}".format(opcode[1]))
            if opcode[2:] == '33':
                if DEBUG: print("[DEBUG][Fx33] LD BCD")
            if opcode[2:] == '55':
                if DEBUG: print("[DEBUG][Fx55] LD [I], V{}".format(opcode[1]))
            if opcode[2:] == '65':
                if DEBUG: print("[DEBUG][Fx65] LD V{}, [I]".format(opcode[1]))
            self.PC += 2


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
