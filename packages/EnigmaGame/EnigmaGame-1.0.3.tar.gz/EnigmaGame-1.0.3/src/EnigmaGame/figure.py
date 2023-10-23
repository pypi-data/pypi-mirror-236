
from EnigmaGame.blocks import Blocks


class Figure:
    def __init__(self):
        self.blocks = []
        self.orient = 0  # 1 = 60, 2 = 120 Grad

    def inc_orient(self):
        self.orient = (self.orient + 1) % 3

    def dec_orient(self):
        self.orient = self.orient - 1
        if self.orient < 0:
            self.orient = self.orient + 3

    def add_block(self, nr: int):
        self.blocks.append(Blocks.blocks[nr])

    def draw(self):
        for block in self.blocks:
            block.draw()

    def get_color_string(self):
        cs = ""
        for i in range(len(self.blocks)):
            idx = (i + self.orient) % 3
            cs = cs + str(self.blocks[idx].col)

        return cs

    def rotate(self, a, x, y):
        for block in self.blocks:
            block.rotate(a, x, y)
