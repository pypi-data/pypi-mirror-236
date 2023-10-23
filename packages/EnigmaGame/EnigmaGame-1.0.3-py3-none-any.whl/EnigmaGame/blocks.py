
import EnigmaGame.const as const
from EnigmaGame.block import Block


class GameBlocks(object):

    def __init__(self):
        self.blocks = []
        self.init_blocks()

    def init_blocks(self):

        if len(self.blocks) > 0:
            return

        for i in range(0, 64):
            self.blocks.append(Block())

        self.blocks[0].gp.add_arc(6.60, 20.0, 160.0, 160.0, 180.0, 21.32)
        self.blocks[0].gp.add_arc(-80.0, 70.0, 160.0, 160.0, 278.68, 21.32)
        self.blocks[0].gp.add_line(40.0, 80.72, 28.87, 100.0)

        self.blocks[1].gp.add_path(self.blocks[0].gp)
        self.blocks[1].rotate(120.0, 28.87, 100.0)

        self.blocks[2].gp.add_path(self.blocks[1].gp)
        self.blocks[2].rotate(120.0, 28.87, 100.0)

        self.blocks[3].gp.add_arc(6.60, 20.0, 160.0, 160.0, 218.68, -17.36)
        self.blocks[3].gp.add_arc(-80.0, 70.0, 160.0, 160.0, 278.68219, 21.32)
        self.blocks[3].gp.add_arc(6.60254, -80.0, 160.0, 160.0, 120, 21.32)

        self.blocks[4].gp.add_path(self.blocks[3].gp)
        self.blocks[4].gp.rotate(180.0, 43.30, 75.0)

        for i in range(5, 30):
            self.blocks[i].gp.add_path(self.blocks[i - 5].gp)
            self.blocks[i].gp.rotate(60.0, 86.60, 100.0)

        for i in range(30, 35):
            self.blocks[i].gp.add_path(self.blocks[i - 7].gp)
            self.blocks[i].gp.rotate(-60.0, 86.60, 200.0)

        for i in range(35, 52):
            self.blocks[i].gp.add_path(self.blocks[i - 5].gp)
            self.blocks[i].gp.rotate(-60.0, 86.60, 200.0)

        self.blocks[52].gp.add_line(86.60 - 30, 100 - 30, 86.60 + 30, 100 - 30)
        self.blocks[52].gp.add_line(86.60 + 30, 100 - 30, 86.60 + 30, 100 + 30)
        self.blocks[52].gp.add_line(86.60 + 30, 100 + 30, 86.60 - 30, 100 + 30)

        self.blocks[53].gp.add_path(self.blocks[52].gp)
        self.blocks[53].gp.translate(0.0, 100.0)

        self.blocks[54].gp.add_line(6.60, 100, 86.60 - 100, 100)
        self.blocks[54].gp.add_line(86.60 - 100, 100, 86.60 - 50, 100 - 86.60)
        self.blocks[54].gp.add_line(86.60 - 50, 100 - 86.60, 46.60, 30.72)

        self.blocks[55].gp.add_path(self.blocks[54].gp)
        self.blocks[55].gp.rotate(60.0, 86.60, 100.0)

        self.blocks[56].gp.add_path(self.blocks[54].gp)
        self.blocks[56].gp.rotate(120.0, 86.60, 100.0)

        self.blocks[57].gp.add_line(6.60, 200, 86.60 - 100, 200)
        self.blocks[57].gp.add_line(86.60 - 100, 200, 6.60, 150)
        self.blocks[57].gp.add_line(6.60, 150, 24.15, 150)

        self.blocks[58].gp.add_line(24.15, 150, 6.60, 150)
        self.blocks[58].gp.add_line(6.60, 150, 86.60 - 100, 100)
        self.blocks[58].gp.add_line(86.60 - 100, 100, 6.60, 100)

        self.blocks[59].gp.add_path(self.blocks[58].gp)
        self.blocks[59].gp.rotate(180.0, 86.60, 150.0)

        self.blocks[60].gp.add_path(self.blocks[57].gp)
        self.blocks[60].gp.rotate(180.0, 86.60, 150.0)

        self.blocks[61].gp.add_path(self.blocks[54].gp)
        self.blocks[61].gp.rotate(180.0, 86.60, 150.0)

        self.blocks[62].gp.add_path(self.blocks[55].gp)
        self.blocks[62].gp.rotate(180.0, 86.60, 150.0)

        self.blocks[63].gp.add_path(self.blocks[56].gp)
        self.blocks[63].gp.rotate(180.0, 86.60, 150.0)

        for block in self.blocks:
            block.translate(30.0, 0.0)
            block.change(300)

    def color_blocks(self, level):
        self.blocks = []
        self.init_blocks()
        for i in range(0, 64):
            self.blocks[i].col = const.GAMES[level][i]

    def scale_blocks(self, f: float = 1.0):
        for block in self.blocks:
            block.scale(f)

    def translate_blocks(self, x: float = 0.0, y: float = 0.0):
        for block in self.blocks:
            block.translate(x, y)

    def get_color_string(self):
        sb = ""
        for i in range(0, 52):
            sb = sb + str(self.blocks[i].col)
        return sb


# Einzige Instanz von GameBlocks
Blocks = GameBlocks()
