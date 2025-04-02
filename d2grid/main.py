from settings_model import Settings
from sources import FileSource, AttrSource
from utils import read_data, write_data
from argparse import ArgumentParser
from generator import create_grid


def create_arg_parser() -> ArgumentParser:
    arg_parser = ArgumentParser(description="A configuration-driven script to generate Dota 2 hero grid layouts")
    arg_parser.add_argument("-v", "--version", action="version", version="0.1.0")
    arg_parser.add_argument("filepath", nargs="?", default="settings.json",
                            help="Path to settings file (default: %(default)s)")
    return arg_parser

def main():
    args = create_arg_parser().parse_args()
    settings = read_data(args.filepath, Settings)
    factory = {
        "file": FileSource(settings.file_source),
        "attr": AttrSource(settings.api_key)
    }
    new_grid = create_grid(settings.configs, factory)
    write_data(settings.result_paths, new_grid)

if __name__ == '__main__':
    main()
