from settings_model import Settings, ConfigSettings, CategorySettings, ColumnSettings
from sources import FileSource, AttrSource, Category, Config, HeroGrid
from utils import read_data, write_data
from itertools import batched
from argparse import ArgumentParser


def get_category_height(width_px: float, width_heroes: int, heroes_number: int) -> float:
    card_width, card_height, padding2 = (51.304352, 82.608699, 8.695647) # TODO: review & document
    height_heroes = -(-heroes_number//width_heroes) if heroes_number else 1 # div up (min 1)
    height = (card_height*height_heroes+padding2) * width_px / (card_width*width_heroes+padding2)
    return height

def create_category(category_opts: CategorySettings, column_opts: ColumnSettings, y: float, f: dict) -> Category:
    hero_ids = f[category_opts.source].hero_list(category_opts.param)
    height = get_category_height(column_opts.width, column_opts.width_heroes, len(hero_ids))
    return Category(
        category_name=category_opts.name,
        x_position=column_opts.x,
        y_position=y,
        width=column_opts.width,
        height=height,
        hero_ids=hero_ids
    )

def create_config(config_opts: ConfigSettings, f: dict) -> Config:
    columns_opts = config_opts.columns
    row_gap = config_opts.row_gap
    y = 0
    categories = []
    for row_category_opts in batched(config_opts.categories, len(columns_opts)):
        row = [create_category(category_s, column_s, y, f) for category_s, column_s in zip(row_category_opts, columns_opts)]
        y = y + max(c.height for c in row) + row_gap
        categories.extend(row)
    return Config(config_name=config_opts.name, categories=categories)

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
    new_configs = [create_config(config_settings, factory) for config_settings in settings.configs]
    write_data(settings.result_paths, HeroGrid(configs=new_configs))

if __name__ == '__main__':
    main()
