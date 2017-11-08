#!/usr/bin/python3
import sys
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="Enable debugging", action="store_true")
parser.add_argument("-s", "--speed", type=int, default=100, help="Operations Per Second")
parser.add_argument("rom", help="The ROM to load")

args = parser.parse_args()

VERSION = "0.1"
DEBUG = args.debug
SPEED = args.speed
WIDTH = 16

debug_output = ""

if DEBUG:
    print("LPU v" + VERSION);

MEMSIZE = 4096

# INIT the registers
pc = 0
ir = 0
addr = 0
a = 0

# INIT Memory to be 0
mem = []

# Load the rom.
ROM = args.rom

try:
    with open(ROM, 'rb') as in_rom:
        while True:
            data = in_rom.read(2);
            if data == b'':
                break;
            mem.append(data.hex());
except:
    print("Rom not found")
    sys.exit(-1)

if DEBUG:
    print(mem);

def print_debug(op):
    global debug_output, pc, ir, addr, a
    print("OUT: " + debug_output)
    print("State OP: " + hex(op) 
            + " PC: " + hex(pc) 
            + " IR: " + hex(ir) 
            + " ADDR: " + hex(addr) 
            + " A: " + str(a));
    if not args.speed:
        input()

def fetch():
    global pc, ir
    ir = int(mem[pc], 16)
    pc += 1
    if pc >= 4096:
        pc = 0;

def execute():
    global debug_output, pc, ir, addr, a
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
        # JMA IF A is ZERO...
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
        out = int(a, 16)
        if not DEBUG:
            print(chr(out), flush=True, end='')
        else:
            debug_output += chr(out)
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
        print("\nHLT Called\n")
        sys.exit()
    time.sleep(1.0/SPEED)

while(1):
    fetch();
    execute();
