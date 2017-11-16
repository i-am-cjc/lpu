class lpu_memory():
    def __init__(self, size, rom):
        self.mem = []
        with open(rom, 'rb') as in_rom:
            while True:
                data = in_rom.read(2)
                if data == b'':
                    break
                self.mem.append(int.from_bytes(data, byteorder='big'))
            while len(self.mem) < size:
                self.mem.append(0x0000)
            self.mem

    def set(self, addr, value):
        self.mem[addr] = value

    def get(self, addr):
        return self.mem[addr]
