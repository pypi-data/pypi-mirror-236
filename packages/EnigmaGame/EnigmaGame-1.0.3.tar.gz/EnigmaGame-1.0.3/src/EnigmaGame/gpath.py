
import copy
import math

import arcade


class GPath:
    def __init__(self):
        self.point_list = []

    def reset(self):
        self.point_list = []

    def add_path(self, gp):
        self.point_list.extend(copy.deepcopy(gp.point_list))

    def add_arc(self, x, y, width, height, start_angle, angle):
        radius_x = width / 2
        radius_y = height / 2

        center_x = x + radius_x
        center_y = y + radius_y
        end_angle = start_angle + angle
        num_segments = 128

        reverse = False
        if start_angle > end_angle:
            reverse = True
            t = start_angle
            start_angle = end_angle
            end_angle = t

        point_list = []

        theta = 2.0 * math.pi * start_angle / 360.0
        x1 = radius_x * math.cos(theta)
        y1 = radius_y * math.sin(theta)
        point_list.append([x1, y1])

        start_segment = int(start_angle / 360 * num_segments)
        end_segment = int(end_angle / 360 * num_segments)

        for segment in range(start_segment + 1, end_segment):
            theta = 2.0 * math.pi * segment / num_segments

            x1 = radius_x * math.cos(theta)
            y1 = radius_y * math.sin(theta)

            point_list.append([x1, y1])

        theta = 2.0 * math.pi * end_angle / 360.0
        x1 = radius_x * math.cos(theta)
        y1 = radius_y * math.sin(theta)
        point_list.append([x1, y1])

        if reverse:
            point_list.reverse()

        for point in point_list:
            self.point_list.append([point[0] + center_x, point[1] + center_y])

    def add_line(self, x1, y1, x2, y2):
        self.point_list.append([x1, y1])
        self.point_list.append([x2, y2])

    def rotate(self, a, x, y):
        for p in self.point_list:
            t = arcade.rotate_point(p[0], p[1], x, y, a)
            p[0] = t[0]
            p[1] = t[1]

    def translate(self, x, y):
        for p in self.point_list:
            p[0] = p[0] + x
            p[1] = p[1] + y

    def scale(self, f):
        for p in self.point_list:
            p[0] = p[0] * f
            p[1] = p[1] * f

    def change(self, h):
        for p in self.point_list:
            p[1] = h - p[1]
