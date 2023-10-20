import argparse
from CPCReady import func_sprite as sprites
from CPCReady import __version__

def main():
    description = 'CPCReady Create sprite.'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--image', '-i', help='Image Path', required=True)
    parser.add_argument('--mode', '-m', type=int, default=0, choices=[0, 1, 2], help='Image Mode (0, 1, 2)', required=True)
    parser.add_argument('--out', '-o', help='Folder Path out', required=True)
    parser.add_argument('--height', '-e', type=int, help='Height sprite size', required=True)
    parser.add_argument('--width', '-w', type=int, help='Width sprite size', required=True)
    parser.add_argument('-v', '--version', action='version', version='\nCPCReady - Sprite ' + __version__)
    
    args = parser.parse_args()

    sprites.create(args.image, args.mode, args.out, args.height, args.width)



def handle_image_mode(args, parser):
    parser.print_help()


if __name__ == '__main__':
    main()
