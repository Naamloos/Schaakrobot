from time import sleep

import numpy
import copy

from Robot.Positions.PositionController import PositionController
from Robot.UR.Constants import Constants


class MoveController:
    def __init__(self, CAMERA):
        self.CONST = Constants()
        self.positions = PositionController()
        self.CAMERA = CAMERA

    def set_magnet(self, set_bool):
        state = self.CONST.ROBOT.set_io(self.CONST.MAGNET_IO, set_bool)
        sleep(0.7)
        while not state:
            state = self.CONST.ROBOT.set_io(self.CONST.MAGNET_IO, set_bool)
        return state

    def goto_start_point(self):
        self.moveto(self.get_start_point())

    def get_start_point(self):
        coordinate = copy.copy(self.positions.START_POINT)
        height = self.positions.START_HEIGHT
        coordinate.append(height)
        return coordinate

    def goto_capture_point(self):
        self.moveto(self.get_capture_point())

    def get_capture_point(self):
        coordinate = copy.copy(self.positions.CAPTURE_BOX_POINT)
        height = self.positions.LOW_CAPTURE_POINT
        coordinate.append(height)
        return coordinate

    def make_move(self, from_pos, to_pos, capture, robot):
        while True:
            if capture:
                issuccess = self.capture(from_pos, to_pos)
            else:
                issuccess = self.move(from_pos, to_pos)
            x, y = self.CAMERA.convertPosition(to_pos)
            color = self.CAMERA.GetColor(x, y)[0]
            print(color)
            if self.check_move(color, robot):
                return issuccess

    def check_move(self, color, robot):
        result = None
        if robot:
            if color == 'Blue' or color == 'None':
                result = False
            else:
                result = True
        else:
            if color == 'Red' or color == 'None':
                result = False
            else:
                result = True
        return result

    def move(self, from_pos, to_pos):
        self.goto_start_point()
        if self.check_move_done(self.get_start_point()):
            from_coordinate = copy.copy(self.positions.CHESS[from_pos])
            to_coordinate = copy.copy(self.positions.CHESS[to_pos])
            from_coordinate.append(self.positions.START_HEIGHT)
            self.moveto(from_coordinate)
            if self.check_move_done(from_coordinate):
                from_coordinate[2] = self.positions.LOW_BOARD_POINT
                self.moveto(from_coordinate)
                if self.check_move_done(from_coordinate):
                    self.set_magnet(True)
                    from_coordinate[2] = self.positions.MOVABLE_BOARD_POINT
                    self.moveto(from_coordinate)
                    if self.check_move_done(from_coordinate):
                        to_coordinate.append(self.positions.MOVABLE_BOARD_POINT)
                        self.moveto(to_coordinate)
                        if self.check_move_done(to_coordinate):
                            to_coordinate[2] = self.positions.LOW_BOARD_POINT
                            self.moveto(to_coordinate)
                            if self.check_move_done(to_coordinate):
                                self.set_magnet(False)
                                self.goto_start_point()
                                if self.check_move_done(self.get_start_point()):
                                    return True

    def capture(self, from_pos, to_pos):
        self.goto_start_point()
        if self.check_move_done(self.get_start_point()):
            from_coordinate = copy.copy(self.positions.CHESS[from_pos])
            to_coordinate = copy.copy(self.positions.CHESS[to_pos])
            to_coordinate.append(self.positions.START_HEIGHT)
            self.moveto(to_coordinate)
            if self.check_move_done(to_coordinate):
                to_coordinate[2] = self.positions.LOW_BOARD_POINT
                self.moveto(to_coordinate)
                if self.check_move_done(to_coordinate):
                    self.set_magnet(True)
                    to_coordinate[2] = self.positions.MOVABLE_BOARD_POINT
                    self.moveto(to_coordinate)
                    if self.check_move_done(to_coordinate):
                        self.goto_capture_point()
                        if self.check_move_done(self.get_capture_point()):
                            self.set_magnet(False)
                            from_coordinate.append(self.positions.MOVABLE_BOARD_POINT)
                            self.moveto(from_coordinate)
                            if self.check_move_done(from_coordinate):
                                from_coordinate[2] = self.positions.LOW_BOARD_POINT
                                self.moveto(from_coordinate)
                                if self.check_move_done(from_coordinate):
                                    self.set_magnet(True)
                                    from_coordinate[2] = self.positions.MOVABLE_BOARD_POINT
                                    self.moveto(from_coordinate)
                                    if self.check_move_done(from_coordinate):
                                        to_coordinate[2] = self.positions.MOVABLE_BOARD_POINT
                                        self.moveto(to_coordinate)
                                        if self.check_move_done(to_coordinate):
                                            to_coordinate[2] = self.positions.LOW_BOARD_POINT
                                            self.moveto(to_coordinate)
                                            if self.check_move_done(to_coordinate):
                                                self.set_magnet(False)
                                                self.goto_start_point()
                                                if self.check_move_done(self.get_start_point()):
                                                    return True

    def moveto(self, coordinate):
        self.CONST.ROBOT.movel((
            coordinate[0],
            coordinate[1],
            coordinate[2],
            self.positions.CAMERA_POINTS[0],
            self.positions.CAMERA_POINTS[1],
            self.positions.CAMERA_POINTS[2]
        ))

    def check_move_done(self, pos):
        rounded_current_pos = []
        rounded_pos = []

        for p in pos:
            rounded_pos.append(float(str(p)[:-1]))

        while not numpy.array_equal(rounded_pos, rounded_current_pos):
            current_pos = self.CONST.ROBOT.get_tcp_position()
            rounded_current_pos = []
            for r in current_pos[:3]:
                rounded_current_pos.append(float(str(r)[:-1]))

            #sleep(0.5)
            continue

        return True
