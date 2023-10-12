# ProcessCUP

Processes 3DS CUPs (Cartridge Update Partitions) from cartridge dumps

## Setup

ProcessCUP requires argparse and pyctr to function. Due to pyctr not being packaged by most distros, the recommended method to install dependencies is to run `pip install -r requirements.txt` within a Python venv. [pyctr](https://github.com/ihaveamac/pyctr) requires additional setup, see see [ninfs's repo](https://github.com/ihaveamac/ninfs#setup) for setup details. Note that `--boot9`/`--seeddb` is not currently supported by ProcessCUP.

## Usage

`ProcessCUP.py` for details. Note that `path` can either a cartridge image, or a directory (which will be recursively searched) containing multiple cartridge images

## Credits

[ihaveahax](https://github.com/ihaveamac) for ninfs
[luigoalma](https://github.com/luigoalma) for testing and recommendations
