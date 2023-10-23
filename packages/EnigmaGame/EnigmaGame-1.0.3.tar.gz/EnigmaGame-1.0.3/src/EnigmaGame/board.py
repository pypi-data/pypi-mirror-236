
import random
import time
from enum import Enum

import EnigmaGame.const as const
from EnigmaGame.blocks import Blocks
from EnigmaGame.figure import Figure


class Disc(Enum):
    LOWER = 0
    UPPER = 1


class Direction(Enum):
    RIGHT = 0
    LEFT = 1


class Board:

    def __init__(self):

        self.numTurns = 20
        self.bShowTurns = False
        self.level = 1
        self.startTime = None

        self.upperCenterX = 116.60
        self.upperCenterY = 200
        self.lowerCenterX = 116.60
        self.lowerCenterY = 100

        self.moves = []
        self.gameActive = False
        self.gameMoves = 0
        self.gameSuccess = False

        self.upperBones = []
        self.lowerBones = []
        self.upperStones = []
        self.lowerStones = []

        self.stones = []
        self.bones = []
        self.frame = None

        self.w = 230
        self.h = 300

        self.init_board()

    def init_board(self):
        self.numTurns = 20
        self.bShowTurns = False

        self.gameActive = False
        self.moves = []
        self.gameMoves = 0

        self.upperBones = [0] * 6
        self.lowerBones = [0] * 6
        self.upperStones = [0] * 6
        self.lowerStones = [0] * 6

        self.stones = []
        for i in range(0, 10):
            self.stones.append(Figure())

        self.bones = []
        for i in range(0, 11):
            self.bones.append(Figure())

        self.frame = Figure()

        Blocks.color_blocks(self.level)

        self.bones[0].add_block(28)
        self.bones[0].add_block(29)

        for i in range(1, 6):
            self.bones[i].add_block(5 * (i - 1) + 3)
            self.bones[i].add_block(5 * (i - 1) + 4)

        for i in range(0, 6):
            self.stones[i].add_block(5 * i)
            self.stones[i].add_block(5 * i + 1)
            self.stones[i].add_block(5 * i + 2)

        for i in range(6, 11):
            self.bones[i].add_block(5 * i)
            self.bones[i].add_block(5 * i + 1)

        for i in range(6, 10):
            self.stones[i].add_block(5 * i + 2)
            self.stones[i].add_block(5 * i + 3)
            self.stones[i].add_block(5 * i + 4)

        for i in range(0, 12):
            self.frame.add_block(i + 52)

        for i in range(0, 6):
            self.upperBones[i] = i
            self.lowerBones[i] = i + 5
            self.upperStones[i] = i
            self.lowerStones[i] = i + 4

        self.upperCenterX = 116.60
        self.upperCenterY = 200
        self.lowerCenterX = 116.60
        self.lowerCenterY = 100

        self.w = 230
        self.h = 300

    def on_resize(self, w, h):
        dx = 1.0 * w / self.w
        dy = 1.0 * h / self.h

        Blocks.scale_blocks(dx)

        self.upperCenterX = self.upperCenterX * dx
        self.upperCenterY = self.upperCenterY * dy
        self.lowerCenterX = self.lowerCenterX * dx
        self.lowerCenterY = self.lowerCenterY * dy

        self.h = h
        self.w = w

    def get_middle_x(self):
        return (self.upperCenterX + self.lowerCenterX) / 2.0

    def get_middle_y(self):
        return (self.upperCenterY + self.lowerCenterY) / 2.0

    def get_runtime(self):
        return int(time.time() - self.startTime)

    def get_turns(self):
        return len(self.moves) - self.gameMoves

    def on_draw(self):
        self.draw_background()
        self.draw_upper_disk()
        self.draw_lower_disk()

    def draw_background(self):
        self.frame.draw()

    def draw_upper_disk(self):

        for i in range(0, 6):
            self.bones[self.upperBones[i]].draw()
            self.stones[self.upperStones[i]].draw()
            pass

    def draw_lower_disk(self):
        for i in range(0, 6):
            self.bones[self.lowerBones[i]].draw()
            self.stones[self.lowerStones[i]].draw()
            pass

    def turn_disc(self, direction: Direction, disc: Disc):
        new_bones = [0] * 6
        new_stones = [0] * 6

        self.moves.append([direction, disc])

        if disc == Disc.UPPER:
            if direction == Direction.LEFT:
                for i in range(0, 6):
                    if self.upperStones[i] >= 6:
                        self.stones[self.upperStones[i]].inc_orient()

                    idx = i + 5
                    if idx > 5:
                        idx -= 6

                    new_bones[idx] = self.upperBones[i]
                    new_stones[idx] = self.upperStones[i]

            else:
                for i in range(0, 6):
                    if self.upperStones[i] >= 6:
                        self.stones[self.upperStones[i]].dec_orient()

                    idx = i - 5
                    if idx < 0:
                        idx += 6
                    new_bones[idx] = self.upperBones[i]
                    new_stones[idx] = self.upperStones[i]

            for i in range(0, 6):
                self.upperBones[i] = new_bones[i]
                self.upperStones[i] = new_stones[i]

            self.lowerBones[0] = self.upperBones[5]
            self.lowerStones[0] = self.upperStones[4]
            self.lowerStones[1] = self.upperStones[5]
        else:
            if direction == Direction.RIGHT:
                for i in range(0, 6):
                    if self.lowerStones[i] < 6:
                        self.stones[self.lowerStones[i]].inc_orient()

                    idx = i + 5
                    if idx > 5:
                        idx -= 6
                    new_bones[idx] = self.lowerBones[i]
                    new_stones[idx] = self.lowerStones[i]
            else:
                for i in range(0, 6):
                    if self.lowerStones[i] < 6:
                        self.stones[self.lowerStones[i]].dec_orient()

                    idx = i - 5
                    if idx < 0:
                        idx += 6

                    new_bones[idx] = self.lowerBones[i]
                    new_stones[idx] = self.lowerStones[i]

            for i in range(0, 6):
                self.lowerBones[i] = new_bones[i]
                self.lowerStones[i] = new_stones[i]

            self.upperBones[5] = self.lowerBones[0]
            self.upperStones[4] = self.lowerStones[0]
            self.upperStones[5] = self.lowerStones[1]

        if self.gameActive:
            s0 = self.get_color_string()
            s1 = Blocks.get_color_string()
            if s0 == s1:
                self.gameActive = False
                self.gameSuccess = True

    def rotate_disc(self, direction: Direction, disc: Disc, deg):
        if disc == Disc.UPPER:
            if direction == Direction.RIGHT:
                deg = -deg
            self.rotate(self.upperBones, self.upperStones, self.upperCenterX, self.upperCenterY, deg)
        else:
            if direction == Direction.RIGHT:
                deg = -deg
            self.rotate(self.lowerBones, self.lowerStones, self.lowerCenterX, self.lowerCenterY, deg)

    def rotate(self, bones, stones, cx, cy, deg):
        for i in range(0, 6):
            self.bones[bones[i]].rotate(deg, cx, cy)
            self.stones[stones[i]].rotate(deg, cx, cy)

    def get_color_string(self):
        sb = ""
        for i in range(0, 5):
            sb = sb + self.stones[self.upperStones[i]].get_color_string()
            sb = sb + self.bones[self.upperBones[i + 1]].get_color_string()

        sb = sb + self.stones[self.upperStones[5]].get_color_string()
        sb = sb + self.bones[self.upperBones[0]].get_color_string()

        sb = sb + self.bones[self.lowerBones[1]].get_color_string()
        for i in range(2, 6):
            sb = sb + self.stones[self.lowerStones[i]].get_color_string()
            sb = sb + self.bones[self.lowerBones[i]].get_color_string()

        return sb

    def get_level(self):
        return const.LEVELS[self.level]

    def level_up(self):
        if self.level == 10:
            return

        self.level = self.level + 1
        self.gameActive = False
        self.gameSuccess = False
        self.init_board()

    def level_down(self):
        if self.level == 0:
            return

        self.level = self.level - 1
        self.gameActive = False
        self.gameSuccess = False
        self.init_board()

    def new_game(self):
        self.init_board()

        self.numTurns = 20
        self.bShowTurns = False
        self.gameActive = False
        self.gameSuccess = False
        self.moves = []
        self.gameMoves = 0
        self.startTime = time.time()

        for i in range(0, self.numTurns):
            direction = Direction.RIGHT
            disc = Disc.UPPER
            if i % 2 == 0:
                disc = Disc.LOWER

            anz = random.randint(1, 6)
            if anz > 3:
                direction = Direction.LEFT
                anz = anz - 3

            self.gameMoves += anz

            for j in range(0, anz):
                self.turn_disc(direction, disc)
                self.rotate_disc(direction, disc, 60.0)
                if self.bShowTurns:
                    pass

        s = self.get_color_string()
        s1 = Blocks.get_color_string()
        if s == s1:
            self.turn_disc(Direction.RIGHT, Disc.LOWER)
            self.rotate_disc(Direction.RIGHT, Disc.LOWER, 60.0)
            self.turn_disc(Direction.RIGHT, Disc.LOWER)
            self.rotate_disc(Direction.RIGHT, Disc.LOWER, 60.0)
            self.turn_disc(Direction.RIGHT, Disc.LOWER)
            self.rotate_disc(Direction.RIGHT, Disc.LOWER, 60.0)

            self.turn_disc(Direction.LEFT, Disc.UPPER)
            self.rotate_disc(Direction.LEFT, Disc.UPPER, 60.0)
            self.turn_disc(Direction.LEFT, Disc.UPPER)
            self.rotate_disc(Direction.LEFT, Disc.UPPER, 60.0)
            self.turn_disc(Direction.LEFT, Disc.UPPER)
            self.rotate_disc(Direction.LEFT, Disc.UPPER, 60.0)

            self.gameMoves += 6

        self.gameActive = True

    def color_blocks(self):
        for i in range(0, 64):
            Blocks.blocks[i].col = random.randrange(0, 7)
