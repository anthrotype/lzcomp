import cffi
import os


CURR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
with open(os.path.join(CURR_DIR, "..", "c", "_lzcompmodule.c"), 'r') as f:
    source = f.read()

ffi = cffi.FFI()

ffi.cdef("""
int do_compress(long length, uint8_t *input,
                long *p_output_length, uint8_t *output);
uint8_t* do_decompress(long length, uint8_t* input,
                       long* p_output_length);
""")

ffi.set_source(
    'lzcomp._lzcomp_cffi',
    source,
    source_extension='.c',
    sources=[
        "src/c/ahuff.c",
        "src/c/bitio.c",
        "src/c/lzcomp.c",
        "src/c/mtxmem.c",
    ],
    depends=[
        "src/c/config.h",
        "src/c/mtxmem.h",
        "src/c/bitio.h",
        "src/c/ahuff.h",
        "src/c/lzcomp.h",
        "src/c/errcodes.h",
    ],
    include_dirs=["src/c"]
    )


if __name__ == '__main__':
     # cd .. to where setup.py is located
    build_dir = os.path.dirname(os.path.dirname(CURR_DIR))
    os.chdir(build_dir)
    # compile extension module here
    ffi.compile('.')
