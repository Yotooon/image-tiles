#!/usr/bin/python
# -*- coding: latin-1 -*-

"""
The MIT License (MIT)
Copyright (c) 2016 TenSoon

Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the "Software"), to deal 
in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is furnished 
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import re
import os
import sys
import math
import string
import argparse
from PIL import Image

parser = argparse.ArgumentParser(description="Chop up an image into tiles.", usage="tile.py --image <image_path>")
parser.add_argument("-i", "--image", metavar='<path>', type=str, required=True, help="input image")
parser.add_argument("-r", "--init-resize", type=str, required=False, default="", help="resize image before processing (example: 500x500 or 500x to resize width to 500px keeping the aspect ratio)")
parser.add_argument("-t", "--tile-size", type=str, required=False, default="2x2", help="tile size (default: 2x2)")
parser.add_argument("-m", "--overlap-margin", type=int, required=False, default=0, help="tile margin (overlap size, default: 0)")
parser.add_argument("-o", "--output", metavar='<path>', type=str, required=False, default="output", help="output directory")

alpha = string.ascii_lowercase
re_tile_size = re.compile('^(\d+)x(\d+)$')
re_resize = re.compile('^(\d*)x(\d*)$')

def divide(num, times):
	div = int(math.floor(num / times))
	frac = num - (div * times)
	out = [div]*times
	out[-1] = out[-1] + int(frac)

	return out

def add_margins(x, y, w, h, img_size):
	# N
	if y > 0:
		y = max(0, y - args.overlap_margin)
		h = min(img_size[1], h + args.overlap_margin)
	# S
	if (y+h) < img_size[1]:
		h = min(img_size[1], h + args.overlap_margin)
	# E
	if (x+w) < img_size[0]:
		w = min(img_size[0], w + args.overlap_margin)
	# W
	if x > 0:
		x = max(0, x - args.overlap_margin)
		w = min(img_size[0], w + args.overlap_margin)

	return (x, y, x+w, y+h)

def init_resize(img, resize_arg):
	match = re.match(re_resize, resize_arg)
	size = img.size

	if match:
		match = [int(0 if x == '' else x) for x in match.groups()]

		if match[0] > 0 and match[1] > 0:
			new_size = tuple(match)
		elif match[0] == 0 and match[1] > 0:
			r = float(match[1]) / int(size[1])
			new_size = (int(size[0] * r), match[1])
		elif match[0] > 0 and match[1] == 0:
			r = float(match[0]) / int(size[0])
			new_size = (match[0], int(size[1] * r))
		else:
			return img

		return img.resize(new_size, Image.ANTIALIAS)

	else:
		return img

def main(args):
	file_name, ext = os.path.splitext(args.image)
	tile_size = re.match(re_tile_size, args.tile_size)

	img = Image.open(args.image)

	# resize?
	img = init_resize(img, args.init_resize)
	img_w, img_h = img.size

	# check tile size
	if tile_size:
		tile_size = [int(x) for x in tile_size.groups()]
	else:
		print 'ERROR: Invalid tile size.'
		sys.exit(1)

	# check out directory
	if not os.path.isdir(args.output):
		os.mkdir(args.output)

	# start
	img_widths = divide(img_w, tile_size[0])
	img_heights = divide(img_h, tile_size[1])

	print 'Processing %s [%s tile, %spx margin]...' % (args.image, args.tile_size, args.overlap_margin)

	for j in range(len(img_heights)):
		for i in range(len(img_widths)):
			x = sum(img_widths[:i]) if i > 0 else 0
			y = sum(img_heights[:j]) if j > 0 else 0
			w = img_widths[i]
			h = img_heights[j]

			tile = img.crop(add_margins(x, y, w, h, img.size))
			tile.save('%s/%s_%s%s.jpg' % (args.output, file_name, alpha[j], i+1), quality=95)

	print 'All done :-)'

if __name__ == "__main__":
	args = parser.parse_args()
	main(args)
