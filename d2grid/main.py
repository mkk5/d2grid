from argparse import ArgumentParser
from d2grid.generator.settings_model import Settings
from d2grid.generator.grid_generator import GridGenerator
from d2grid.sources import FileSource, AttrSource
from d2grid.utils import read_data, write_data


def create_arg_parser() -> ArgumentParser:
    arg_parser = ArgumentParser(description="A configuration-driven script to generate Dota 2 hero grid layouts")
    arg_parser.add_argument("-v", "--version", action="version", version="0.1.0")
    arg_parser.add_argument("filepath", nargs="?", default="settings.json",
                            help="Path to settings file (default: %(default)s)")
    return arg_parser


def main():
    args = create_arg_parser().parse_args()
    settings = read_data(args.filepath, Settings)
    new_grid = GridGenerator(
        file=FileSource(settings.globals.file_source),
        attr=AttrSource(settings.globals.stratz_api_key),
    ).create_grid(settings.configs)
    write_data(settings.result_paths, new_grid)


if __name__ == '__main__':
    main()
