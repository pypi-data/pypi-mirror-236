import datetime
import math
import os

import arcade
import arcade.gui
import pyglet.window

from EnigmaGame.board import Board
from EnigmaGame.board import Direction
from EnigmaGame.board import Disc
import EnigmaGame.const as const


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title, style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS, center_window=True)

        arcade.set_background_color(arcade.color.DIM_GRAY)

        self.scale_factor = height / 1280
        self.board = Board()
        self.turning = 0
        self.coloring = 0
        self.disc = Disc.LOWER
        self.dir = Direction.RIGHT
        self.drag_x = 0
        self.drag_y = 0
        self.drag = False

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        self.time_text = arcade.gui.UILabel(width=240 * self.scale_factor, text=" ", font_size=15 * self.scale_factor)
        self.v_box.add(self.time_text.with_space_around(bottom=30))

        self.moves_text = arcade.gui.UILabel(width=240 * self.scale_factor, text=" ", font_size=15 * self.scale_factor)
        self.v_box.add(self.moves_text.with_space_around(bottom=30 * self.scale_factor))

        self.level_text = arcade.gui.UILabel(width=240 * self.scale_factor, text="Level: " + self.board.get_level(), font_size=15 * self.scale_factor)
        self.v_box.add(self.level_text.with_space_around(bottom=100 * self.scale_factor))

        # Create the buttons
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=240 * self.scale_factor)
        self.v_box.add(start_button.with_space_around(bottom=30 * self.scale_factor))

        level_up_button = arcade.gui.UIFlatButton(text="Level Up", width=240 * self.scale_factor)
        self.v_box.add(level_up_button.with_space_around(bottom=30 * self.scale_factor))

        level_down_button = arcade.gui.UIFlatButton(text="Level Down", width=240 * self.scale_factor)
        self.v_box.add(level_down_button.with_space_around(bottom=30 * self.scale_factor))

        close_button = arcade.gui.UIFlatButton(text="Quit", width=240 * self.scale_factor)
        self.v_box.add(close_button.with_space_around(bottom=30 * self.scale_factor))

        start_button.on_click = self.on_click_start
        close_button.on_click = self.on_click_close
        level_down_button.on_click = self.on_click_level_down_button
        level_up_button.on_click = self.on_click_level_up_button

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x=-80 * self.scale_factor,
                align_y=-300 * self.scale_factor,
                anchor_x="right",
                anchor_y="center_y",
                child=self.v_box)
        )

        self.widget = None

    def on_click_level_down_button(self, event):
        self.board.level_down()
        self.level_text.text = "Level: " + self.board.get_level()
        self.setup()

    def on_click_level_up_button(self, event):
        self.board.level_up()
        self.level_text.text = "Level: " + self.board.get_level()
        self.setup()

    def on_click_start(self, event):
        self.board.new_game()
        self.setup()

    def on_click_close(self, event):
        self.close()

    def setup(self):
        self.board.on_resize(920 * self.scale_factor, 1200 * self.scale_factor)
        self.on_draw()

        image = arcade.get_image(0, 0, int(900 * self.scale_factor), int(1150 * self.scale_factor))
        image.save(f"p1_{self.board.level}.png")
        sprite = arcade.Sprite(filename=f"p1_{self.board.level}.png")

        if self.widget is not None:
            self.manager.remove(self.widget)

        self.widget = arcade.gui.UISpriteWidget(x=870 * self.scale_factor, y=700 * self.scale_factor, width=414 * self.scale_factor, height=540 * self.scale_factor, sprite=sprite)
        self.manager.add(self.widget)
        self.manager.trigger_render()
        os.remove(f"p1_{self.board.level}.png")

    def on_draw(self):
        self.clear()
        self.board.on_draw()
        self.manager.draw()

    def on_update(self, delta_time):
        if self.turning > 0:
            self.board.rotate_disc(self.dir, self.disc, 60 / 4)
            self.turning = self.turning - 1
        else:
            if self.coloring > 0:
                self.board.color_blocks()
                self.coloring = self.coloring - 1
            else:
                if self.board.gameActive or self.board.gameSuccess:
                    rt = self.board.get_runtime()
                    self.time_text.text = "Time: " + str(datetime.timedelta(seconds=rt)).zfill(8)
                    self.manager.trigger_render()

                    self.moves_text.text = "Moves: " + str(self.board.get_turns())

                if self.board.gameSuccess:
                    self.board.gameSuccess = False
                    self.coloring = 20

    def on_key_press(self, key, key_modifiers):
        pass

    def on_key_release(self, key, key_modifiers):
        if not self.board.gameActive:
            return

        if key == arcade.key.LEFT:
            self.dir = Direction.LEFT
            self.disc = Disc.LOWER
            if key_modifiers & arcade.key.MOD_SHIFT:
                self.disc = Disc.UPPER
            self.invoke_turn()

        if key == arcade.key.RIGHT:
            self.dir = Direction.RIGHT
            self.disc = Disc.LOWER
            if key_modifiers & arcade.key.MOD_SHIFT:
                self.disc = Disc.UPPER
            self.invoke_turn()

        if key == arcade.key.UP:
            self.board.level_up()
            self.setup()

        if key == arcade.key.DOWN:
            self.board.level_down()
            self.setup()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        if not self.board.gameActive:
            return

        if self.drag:
            return

        self.drag_x = x
        self.drag_y = y
        self.drag = True

    def on_mouse_release(self, x, y, button, key_modifiers):
        if not self.board.gameActive:
            return

        if self.drag:
            x1 = self.drag_x
            x2 = x
            y1 = self.drag_y
            y2 = y

            self.disc = Disc.UPPER
            self.dir = Direction.LEFT

            if self.drag_y > self.board.get_middle_y():
                self.disc = Disc.UPPER
                cy = self.board.upperCenterY
            else:
                self.disc = Disc.LOWER
                cy = self.board.lowerCenterY

            x1 -= self.board.get_middle_x()
            x2 -= self.board.get_middle_x()

            y1 = -(y1 - cy)
            y2 = -(y2 - cy)

            vx = x2 - x1
            vy = y2 - y1
            if math.sqrt(vx * vx + vy * vy) < 20:
                return

            orient = x1 * y2 - y1 * x2
            if orient > 0:
                self.dir = Direction.RIGHT
            else:
                self.dir = Direction.LEFT

            self.invoke_turn()
            self.drag = False

    def invoke_turn(self):
        if self.turning == 0:
            self.turning = 4
            self.board.turn_disc(self.dir, self.disc)


def main():
    (w, h) = arcade.get_display_size()
    game = MyGame(int(h * 0.9), int(h * 0.9), const.SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == '__main__':
    main()
