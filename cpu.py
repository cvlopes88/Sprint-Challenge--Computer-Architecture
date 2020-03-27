import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

SP = 7

class CPU:
  
  def __init__(self):
    # Construct a new CPU
    self.ram = [0] * 256
    #registers
    self.reg = [0] * 8
    # Internal register
    # program counter
    self.pc = 0
    # Stack Pointer, initialized 1 spot above the beginning of stack when empty
    self.reg[SP] = 0xF4
    # Flags register
    self.FL = 0b00000000
    
  def load(self):
        """Load a program into memory."""
        # Error handling
        if len(sys.argv) != 2:
            print("usage: ls8.py filename")
            sys.exit(1)
            
        
        address = 0
        
        
        try:
            with open(sys.argv[1]) as p:
                for line in p:

                    #ignore comments
                    line = line.split('#')[0]

                    # Strip white space
                    line = line.strip()
                    # skip empty lines
                    if line == "":
                      continue

                    instruction = int(line, 2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print('FILE NOT FOUND')
            sys.exit(2)


  def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

  def run(self):
        """Run the CPU."""
        #load the program
        self.load()
        running = True
        print("hello")
        while True:
            # instruction register
            ir = self.ram[self.pc]
            # read command
            op = self.ram_read(ir)
            # read operands
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
        if op == LDI:
            self.reg[operand_a] = operand_b
            self.pc += 3  # Skip 3

        elif op == PRN:
            # print numeric value stored in register
            print(self.reg[operand_a])
            self.pc += 2  # skip 2

        elif op == MUL:
            self.alu("MUL", operand_a, operand_b)
            self.pc += 3

        elif op == PUSH:
                regs = self.ram[pc + 1]
                val = self.reg[regs]
                # Decrement the SP.
                self.reg[SP] -= 1
                # Copy the value in the given register to the address pointed to by SP.
                self.ram[reg[SP]] = val
                pc += 2

        elif op == POP:
            regs = self.ram[pc + 1]
            val = self.ram[regs[SP]]
            # Copy the value from the address pointed to by SP to the given register.
            # Increment SP.

        elif op == JMP:
          # Jump to the address stored in the given register.
          # Set the PC to the address stored in the given register.
          reg = self.ram_read(self.pc + 1)
          self.pc = self.reg[reg]
          
        elif op == CMP:
          # Compare the values in two registers.
          # If they are equal, set the Equal E flag to 1, otherwise set it to 0.
          # If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
          # If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
          pass

        elif op == JEQ:
          # If equal flag is set(true), jump to the address stored in the given register.
          reg = self.ram_read(self.pc + 1)
          if self.FL == 1:
            self.pc = self.reg[reg] 
          else:
            self.pc += operand_a
            
        elif op == JNE:
          reg = self.ram_read(self.pc + 1)
            # if equal flag is clear (false, 0), jump to the address stored in the given register.
          if self.fl & 0b00000001 == 0:
                self.JMP(reg)
          else:
                self.pc += 2
            
        elif op == HLT:
            running = False

        else:
            print(f"cant get this instruction: {op}")
            sys.exit(1)

  def ram_read(self, MAR):  # mar - Memory Address Register
        """Return value stored at address"""
        mdr = self.ram[MAR]  # mdr - Memory Data Register
        return mdr

  def ram_write(self, MAR, MDR):
        """Write value to address"""
        # MAR = Memory Address Register, contains the address that is being read or written to
        # MDR =  Memory Data Register, contains the data that was read or the data to write
        self.ram[MAR] = MDR
