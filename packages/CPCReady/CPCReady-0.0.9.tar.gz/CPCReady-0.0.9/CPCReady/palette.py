
from CPCReady import func_palette as palette
from CPCReady import __version__
import click

@click.command(name="cpcr_palette",help="Extract the color palette of an image")
@click.option("-i", "--image", "image", type=click.STRING, help="Input file name",required=True)
@click.option("-m", "--mode", "mode", type=click.Choice(["0","1","2"]), help="Image Mode (0, 1, 2)",required=True)
@click.version_option(version=__version__)
def main(image, mode):
    if image is None or mode is None:
        show_help()
    else:
        palette.getData(image, mode)

def show_help():
    with click.Context(main) as ctx:
        click.echo(main.get_help(ctx))

if __name__ == "__main__":
    main()
