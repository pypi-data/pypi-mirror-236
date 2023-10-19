import argparse
from CPCReady import __version__
from CPCReady import func_run as emulador
from CPCReady import common as cm

def main():
    description = 'CPCReady Run Project in Emulator.'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--project', '-p', help='Project name', default=cm.PWD)
    parser.add_argument('-v', '--version', action='version', version='\nCPCReady - Project ' + __version__)
    parser.add_argument('--emulator', '-e', type=str, required=True, choices=["rvm-web", "rvm-desktop", "m4board"],
                        help='Emulador for testing softwqre')
    args = parser.parse_args()

    if args.project != "":
        emulador.execute(args.project, args.emulator)
    else:
        handle_image_mode(args, parser)


def handle_image_mode(args, parser):
    parser.print_help()


if __name__ == '__main__':
    main()