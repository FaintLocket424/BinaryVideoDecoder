import os
from pickletools import optimize

import cv2 as cv
from PIL import Image as pImg
from numpy import ndarray


def save_images(_data: ndarray, _out_path: str) -> None:
    if not os.path.exists(_out_path):
        os.makedirs(_out_path, exist_ok=True)

    for _frame_num in range(_data.shape[0]):
        _frame = _data[_frame_num]
        image = pImg.fromarray(_frame, 'RGB')
        image.save(os.path.join(_out_path, f"frame_{_frame_num:03}.png"), 'PNG')


def save_video(_data: ndarray, _codec: str, _out_path: str, _width: int, _height: int) -> None:
    if _codec.upper() == "GIF":
        _video_file_name = os.path.join(_out_path, "video.gif")

        images = []

        for _frame in _data:
            images.append(pImg.fromarray(_frame))

        images[0].save(_video_file_name, save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)

        return
    elif _codec.upper() == "MP4":
        _video_file_name = os.path.join(_out_path, "video.mp4")
        _fourcc = cv.VideoWriter_fourcc(*'mp4v')
    elif _codec.upper() == "AVI":
        _video_file_name = os.path.join(_out_path, "video.avi")
        _fourcc = cv.VideoWriter_fourcc(*'mjpg')
    else:
        print("Invalid media codec selected")
        exit(1)

    _video = cv.VideoWriter(_video_file_name, _fourcc, 10, (_width, _height))

    for _frame in _data:
        _video.write(cv.cvtColor(_frame, cv.COLOR_RGB2BGR))

    cv.destroyAllWindows()
    _video.release()
