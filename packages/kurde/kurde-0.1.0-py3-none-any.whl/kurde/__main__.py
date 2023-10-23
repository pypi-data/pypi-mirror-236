import click
from kurde.core import serialize

@click.command()
@click.argument('script', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
def main(script):
    """Simple configuration language based on Python."""
    serialize(script)

if __name__ == '__main__':
    main()
