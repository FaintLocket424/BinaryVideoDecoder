# Binary Video Decoder

**Written by Matthew Peters**.

This is a simple python program which converts a very specific binary file format into a series of images and/or a video file for viewing.

This takes the guesswork out of trying to see if your video transformations are actually working.

#### Standard gif output: 

![](assets/gif_output.gif)

#### Compare gif output (comparing the same file):

![](assets/gif_compare.gif)

## How to Run
1. Download the [latest release](https://github.com/FaintLocket424/BinaryVideoDecoder/releases/latest)
2. Requires the `opencv` and `pillow` conda packages. Alternatively, you can `pip install -r requirements.txt` which will pip install the necessary dependencies.
3. To run the program, simply run `python.exe main.py`

## Optional Flags

- You may use `--frames` for the program to output all the frames as PNG files instead of a video.
- You may use `--bin [path]` to specify a path for the input binary file.
- You may use `--codec [mp4|avi|gif]` to select between an MP4, AVI or GIF video output. Without this, the output will be GIF.
- You may use `--compare [path]` to specify the path for another video which will be put next to the first for comparison
- You may use `--overwrite` to save the video/images in a single folder, rather than in subfolder of the date.
- You may use `--scale [factor]` to scale the output images/videos
- You may use `--skipupdate` to skip running the update checker.
- You may use `--out [path]` to redirect the output to a folder of your choice
- You may use `--named` to suffix the output with the input file name
- You may use `--prompt` to prompt for the input binary file path in the console
