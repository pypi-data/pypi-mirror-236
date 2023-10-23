
import arcade

import EnigmaGame.const as const
from EnigmaGame.gpath import GPath


class Block:
    def __init__(self):
        self.gp = GPath()
        self.col = -1

    def draw(self):
        if len(self.gp.point_list) == 0:
            return

        if 0 <= self.col < len(const.COLORS):
            arcade.draw_polygon_filled(self.gp.point_list, const.COLORS[self.col])

        arcade.draw_polygon_outline(self.gp.point_list, arcade.color.WHITE, 2)

    def rotate(self, a, x, y):
        self.gp.rotate(a, x, y)

    def translate(self, x, y):
        self.gp.translate(x, y)

    def scale(self, f):
        self.gp.scale(f)

    def change(self, h):
        self.gp.change(h)
