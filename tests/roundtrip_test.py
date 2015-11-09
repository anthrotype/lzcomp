#!/usr/bin/env python
from __future__ import print_function
import sys
import os
from subprocess import check_call, Popen, PIPE
import time

from test_utils import PYTHON, LZCOMP, TEST_ENV, diff_q


INPUTS = """\
data/alice29.txt
data/asyoulik.txt
data/lcet10.txt
data/plrabn12.txt
../src/c/lzcomp.c
../src/c/mtxmem.h
../src/c/ahuff.c
%s
""" % LZCOMP


start = time.time()
for filename in INPUTS.splitlines():
    print('Roundtrip testing of file "%s"' % os.path.basename(filename))
    compressed = os.path.splitext(filename)[0] + ".comp"
    uncompressed = os.path.splitext(filename)[0] + ".decomp"
    comp_start = time.time()
    check_call([PYTHON, LZCOMP, "-f", "-i", filename, "-o", compressed],
               env=TEST_ENV)
    print("--- compression: %s seconds ---" % (time.time() - comp_start))
    decomp_start = time.time()
    check_call([PYTHON, LZCOMP, "-f", "-d", "-i", compressed, "-o",
                uncompressed], env=TEST_ENV)
    print("--- decompression: %s seconds ---" % (time.time() - decomp_start))
    if diff_q(filename, uncompressed) != 0:
        sys.exit(1)
    # Test the streaming version
    with open(filename, "rb") as infile, open(uncompressed, "wb") as outfile:
        p = Popen([PYTHON, LZCOMP], stdin=infile, stdout=PIPE, env=TEST_ENV)
        check_call([PYTHON, LZCOMP, "-d"], stdin=p.stdout, stdout=outfile,
                   env=TEST_ENV)
    if diff_q(filename, uncompressed) != 0:
        sys.exit(1)
    # clean up
    os.remove(compressed)
    os.remove(uncompressed)
print("--- TOTAL: %s seconds ---\n" % (time.time() - start))
