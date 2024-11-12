import argparse
import os
import struct
import time
from typing import BinaryIO

import numpy as np
from PIL import Image as pImg

parser = argparse.ArgumentParser(description='Optional app description')

parser.add_argument('--outframes', action='store_true', help="When enabled, program will output the individual frames")
parser.add_argument('--bin', type=str, nargs=1, help="path to input binary file. Defaults to 'out.bin'")
parser.add_argument('--novideo', action='store_true', help="When enabled, program will not output a video")
parser.add_argument('--codec', type=str, nargs=1, help="The video extension to use, AVI or MP4. Defaults to MP4")
parser.add_argument('--compare', type=str, nargs=1,
                    help="Specify a path to another binary which will be put beside the first binary in the output.")
parser.add_argument('--overwrite', action='store_true', help="when enabled, videos/images will not be stored in subfolders of the time")

args = parser.parse_args()

if args.novideo and not args.outframes:
    print("Program not outputting frames or video. Check your args!")
    exit(0)

if not args.novideo:
    import cv2

frameOutPath = "out" if args.overwrite else os.path.join("out", str(int(time.time())))

if not os.path.exists(frameOutPath):
    os.makedirs(frameOutPath, exist_ok=True)

codec: str = args.codec[0] if args.codec else 'MP4'
if codec.upper() == "MP4":
    videoFileName = os.path.join(frameOutPath, "video.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
elif codec.upper() == "AVI":
    videoFileName = os.path.join(frameOutPath, "video.avi")
    fourcc = cv2.VideoWriter_fourcc(*'mjpg')
else:
    print("Invalid media codec selected")
    exit(1)

filename = args.bin[0] if args.bin else "test.bin"

if not os.path.exists(filename):
    print("The specified input file does not exist:")
    print(filename)
    exit(1)

compareFile: BinaryIO = None
if args.compare:
    compareFileName = args.compare[0]
    compareFile = open(compareFileName, 'rb')


def get_file_information(_file):
    print(f"Reading data for {_file.name}")
    _numofframes: int = struct.unpack('<Q', _file.read(8))[0]
    _numofchannels: int = struct.unpack('B', _file.read(1))[0]
    _height: int = struct.unpack('B', _file.read(1))[0]
    _width: int = struct.unpack('B', _file.read(1))[0]

    print(f"Number of frames: {_numofframes}")
    print(f"Number of channels: {_numofchannels}")
    print(f"Height: {_height}")
    print(f"Width: {_width}")

    return _numofframes, _numofchannels, _width, _height


with open(filename, 'rb') as file:
    src_number_of_frames, src_number_of_channels, src_width, src_height = get_file_information(file)

    if compareFile:
        comp_number_of_frames, comp_number_of_channels, comp_width, comp_height = get_file_information(compareFile)

    output_width = src_width + comp_width if compareFile else src_width

    data = np.zeros((src_height, output_width, src_number_of_channels), np.uint8)

    if not args.novideo:
        video = cv2.VideoWriter(videoFileName, fourcc, 10, (output_width, src_height))

    for frame in range(src_number_of_frames):
        for c in range(src_number_of_channels):
            for x in range(output_width):
                for y in range(src_height):
                    if compareFile and x >= src_width:
                        pixel = struct.unpack('B', compareFile.read(1))[0]
                    else:
                        pixel = struct.unpack('B', file.read(1))[0]

                    data[y][x][c] = pixel

        for y in range(src_height):
            for x in range(output_width):
                if (data[y][x] == np.array([0, 0, 0])).all():
                    data[y][x] = [128, 128, 255]

        if args.outframes:
            image = pImg.fromarray(data, 'RGB')

            image.save(os.path.join(frameOutPath, f"frame_{frame:03}.png"), 'PNG')

        if not args.novideo:
            video.write(cv2.cvtColor(data, cv2.COLOR_RGB2BGR))

    if not args.novideo:
        cv2.destroyAllWindows()
        video.release()

print("Finished.")
if compareFile:
    compareFile.close()
