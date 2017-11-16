class lpu_video:
    def __init__(self, mem):
        self.mem = mem
        self.buffer = "" 
        for y in range(32):
            for x in range(64):
                self.buffer += " "
            self.buffer += "\n"

    def draw_buffer(self):
        print(self.buffer)

    def redraw(self):
        '''Get the data from memory and create a buffer for it'''
        current = 0xF7F
        end = 0xFFF
        self.buffer = ""
        while current < end:
            data = self.mem.get(current)
            data = str(bin(data))[2:].zfill(16)
            self.buffer += data
            t = self.buffer.replace("\n", "")
            if (len(t) % 64) == 0:
                self.buffer += "\n"
            current += 1
        self.buffer = self.buffer.replace("0", ".").replace("1", "x")
