LPU
===

The Linc Processing Unit, a ~shitty~ simple CPU, based on Caxton Foster's Blue CPU, with a screen inspired by chip 8 tacked on for amusement

* 16 instructions
* 4k memory locations of 2bytes each
* 16bit bus

* A = accumulator (single register)
* m = memory 4k of memory
* pc = program counter
* ir = instruction register


* 0x0 NOP, NO OPERATION
* 0x1 ADD A = A + M[addr]
* 0x2 XOR A = A xor m[addr]
* 0x3 AND A = A and m[addr]
* 0x4 OR  A = A OR m[addr]
* 0x5 NOT A = A NOT 0xFFFF
* 0x6 LDA A = m[addr]
* 0x7 STA m[addr] = A
* 0x8 SRJ A = PC AND 0xFFF, PC = addr ???
* 0x9 JMA if (a AND 0x8000) PC = addr
* 0xA JMP PC = addr
* 0xB INP A = getch()
* 0xC OUT putch(a)
* 0xD RAL if (a AND 0x800) A = A << 1 | 1, else A = A << 1;
* 0xE DRW Draw the screen
* 0xF HLT Halt the CPU

0xABCD A = instruction, BCD is data / IR

a cycle is fetch(), then execute()

Fetch
-----
  IR = M[PC]
  
  PC ++
  
  PC &= MEMSIZE-1 , ie it cycles when it reaches 4k

execute
-------
  op = IR >> 2
  
  addr = IR & 0xfff ??????

screen
------

64x32 screen inspired by CHIP-8

Using address space 0xF7F-0xFFF is display which is 128 memory locations of 16 bits to represent the monochrome screen. Call 0xE / DRW to draw the screen.
