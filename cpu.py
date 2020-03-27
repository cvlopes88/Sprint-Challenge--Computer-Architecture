import sys


LDI = 0b10000010 
PRN = 0b01000111 
HLT = 0b00000001 
MUL = 0b10100010 
POP = 0b01000110 
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
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
    # self.reg[SP] = 0xF4
    # Flags register
    self.fl = False
    self.branchtable = {}
    self.branchtable[LDI] = self.handle_LDI
    self.branchtable[PRN] = self.handle_PRN
    self.branchtable[HLT] = self.handle_HLT
    self.branchtable[MUL] = self.handle_MUL
    self.branchtable[POP] = self.handle_POP
    self.branchtable[PUSH] = self.handle_PUSH
    self.branchtable[CALL] = self.handle_CALL
    self.branchtable[RET] = self.handle_RET
    self.branchtable[ADD] = self.handle_ADD
    self.branchtable[CMP] = self.handle_CMP
    self.branchtable[JMP] = self.handle_JMP
    self.branchtable[JEQ] = self.handle_JEQ
    self.branchtable[JNE] = self.handle_JNE
    
    
  def load(self, datas):
        """Load a program into memory."""
        # Error handling
        if len(sys.argv) != 2:
            print("usage: ls8.py filename")
            sys.exit(1)
            
        
        address = 0
        
        
        try:
            with open(datas) as p:
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


  def alu(self, op, reg_a, reg_b=None):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            # Multiply the values in two registers together and store the result in registerA
        elif op == "MUL":  
            self.reg[reg_a] *= self.reg[reg_b]
            # Compare the values in two registers.
        elif op == "CMP":  
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = True
                # Jump to the address stored in the given register.
        elif op == "JMP":  
            self.pc = self.reg[reg_a]

        # If equal flag is set (true), jump to the address stored in the given register.
        elif op == "JEQ":
            if self.fl is True:
                self.pc = self.reg[reg_a]
            else:
                self.pc += 2

        # If E flag is clear (false, 0), jump to the address stored in the given register.
        elif op == "JNE":
            if self.fl is False:
                self.pc = self.reg[reg_a]
            else:
              self.pc += 2
        else:
            raise Exception("Unsupported ALU operation")

  def handle_LDI(self):  # sets a specified register to a specified value
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        self.reg[operand_a] = operand_b
        self.pc += 3  # skip down 3 to PRN

  def handle_PRN(self): # prints the numeric value stored in a register
        operand_a = self.ram_read(self.pc + 1) 

        print("printing>>", self.reg[operand_a])
        self.pc += 2 #skip down 2 to HLT

  def handle_MUL(self): # Multiply the values in two registers together and store the result in registerA
        operand_a = self.ram_read(self.pc + 1) 
        operand_b = self.ram_read(self.pc + 2)

        self.alu("MUL", operand_a, operand_b) #call the alu.mul and use operand_a and operand_b
        self.pc += 3 #increment the program counter 3
    
  def handle_ADD(self): # Add the value in two registers and store the result in registerA.
        operand_a = self.ram_read(self.pc + 1) 
        operand_b = self.ram_read(self.pc + 2)

        self.alu("ADD", operand_a, operand_b)
        self.pc += 3

  def handle_CMP(self):
        operand_a = self.ram_read(self.pc + 1) 
        operand_b = self.ram_read(self.pc + 2)

        self.alu("CMP", operand_a, operand_b)
        self.pc += 3


  def handle_HLT(self):
        sys.exit(0) #exit without an error unlike sys.exit 1 which means an error

  def handle_POP(self):
        reg = self.ram_read(self.pc +1)
        value = self.ram_read(self.reg[SP]) #calls memory and gets the F5 value
        #Copy the value
        self.reg[reg] = value
        #increment the stack pointer
        self.reg[SP] += 1
        self.pc += 2

  def handle_PUSH(self):
        reg = self.ram_read(self.pc+1)
        value = self.reg[reg]
        #Decrement the stack pointer
        self.reg[SP] -= 1 
        #Copy the value  in given register to the address pointed to by stack pointer
        self.ram_write(self.reg[SP], value)
        self.pc += 2 #because one argument

  def handle_CALL(self):
        # The address of the instruction directly after CALL is pushed onto the stack.
        # This allows us to return to where we left off when the subroutine finishes executing.
        self.reg[SP] -= 1
        address = self.pc + 2
        self.ram[self.reg[SP]] = address
        # The PC is set to the address stored in the given register.
        # We jump to that location in RAM and execute the first instruction in the subroutine.
        # The PC can move forward or backwards from its current location.
        reg = self.ram_read(self.pc + 1)
        self.pc = self.reg[reg]
        

  def handle_RET(self):
        # Return from subroutine.
        # Pop the value from the top of the stack and store it in the PC.
        self.pc = self.ram[self.reg[SP]]
        self.reg[SP] += 1

  def handle_JMP(self):
        # Jump to the address stored in the given register
        # Set the PC to the address stored in the given register.

        operand_a = self.ram_read(self.pc + 1) 
        self.alu("JMP", operand_a, None) #None we don't need operand_b


  def handle_JEQ(self):
        # If equal flag is set (true), jump to the address stored in the given register.
        operand_a = self.ram_read(self.pc + 1) 

        self.alu("JEQ", operand_a, None) #None we don't need operand_b


  def handle_JNE(self):
        # If E flag is clear (false, 0), jump to the address stored in the given register.
        operand_a = self.ram_read(self.pc + 1) 

        self.alu("JNE", operand_a, None) 


  def run(self):
        """Run the CPU."""
        #load the program
        
        running = True
        
        while True:
            # instruction register
            # read command
            IR = self.ram[self.pc]
            self.branchtable[IR]()
        print("hello")

  def ram_read(self, MAR):  # mar - Memory Address Register
        """Return value stored at address"""
        mdr = self.ram[MAR]  # mdr - Memory Data Register
        return mdr

  def ram_write(self, MAR, MDR):
        """Write value to address"""
        # MAR = Memory Address Register, contains the address that is being read or written to
        # MDR =  Memory Data Register, contains the data that was read or the data to write
        self.ram[MAR] = MDR


def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
           self.pc,
           # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print(trace())
