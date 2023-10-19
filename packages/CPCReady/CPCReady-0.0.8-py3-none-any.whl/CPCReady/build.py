
import argparse
from CPCReady import __version__
from CPCReady import func_build as build

def main():
    description = 'CPCReady Build a Basic Project.'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--build', '-b', action='store_true', help='Create image Disc')
    parser.add_argument('-v', '--version', action='version', version='\nCPCReady - Build Image ' + __version__)
    
    args = parser.parse_args()

    if args.build:
        build.create()
    else:
        handle_image_mode(args, parser)


def handle_image_mode(args, parser):
    parser.print_help()


if __name__ == '__main__':
    main()
