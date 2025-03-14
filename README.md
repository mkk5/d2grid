# Hero Grid Generator

A configuration-driven script to generate and manage Dota 2 hero grid layouts.

## Example configuration

Example `settings.json` file:

```json
{
    "api_key": "STRATZ API KEY",
    "file_source": "hero_grid_config.json",
    "result_path": "new_hero_grid_config.json",
    "configs": [
        {
            "name": "Main Grid",
            "columns": [
                { "x": 0.0, "width": 316.0, "width_heroes": 6 },
                { "x": 960, "width": 214, "width_heroes": 4 }
            ],
            "row_gap": 21.5,
            "categories": [
                { "name": "Strength", "source": "attr", "param": "str" },
                { "name": "Universal", "source": "attr", "param": "all" },
                { "name": "MyCustom", "source": "file", "param": {"config": "Fav", "category": 4} }
            ]
        }
    ]
}
```

The script will create `new_hero_grid_config.json` containing a single `Main Grid` layout with three
categories distributed across two columns.

Columns control horizontal layout with automatic vertical sizing based on the number of heroes in each category. The
heroes within each category are determined by the specified [sources and parameters](#sources).

A single settings file can define multiple configs (layouts), each with as many categories as needed.

Besides generating new files, the script can be used to sync hero grids across accounts or update existing layouts
(adjusting a custom category's height if new heroes were added manually, etc.)

## Sources

### File source

Heroes from a category in your existing hero_grid_config.json file.

**Param**:

- `config`: name (string) or index (integer) of config
- `category`: name (string) or index (integer) of category

**Requires**: `file_source` in settings

> [!NOTE]
> Names aren't unique – the first match wins.

### Attribute source

Heroes with the specified primary attribute, sorted alphabetically.

**Param**:

`"str"` | `"agi"` | `"int"` | `"all"`

**Requires**: `api_key` in settings

## Usage

1. Create `settings.json`
2. Run `main.py`

Dota uses hero grid configurations at `<STEAM_PATH>/userdata/<STEAM_ID>/570/remote/hero_grid_config.json`
