import sys

VERSION = "0.1"
DEBUG = True

print("LPU v" + VERSION);

MEMSIZE = 4096

# INIT the registers
pc = 0
ir = 0
addr = 0
a = 0

# INIT Memory to be 0
mem = []
for i in range(0, MEMSIZE-1):
    mem.append(0x0) # NOPs for days

mem[1] = 0x60AA # H LDA A = m[addr] 
mem[2] = 0xC000 # OUT A
mem[3] = 0x60AB # E LDA A = m[addr] 
mem[4] = 0xC000 # OUT A
mem[5] = 0x60AC # L LDA A = m[addr] 
mem[6] = 0xC000 # OUT A
mem[7] = 0xC000 # OUT A
mem[8] = 0x60AD # O LDA A = m[addr] 
mem[9] = 0xC000 # OUT A
mem[10] = 0x60AE # W LDA A = m[addr] 
mem[11] = 0xC000 # OUT A
mem[12] = 0x60AD # O LDA A = m[addr] 
mem[13] = 0xC000 # OUT A
mem[14] = 0x60AF # R LDA A = m[addr] 
mem[15] = 0xC000 # OUT A
mem[16] = 0x60AC # L LDA A = m[addr] 
mem[17] = 0xC000 # OUT A
mem[18] = 0x60B0 # D LDA A = m[addr] 
mem[19] = 0xC000 # OUT A
mem[20] = 0xF000 # HALT


# HELLO WORLD
mem[0xAA] = ord('h')
mem[0xAB] = ord('e')
mem[0xAC] = ord('l')
mem[0xAD] = ord('o')
mem[0xAE] = ord('w')
mem[0xAF] = ord('r')
mem[0xB0] = ord('d')

def print_debug(op):
    global pc, ir, addr, a
    print("State OP: " + str(op) 
            + " PC: " + str(pc) 
            + " IR: " + str(ir) 
            + " ADDR: " + str(addr) 
            + " A: " + str(a));
    input()

def fetch():
    global pc, ir
    ir = mem[pc]
    pc += 1
    if pc > 4096:
        pc = 0;

def execute():
    global pc, ir, addr, a
    op = ir >> 12;
    addr = ir & 0xfff
    if DEBUG:
        print_debug(op)

    if op == 0x0:
        # NOP
        pass
    elif op == 0x1:
        # ADD
        a = a + mem[addr]
    elif op == 0x2:
        # XOR
        a ^= a
    elif op == 0x3:
        #AND
        a &= a
    elif op == 0x04:
        # OR
        a |= a
    elif op == 0x05:
        # NOT
        a = ~a
    elif op == 0x06:
        # LDA
        a = mem[addr]
    elif op == 0x07:
        #STA
        mem[addr] = a
    elif op == 0x08:
        #SRJ
        a = pc & 0xFFFF
        pc = addr
    elif op == 0x09:
        # JMA
        if a & 0x8000:
            pc = addr
    elif op == 0x0A:
        #JMP
        pc = addr
    elif op == 0x0B:
        #INP
        a = 'x'
    elif op == 0x0C:
        #OUT
        print(chr(a))
    elif op == 0x0D:
        #RAL
        if (a & 0x8000):
            a = a << 1 | 1
        else:
            a = a << 1
    elif op == 0x0E:
        #CSA
        a = cs
    elif op == 0x0F:
        #HLT
        print("HLT Called\n")
        sys.exit()

while(1):
    fetch();
    execute();
