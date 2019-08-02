######
# PyChip8

# Author: Jake Robinson
# Date  : 08/01/2019

# Running through a list of CPUs to emulate. Trying a few things to learn
# a process to do these emulations easy.

# Verison:
# 0.0 - First commit, adding comments and other starting things
min_ver, maj_ver = 0,0

RAM = []  # Im not sure if I like the RAM being a list

class CPU():
    ''' Handles the opcodes and the register values '''
    def __init__(self):
        # Registers
        pass

    def decode(self, opcode):
        # Just going to be a large if statment
        # There might be a way to do this with
        # dictionaries, but this will work for now
        pass


with open('./pong.ch8', 'rb') as f:
    raw_data = f.read()

# load the RAM
for item in [(x,y) for x,y in zip(raw_data[::2], raw_data[1::2])]:
    RAM.append("{:02X}{:02X}".format(ord(item[0]), ord(item[1])))



    

if __name__ == "__main__":
    print("Python Chip 8 Emulator")
    print("Verison: {}.{}".format(maj_ver, min_ver))
