import sys
import json
from PIL import Image
from ninepatch import Ninepatch
import importlib.metadata


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=importlib.metadata.version('ninepatch'))

    subparsers = parser.add_subparsers(dest='command')

    parser_render = subparsers.add_parser('render', help='render the 9patch to an image')
    parser_render.add_argument('source_filename', help='filename of the ninepatch image')
    parser_render.add_argument('width', type=int)
    parser_render.add_argument('height', type=int)
    parser_render.add_argument('target_filename', nargs='?', help='filename or empty to open the viewer')

    parser_slice = subparsers.add_parser('slice', help='slice the 9patch into tiles and save them into a directory')
    parser_slice.add_argument('source_filename', help='filename of the ninepatch image')
    parser_slice.add_argument('target_path', help='the directory where the slices should be saved')

    parser_info = subparsers.add_parser('info', help='describe the marks in the 9patch using a JSON object')
    parser_info.add_argument('source_filename', help='filename of the ninepatch image')

    parser_fit = subparsers.add_parser('fit', help='render the 9patch to fit given dimension')
    parser_fit.add_argument('source_filename', help='filename of the ninepatch image')
    parser_fit.add_argument('width', type=int)
    parser_fit.add_argument('height', type=int)
    parser_fit.add_argument('target_filename', nargs='?', help='filename or empty to open the viewer')

    parser_wrap = subparsers.add_parser('wrap', help='render the 9patch around existing image')
    parser_wrap.add_argument('source_filename', help='filename of the ninepatch image')
    parser_wrap.add_argument('wrapped_filename', help='filename of the image to wrap inside a ninepatch')
    parser_wrap.add_argument('target_filename', nargs='?', help='filename or empty to open the viewer')

    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    if args.command == 'render':
        ninepatch = Ninepatch(args.source_filename)
        scaled_image = ninepatch.render(args.width, args.height)
        if args.target_filename:
            scaled_image.save(args.target_filename)
        else:
            scaled_image.show()

    elif args.command == 'slice':
        ninepatch = Ninepatch(args.source_filename)
        ninepatch.export_slices(args.target_path)

    elif args.command == 'info':
        ninepatch = Ninepatch(args.source_filename)
        sys.stdout.write('%s\n' % json.dumps({'marks': ninepatch.marks, 'size': ninepatch.image_size}, indent=4, sort_keys=True))

    elif args.command == 'fit':
        ninepatch = Ninepatch(args.source_filename)
        scaled_image = ninepatch.render_fit(args.width, args.height)
        if args.target_filename:
            scaled_image.save(args.target_filename)
        else:
            scaled_image.show()

    elif args.command == 'wrap':
        ninepatch = Ninepatch(args.source_filename)
        image = Image.open(args.wrapped_filename)
        scaled_image = ninepatch.render_wrap(image)
        if args.target_filename:
            scaled_image.save(args.target_filename)
        else:
            scaled_image.show()


if __name__ == "__main__":
    main()
