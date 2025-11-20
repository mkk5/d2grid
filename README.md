# D2Grid

A powerful, highly customizable CLI tool for creating and managing your Dota 2 hero grid layouts.

## Features

- Declarative Layouts
- Multiple Data Sources
- Automatic Sizing
- Extensibility (custom sources)
- Update & Sync (across multiple Steam accounts)

## Installation

D2Grid can be installed from [PyPI](https://pypi.org/project/d2grid/):

```shell
# With uv
uv tool install d2grid
```

```shell
# With pipx
pipx install d2grid
```

## Usage

Once installed, run the tool by passing it the path to your [configuration file](#configuration):

```shell
d2grid settings.json
```

Alternatively, you can execute the script without an installation:

```shell
# With uv
uvx d2grid settings.json
```

Or run from the source directly:

```shell
# With uv
uv run -m src.d2grid settings.json
```

```shell
# With python (need to install python and dependencies)
python3 -m src.d2grid settings.json
```

## Configuration

The tool is controlled by a single JSON settings file. Here is an example:

```json
{
    "globals": {
        "file_source": "hero_grid_config.json",
        "stratz_api_key": "STRATZ API KEY"
    },
    "result_paths": ["new_hero_grid_config.json"],
    "configs": [
        {
            "name": "Main Grid",
            "columns": [
                { "x": 0.0, "width": 316.0, "width_heroes": 6 },
                { "x": 960, "width": 214, "width_heroes": 4 }
            ],
            "row_gap": 21.5,
            "categories": [
                {
                    "name": "Strength",
                    "source": "attr",
                    "param": "str"
                },
                {
                    "name": "My Custom List",
                    "source": "inline",
                    "param": [1, 2, 3, 14, 56]
                },
                {
                    "name": "Sync from File",
                    "source": "file",
                    "param": { "config": "Fav", "category": 4 }
                },
                {
                    "name": "15 best supports (10 days)",
                    "source": "stratz",
                    "param": {"top": 15, "days": 10, "positions": ["POSITION_4", "POSITION_5"]}
                },
                {
                    "name": "Spectral.gg Core Meta",
                    "source": "spectral",
                    "param": { "top": 12, "position": "P1" }
                }
            ]
        }
    ]
}
```

The script will create `new_hero_grid_config.json` containing a single `Main Grid` layout with five
categories distributed across two columns.

Columns control the horizontal layout with automatic vertical sizing based on the number of heroes in each category. The
heroes within each category are determined by the specified [sources and parameters](#sources).

A single settings file can define multiple configs (layouts), each with as many categories as needed.

Dota stores its hero grid configuration at `<STEAM_PATH>/userdata/<STEAMID>/570/remote/hero_grid_config.json`, which can
be used as the path for `file_source` or `result_paths`.

The full configuration schema can be printed with the following command:

```shell
d2grid --schema
```

## Sources

Sources are callables that provide a list of hero IDs for a category.

### Inline Source

Directly provides a list of hero IDs. Use this for static categories.

- Source Key: `"inline"`

**Parameters**

The `param` field accepts a simple list of hero IDs (integers).

### File Source

Pulls heroes from a category in an existing `hero_grid_config.json` file. Ideal for syncing or preserving manual edits.
Requires `file_source` to be defined in the `globals` section of your settings.

- Source Key: `"file"`

**Parameters**

The `param` field is an object with the following properties:
  
| Property | Type              | Description                                                                           |
|----------|-------------------|---------------------------------------------------------------------------------------|
| config   | integer \| string | The name (string) or index (integer) of the config to read from. **Required**         |
| category | integer \| string | The name (string) or index (integer) of the category within that config. **Required** |

**Note**: When using string names, the first match found will be used.

### Attribute Source

Pulls heroes based on their primary attribute, sorted alphabetically.

- Source Key: `"attr"`

**Parameters**

The `param` field is a string specifying the attribute. Allowed values are: "str", "agi", "int" or "all".

### Stratz Source

Pulls the best performing heroes over a specified time window using the STRATZ API.
Requires `stratz_api_key` to be defined in the `globals` section of your settings.

- Source Key: `"stratz"`

**Parameters**

The `param` field is an object with the following properties:

| Property   | Type           | Description                                                       |
|------------|----------------|-------------------------------------------------------------------|
| top        | integer        | How many heroes to include in the category. **Required**          |
| sort       | string         | Sort method ("rank" or "winrate"). **Default:** "rank"            |
| days       | integer        | Number of recent days of data to consider (1-30). **Default:** 14 |
| ranks      | array\<string> | Rank brackets to filter by. **Default:** ["IMMORTAL"]             |
| positions  | array\<string> | Positions to filter by. **Default:** [] (all positions)           |
| regions    | array\<string> | Regions to filter by. **Default:** [] (all regions)               |
| game_modes | array\<string> | Game modes to filter by. **Default:** ["ALL_PICK_RANKED"]         |

### Spectral Source

Pulls the best performing heroes in a specified league from Spectral.gg.

- Source Key: `"spectral"`

**Parameters**

The `param` field is an object with the following properties:

| Property | Type    | Description                                                            |
|----------|---------|------------------------------------------------------------------------|
| top      | integer | How many heroes to include in the category. **Required**               |
| position | string  | The position to filter by ("P1", "P2", "P3", "P4", "P5"). **Required** |
| league   | string  | League name. **Default:** latest ranked patch                          |
