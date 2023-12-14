# netquality

_Benchmark your internet connection._
<br>

| Measure speed, ping, jitter and packet loss. | Get a rating to understand and compare results. |
| :------------------------------------------: | :---------------------------------------------: |
|     ![](https://i.imgur.com/K1hF3o6.png)     |      ![](https://i.imgur.com/diodVSM.png)       |

Table of Contents

- [netquality](#netquality)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
    - [From PyPI](#from-pypi)
    - [From source](#from-source)
    - [Installing to system path (Linux)](#installing-to-system-path-linux)
  - [Usage](#usage)
  - [Uninstalling](#uninstalling)
  - [License](#license)

## Dependencies

- [Python 3.8+](https://www.python.org/downloads)
- [poetry](https://python-poetry.org/docs/#installation)
- [speedtest-cli](https://pypi.org/project/speedtest-cli)
- [pythonping](https://pypi.org/project/pythonping)
- [match-func](https://pypi.org/project/match-func)
- [string-grab](https://pypi.org/project/string-grab)

## Installation

### From PyPI

```sh
pipx install netquality
```

### From source

Open a **Terminal** and run the following commands:

```sh
git clone https://github.com/julynx/netquality
cd netquality
poetry install
poetry run netquality
```

### Installing to system path (Linux)

This option is not recommended, as it may cause conflicts with other packages because of the `netquality` dependencies.

Open a **Terminal** and run the following commands:

```sh
git clone https://github.com/julynx/netquality
cd netquality/netquality
mv __main__.py netquality
sudo chmod +x netquality
sudo cp netquality /usr/bin
```

## Usage

You can run netquality from anywhere with the `netquality` command.

> Note: To run netquality from anywhere, it is required to use root privileges due to the [pythonping](https://pypi.org/project/pythonping) library. See the reason [here](https://github.com/alessandromaggio/pythonping?tab=readme-ov-file#why-do-i-need-to-be-root-to-use-pythonping). Because of this, it is currently being studied to replace it with [pingparsing](https://github.com/thombashi/pingparsing) which may be a simpler approach.

## Uninstalling

To uninstall `netquality`, simply remove the installation folder and the executables from the system path. If you installed it from PyPI, you can use the following commands:

```sh
pipx uninstall netquality
```

## License

`netquality` is released under the [GPL-2.0 License](https://opensource.org/license/gpl-2-0).
