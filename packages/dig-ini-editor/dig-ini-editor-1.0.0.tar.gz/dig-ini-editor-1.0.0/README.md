# DIG ini-editor
[![Build Status](https://img.shields.io/appveyor/build/DIG-/python-ini-editor/master?logo=appveyor&logoColor=dddddd)](https://ci.appveyor.com/project/DIG-/python-ini-editor/branch/master)
[![Build tests](https://img.shields.io/appveyor/tests/DIG-/python-ini-editor/master?logo=appveyor&logoColor=dddddd)](https://ci.appveyor.com/project/DIG-/python-ini-editor/branch/master)
[![PyPI - License](https://img.shields.io/pypi/l/dig-ini-editor?color=blue)](https://creativecommons.org/licenses/by-nd/4.0/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dig-ini-editor)](https://pypi.org/project/dig-ini-editor/)
[![PyPI - Version](https://img.shields.io/pypi/v/dig-ini-editor)](https://pypi.org/project/dig-ini-editor/)

[![Windows - Supported](https://img.shields.io/badge/windows-supported-success?logo=windows&logoColor=dddddd)](#)
[![Linux - Supported](https://img.shields.io/badge/linux-supported-success?logo=linux&logoColor=dddddd)](#)
[![MacOS - Supported](https://img.shields.io/badge/macos-supported-success?logo=apple&logoColor=dddddd)](#)

Simple command line INI editor.
- Get list of sections
- Get list of keys from section
- Get value of key from section
- Add/Edit value of key from section
- Delete key from section
- Delete entire section
- Check if section exists
- Check if section and key exists

By default, all output will be written into stdout. It can be changed with option `--output FILENAME` or `--in-place` wich will use the input file as output.

The input filename `"-"` is reserved to read from stdin (`cat file.ini | ini-editor ACTION - …`)

## Usage
```sh
python -m dig_ini_editor ACTION
```
or
```sh
ini-editor ACTION
```

`ACTION` must be one of:

### • `get`
```sh
ini-editor get filename [section [key]]
```
- If `section` is not set, will return a list of sections.
- If `key` is not set, will return a list of keys from `section`.
- Otherwise will return the value of `key` from `section`.

### • `set`
```sh
ini-editor set filename section key value
```
Will add or replace, with `value`, the value of `key` from `section`.

### • `delete`
```sh
ini-editor delete filename section [key]
```
- If `key` is not set, will remove entire `section`.
- Otherwise will remove only the `key` from `section`.

### • `exists`
```sh
ini-editor exists filename section [key]
```
Will return `"true"` and exit code `0` if the condition is satisfied, otherwise return `"false"` and exit code non-zero.
- If `key` is not set, will only check if `section` exists.

## Installation
### From PyPI (preferred):
``` sh
python -m pip install dig-ini-editor
```
### From github release:
``` sh
python -m pip install "https://github.com/DIG-/python-ini-editor/releases/download/1.0.0/dig_ini_editor-1.0.0-py3-none-any.whl"
```
or
``` sh
python -m pip install "https://github.com/DIG-/python-ini-editor/releases/download/1.0.0/dig_ini_editor.tar.gz"
```

### From github main branch:
``` sh
python -m pip install "git+https://github.com/DIG-/python-ini-editor.git@master#egg=dig_git_ignore"
```

## License
[CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0/)

- You can use and redist freely.
- You can also modify, but only for yourself.
- You can use it as a part of your project, but without modifications in this project.