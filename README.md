# Module Map

This is a lightweight package which allows module descriptions to be captured as json files. These can then be compared to capture changes in the module structure between versions.

## Installation
_modulemap_ can be installed by running `pip install modulemap`. It requires Python 3.5.0+ to run.

## Dependencies
- [jsondiff](https://github.com/fzumstein/jsondiff)

## Features
- Mapping modules at varying levels of depth
- Quick evaluation of module changes

## Code Example

```python
import modulemap

modulemap.map_module('os')
modulemap.map_module('shutil')

differences = modulemap.compare_module_maps('os_modulemap.json', 'shutil_modulemap.json')

print(differences)
```