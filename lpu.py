#!/usr/bin/python3
import sys
import argparse
import time

sys.path.append("./component")
from mem import lpu_memory
from video import lpu_video

parser = argparse.ArgumentParser()
parser.add_argument("-D", "--decompile", help="Decompile the rom rather than running it", action="store_true")
parser.add_argument("-s", "--speed", type=int, default=100, help="Operations Per Second")
parser.add_argument("-S", "--step", help="Step Through", action="store_true")
parser.add_argument("rom", help="The ROM to load")

args = parser.parse_args()

VERSION = "0.1"
SPEED = args.speed
STEP = args.step
DECOMPILE = args.decompile
WIDTH = 16

output = ""

print("LPU v" + VERSION);

MEMSIZE = 4096

# INIT the registers
pc = 0
ir = 0
addr = 0
a = 0

# Load the rom.
ROM = args.rom

mem = lpu_memory(MEMSIZE, ROM)
video = lpu_video(mem)

def decompile(op, addr, pc, ir):
    ops = [ "NOP", "ADD", "XOR", "AND", "OR", "NOT", "LDA", "STA", "SRJ", "JMA", "JMP", "INP", "OUT", "RAL", "DRW", "HLT" ]
    return "[0x" + hex(pc-1)[2:].zfill(3) + "] 0x" + hex(ir)[2:].zfill(4) + " - " + ops[op] + " 0x" + hex(addr)[2:].zfill(3)

def print_debug(op):
    global output, pc, ir, addr, a
    print("OUT: " + output)
    print("State PC: " + hex(pc) 
            + "  OP: " + hex(op)
            + " ADDR: " + hex(addr) 
            + " IR: " + hex(ir) 
            + " A: " + str(a));
    print(decompile(op, addr, pc, ir))

def fetch():
    global pc, ir
    ir = mem.get(pc)
    pc += 1
    if pc >= 4096:
        pc = 0;

def print_screen():
    global video
    video.draw_buffer()

def execute():
    global video, output, pc, ir, addr, a
    op = ir >> 12;
    addr = ir & 0xfff

    if DECOMPILE:
        print(decompile(op, addr, pc, ir))
        if op == 0xF:
            sys.exit()
        return 

    time.sleep(1.0/SPEED)
    if op == 0x0:
        # NOP
        pass
    elif op == 0x1:
        # ADD
        a += mem.get(addr)
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
        a = mem.get(addr)
    elif op == 0x07:
        #STA
        mem.set(addr,a)
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
        output += chr(a)
    elif op == 0x0D:
        #RAL
        if (a & 0x8000):
            a = a << 1 | 1
        else:
            a = a << 1
    elif op == 0x0E:
        # DRW
        video.redraw()
        pass
    elif op == 0x0F:
        #HLT
        print("\nHLT Called\n")
        sys.exit()

    print(chr(27) + "[2J" + chr(27) + "[H")
    print_screen()

    if STEP:
        print_debug(op)
        input()

while(1):
    fetch();
    execute();
