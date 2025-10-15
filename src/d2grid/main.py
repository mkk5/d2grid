import sys
from argparse import ArgumentParser
from importlib.metadata import version
from d2grid.generator.settings_model import Settings
from d2grid.generator.grid_generator import GridGenerator
from d2grid.sources import FileSource, attr_source, StratzSource, SpectralSource
from d2grid.utils import read_data, write_data, print_schema


def create_arg_parser() -> ArgumentParser:
    arg_parser = ArgumentParser(description="Highly customizable Dota 2 hero grid generator")
    arg_parser.add_argument("-V", "--version", action="version", version=version("d2grid"))
    arg_parser.add_argument("-s", "--schema", action="store_true", help="show settings schema and exit")
    arg_parser.add_argument("filepath", nargs="?", default="settings.json",
                            help="Path to settings file (default: %(default)s)")
    return arg_parser


def main():
    args = create_arg_parser().parse_args()
    if args.schema:
        print_schema(Settings)
        sys.exit(0)

    settings = read_data(args.filepath, Settings)
    new_grid = GridGenerator(
        file=FileSource(settings.globals.file_source),
        attr=attr_source,
        stratz=StratzSource(settings.globals.stratz_api_key),
        spectral=SpectralSource(),
    ).create_grid(settings.configs)
    write_data(settings.result_paths, new_grid)


if __name__ == '__main__':
    main()
