# lzcomp

[![Build Status](https://drone.io/github.com/anthrotype/lzcomp/status.png)](https://drone.io/github.com/anthrotype/lzcomp/latest)

CFFI-based Python bindings for the LZCOMP compression algorithm, as defined in the **Microtype® Express (MTX)** font format specification from Monotype Imaging.

<http://www.w3.org/Submission/MTX/>

Build:
```
$ python setup.py build
```

Test:
```
$ python setup.py test
```

Install:
```bash
$ pip install -v .
```

Usage:
```
lzcomp [--force] [--decompress] [--input filename] [--output filename]
```
