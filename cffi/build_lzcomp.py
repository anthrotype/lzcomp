import cffi
import os


CURR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
with open(os.path.join(CURR_DIR, "_lzcompmodule.c"), 'r') as f:
    source = f.read()

ffi = cffi.FFI()

ffi.cdef("""
int do_compress(long length, uint8_t *input,
                long *p_output_length, uint8_t *output);
int do_decompress(long length, uint8_t *input,
                  int callback(void *, const uint8_t *, long),
                  void *callback_data);
""")

ffi.set_source(
    'lzcomp._lzcomp_cffi',
    source,
    source_extension='.c',
    sources=[
        "mtx/ahuff.c",
        "mtx/bitio.c",
        "mtx/lzcomp.c",
        "mtx/mtxmem.c",
    ],
    depends=[
        "mtx/config.h",
        "mtx/mtxmem.h",
        "mtx/bitio.h",
        "mtx/ahuff.h",
        "mtx/lzcomp.h",
        "mtx/errcodes.h",
    ],
    include_dirs=["mtx"]
    )


if __name__ == '__main__':
     # cd .. to where setup.py is located
    build_dir = os.path.dirname(os.path.dirname(CURR_DIR))
    os.chdir(build_dir)
    # compile extension module here
    ffi.compile('.')
