import cffi
import os


CURR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
MODULE_NAME = "_lzcomp_cffi"


ffi = cffi.FFI()


ffi.cdef("""
uint8_t* do_compress(long length, uint8_t *input,
                     long *p_output_length);
uint8_t* do_decompress(long length, uint8_t* input,
                       long* p_output_length);
""")


ffi.set_source('lzcomp.'+MODULE_NAME, """
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <config.h>
#include <mtxmem.h>
#include <bitio.h>
#include <ahuff.h>
#include <lzcomp.h>
#include <errcodes.h>

uint8_t* do_compress(long length, uint8_t* input,
                     long* p_output_length) {
    int returned_status = 0;
    MTX_MemHandler* mem = NULL;
    LZCOMP* lzcomp = NULL;
    uint8_t *output = NULL;

    mem = MTX_mem_Create(&malloc, &realloc, &free);
    if (!mem) goto CLEANUP;

    lzcomp = MTX_LZCOMP_Create1(mem);
    if (!lzcomp) goto CLEANUP;

    output = (uint8_t*)MTX_LZCOMP_PackMemory(
        lzcomp, input, length, p_output_length);
    if (!output) {
        goto CLEANUP;
    } else {
        MTX_LZCOMP_Destroy(lzcomp);
        free(mem);
        return output;
    }
CLEANUP:
    MTX_LZCOMP_Destroy(lzcomp);
    free(mem);
    return NULL;
}

uint8_t* do_decompress(long length, uint8_t* input,
                       long* p_output_length) {
    int returned_status = 0;
    MTX_MemHandler* mem = NULL;
    LZCOMP* lzcomp = NULL;
    uint8_t *output = NULL;

    mem = MTX_mem_Create(&malloc, &realloc, &free);
    if (!mem) goto CLEANUP;

    lzcomp = MTX_LZCOMP_Create1(mem);
    if (!lzcomp) goto CLEANUP;

    output = (uint8_t*)MTX_LZCOMP_UnPackMemory(
        lzcomp, input, length, p_output_length, 3);
    if (!output) {
        goto CLEANUP;
    } else {
        MTX_LZCOMP_Destroy(lzcomp);
        free(mem);
        return output;
    }
CLEANUP:
    MTX_LZCOMP_Destroy(lzcomp);
    free(mem);
    return NULL;
}
""",
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
