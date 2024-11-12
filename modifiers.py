import numpy as np
from numpy import ndarray


def replace_color(_data: ndarray, _target: list[int], _new: list[int]):
    _frames, _height, _width, _ = _data.shape
    for _frame in range(_frames):
        for _y in range(_height):
            for _x in range(_width):
                if np.array_equal(_data[_frame][_y][_x], _target):
                    _data[_frame][_y][_x] = _new
