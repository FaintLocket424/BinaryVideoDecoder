import argparse
import os
import struct
import time
from argparse import Namespace
from typing import BinaryIO

import numpy as np
from numpy import ndarray

from BColours import BColours
from saving import save_images, save_video
from update_checker import check_latest_version

current_version: str = "v1.2.1"


def get_args() -> Namespace:
    parser = argparse.ArgumentParser(description='Optional app description')

    parser.add_argument('--frames', action='store_true',
                        help="When enabled, program will output the individual frames")
    parser.add_argument('--bin', type=str, nargs=1, help="path to input binary file. Defaults to 'out.bin'")
    parser.add_argument('--codec', type=str, nargs=1,
                        help="The video extension to use, AVI, MP4 or GIF. Defaults to MP4")
    parser.add_argument('--compare', type=str, nargs=1,
                        help="Specify a path to another binary which will be put beside the first binary in the output.")
    parser.add_argument('--overwrite', action='store_true',
                        help="when enabled, videos/images will not be stored in subfolders of the time")
    parser.add_argument('--scale', type=float, nargs=1, help="A scale factor by which all outputs will be scaled by.")
    parser.add_argument('--skipupdate', action='store_true',
                        help="When enabled, the program will skip checking for an update.")
    parser.add_argument('--out', type=str, nargs=1, help="redirect the output")

    return parser.parse_args()


def get_file_information(_file: BinaryIO) -> (int, int, int, int):
    print(f"Reading data for {_file.name}")
    _num_of_frames: int = struct.unpack('<Q', _file.read(8))[0]
    _num_of_channels: int = struct.unpack('B', _file.read(1))[0]
    _height: int = struct.unpack('B', _file.read(1))[0]
    _width: int = struct.unpack('B', _file.read(1))[0]

    print(f"Number of frames: {_num_of_frames}")
    print(f"Number of channels: {_num_of_channels}")
    print(f"Height: {_height}")
    print(f"Width: {_width}")
    print()

    return _num_of_frames, _num_of_channels, _width, _height


def read_bin() -> ndarray:
    _filename = args.bin[0] if args.bin else "test.bin"

    if not os.path.exists(_filename):
        print(f"{BColours.FAIL}The specified input file does not exist: {_filename}", end='')
        if not args.bin:
            print("\nTry adding --bin [path] to the command to specify a new input file like `py main.py --bin tests/out.bin`")

        print(BColours.ENDC)
        exit(1)

    _compare_file_name: str | None = None
    _compare_file: (BinaryIO | None) = None

    if args.compare:
        _compare_file_name = args.compare[0]

        if not os.path.exists(_compare_file_name):
            print(f"{BColours.FAIL}The specified compare input file does not exist: {_compare_file_name}")
            print("To specify the compare file, use --compare [path] e.g. `py main.py --compare out.bin`", end='')
            print(BColours.ENDC)
            exit(1)

        _compare_file = open(_compare_file_name, 'rb')

    with open(_filename, 'rb') as _file:
        _src_number_of_frames, _src_number_of_channels, _src_width, _src_height = get_file_information(_file)

        if _compare_file:
            _comp_number_of_frames, _comp_number_of_channels, _comp_width, _comp_height = get_file_information(
                _compare_file)

        _output_width = _src_width + _comp_width if _compare_file else _src_width

        _data = np.zeros((_src_number_of_frames, _output_width, _src_height, _src_number_of_channels), np.uint8)

        for frame in range(_src_number_of_frames):
            for c in range(_src_number_of_channels):
                for x in range(_output_width):
                    for y in range(_src_height):
                        if _compare_file and x >= _src_width:
                            _pixel = struct.unpack('B', _compare_file.read(1))[0]
                        else:
                            _pixel = struct.unpack('B', _file.read(1))[0]

                        _data[frame][x][y][c] = _pixel

    if _compare_file:
        _compare_file.close()

    return _data


if __name__ == "__main__":
    print(f"Running Binary Video Decoder {current_version}")
    print("Written by Matthew Peters, aka @faintlocket424\n")

    args = get_args()

    if not args.skipupdate:
        check_latest_version(current_version)

    data = read_bin()

    _, height, width, _ = data.shape

    out_folder = args.out[0] if args.out else "out"
    out_path = out_folder if args.overwrite else os.path.join(out_folder, "out-" + str(int(time.time())))

    if not os.path.exists(out_path):
        if args.out:
            print(f"{BColours.WARNING}The specified output path does not exist: {out_path}")
            print(f"Creating directory {out_path}", end='')
            print(BColours.ENDC + '\n')
        os.makedirs(out_path, exist_ok=True)

    if args.overwrite:
        output_dir_contents = os.listdir(out_path)
        only_files = [f for f in output_dir_contents if os.path.isfile(os.path.join(out_path, f))]
        for _file in [f for f in only_files if f.startswith("video.")]:
            os.remove(os.path.join(out_path, _file))

    scale_factor = args.scale[0] if args.scale else 1

    if args.frames:
        save_images(data, out_path, scale_factor)

    if not args.frames:
        codec: str = args.codec[0] if args.codec else 'MP4'
        save_video(data, codec, out_path, width, height, scale_factor)

    print("Finished.")
