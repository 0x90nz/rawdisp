#!/usr/bin/env python3
import sys
import argparse
import pathlib
from PIL import Image

scaling_methods = ['nearest', 'box',
                   'bilinear', 'hamming', 'bicubic', 'lanczos']


def error(msg):
    print(msg, file=sys.stderr)
    exit(1)


def read_file_bytes(file: pathlib.Path) -> bytes:
    with open(file, 'rb') as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(
        description='CLI application to display raw image data')
    parser.add_argument('-s', dest='scalefactor', metavar='FACTOR', type=int,
                        help='factor (e.g. 2 for 2x) to scale the image by')
    parser.add_argument('-m', dest='scalemode', help='the method by which to scale, ignored if --scale-by not present',
                        choices=scaling_methods, default='box')
    parser.add_argument('-k', dest='skip', metavar='SKIP', type=int,
                        help='number of bytes to skip before interpreting image data')
    parser.add_argument('-f', dest='mode', choices=Image.MODES,
                        help='the format which the data is in', default='1')
    parser.add_argument('width', type=int,
                        help='the width to display the image at')
    parser.add_argument('height', type=int,
                        help='the height to display the image at')
    parser.add_argument('file', type=pathlib.Path, help='the file to read')

    args = parser.parse_args()

    if not args.file.exists():
        error(f'File {args.file} does not exist')

    data = read_file_bytes(args.file)
    if args.skip is not None:
        data = data[args.skip:]

    img = Image.frombytes(args.mode, (args.width, args.height), data)
    if args.scalefactor is not None:
        img = img.resize((img.width * args.scalefactor, img.height * args.scalefactor),
                         getattr(Image, args.scalemode.upper()))
    img.show()


if __name__ == '__main__':
    main()
