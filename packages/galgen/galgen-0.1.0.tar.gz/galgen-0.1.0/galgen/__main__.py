import click
from galgen.init import init_action
from galgen.build import build_action

@click.group
def main():
    """Simple gallery generator."""
    pass

@main.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('-f', '--force', default=False, is_flag=True, help='Overwrite existing files')
def init(path, force):
    """Generate config files."""
    init_action(path, force)

@main.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('-o', '--open', 'show', default=False, is_flag=True, help='Open gallery in the browser')
@click.option('-f', '--force', default=False, is_flag=True, help='Overwrite existing files')
def build(path, force, show):
    """Generate webpage."""
    build_action(path, force, show)

if __name__ == '__main__':
    main()
