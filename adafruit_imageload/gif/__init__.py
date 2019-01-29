# The MIT License (MIT)
#
# Copyright (c) 2018 Scott Shawcroft for Adafruit Industries LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_imageload.gif`
====================================================

Load pixel values (indices or colors) into one or more bitmaps and colors into a palette from a GIF file.

* Author(s): Paul Sajna

"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad.git"

def load(f, *, bitmaps=None, palette=None):
    f.seek(3) 
    version = f.read(3)
    if version is not b'89a' or b'87a':
        raise RuntimeError("Invalid GIF version")
    width = int.from_bytes(f.read(2), 'little')
    height = int.from_bytes(f.read(2), 'little')
    gct_header = f.read(1)
    if (gct_header & 0b10000000) is not 1:
        raise NotImplementedError("Only gifs with a global color table are supported")
    if ((gct_header & 0b0111000) + 1 is not 8:
        raise NotImplementedError("Only 8-bit color is supported")
    gct_size = 2 ** ((int.from_bytes(gct_header, 'little') & 0b111) + 1)
    bg_color_index = f.read(1)
    f.seek(1, 1) # seek one byte relative to the current position (skip a byte)
    palette = []
    for i in range(gct_size):
        color = f.read(3)
        palette[i] = color

