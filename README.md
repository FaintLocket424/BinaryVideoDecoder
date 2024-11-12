# Binary Video Decoder

**Written by Matthew Peters**.

This is a simple python program which converts a very specific binary file format into a series of images and/or an MP4 file for viewing.

This takes the guesswork out of trying to see if your video transformations are actually working.

## How to Run
1. Clone the repo to your machine.
2. Requires the `opencv` and `pillow` conda packages. Alternatively, you can `pip install -r requirements.txt` which will pip install the necessary dependencies.
3. To run the program, simply run `python.exe main.py`

## Optional Flags

- You may use `--outframes` for the program to output all the frames as PNG files.
- You may use `--bin [path]` to specify a path for the input binary file.
- You may use `--novideo` to stop the program from outputting a video.
- You may use `--codec [mp4|avi]` to select between an MP4 or AVI video output.
- You may use `--compare [path]` to specify the path for another video which will be put next to the first for comparison
- You may use `--overwrite` to save the video/images in a single folder, rather than in subfolder of the date.