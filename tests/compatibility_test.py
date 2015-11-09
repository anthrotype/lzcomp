#!/usr/bin/env python
from __future__ import print_function
import sys
import os
from subprocess import check_call
import time

from test_utils import PYTHON, LZCOMP, TEST_ENV, diff_q


INPUTS = """\
data/empty.compressed
data/x.compressed
data/64x.compressed
data/10x10y.compressed
data/xyzzy.compressed
data/quickfox.compressed
data/ukkonooa.compressed
data/monkey.compressed
data/backward65536.compressed
data/zeros.compressed
data/quickfox_repeated.compressed
data/compressed_file.compressed
data/compressed_repeated.compressed
data/alice29.txt.compressed
data/asyoulik.txt.compressed
data/lcet10.txt.compressed
data/plrabn12.txt.compressed
"""


start = time.time()
for filename in INPUTS.splitlines():
    print('Testing decompression of file "%s"' % os.path.basename(filename))
    uncompressed = os.path.splitext(filename)[0] + ".uncompressed"
    expected = os.path.splitext(filename)[0]
    decomp_start = time.time()
    check_call([PYTHON, LZCOMP, "-f", "-d", "-i", filename, "-o",
                uncompressed], env=TEST_ENV)
    print("--- %s seconds ---" % (time.time() - decomp_start))
    if diff_q(uncompressed, expected) != 0:
        sys.exit(1)
    # Test the streaming version
    with open(filename, "rb") as infile, open(uncompressed, "wb") as outfile:
        check_call([PYTHON, LZCOMP, '-d'], stdin=infile, stdout=outfile,
                   env=TEST_ENV)
    if diff_q(uncompressed, expected) != 0:
        sys.exit(1)
    # clean up
    os.remove(uncompressed)
print("--- TOTAL: %s seconds ---\n" % (time.time() - start))
