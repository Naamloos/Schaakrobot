from Robot.UR.URRobot import URRobot


class Constants:
    ROBOT_HOST = '192.168.0.12'
    ROBOT = URRobot(ROBOT_HOST)
    MAGNET_IO = 8
