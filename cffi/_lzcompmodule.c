#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <config.h>
#include <mtxmem.h>
#include <bitio.h>
#include <ahuff.h>
#include <lzcomp.h>
#include <errcodes.h>

const int version = 3; 

int do_compress(long length, uint8_t *input,
                long *p_output_length, uint8_t *output) {
    MTX_MemHandler *mem = NULL;
    LZCOMP *lzcomp = NULL;
    uint8_t *buf = NULL;
    long bufsize;
    int result = 0;

    mem = MTX_mem_Create(&malloc, &realloc, &free);
    if (!mem) return result;

    lzcomp = MTX_LZCOMP_Create1(mem);
    if (!lzcomp) {
        free(mem);
        return result;
    }

    buf = (uint8_t *)MTX_LZCOMP_PackMemory(
        lzcomp, input, length, &bufsize);
    if (bufsize <= *p_output_length) {
        memcpy(output, buf, bufsize);
        *p_output_length = bufsize;
        result = 1; // success!
    }
    MTX_LZCOMP_Destroy(lzcomp);
    free(mem);
    return result;
}

int do_decompress(long length, uint8_t *input,
                  int callback(void *, const uint8_t *, long),
                  void *callback_data) {
    MTX_MemHandler* mem = NULL;
    LZCOMP* lzcomp = NULL;
    uint8_t *buf = NULL;
    long bufsize;
    int result = 0;
    int num_written;

    mem = MTX_mem_Create(&malloc, &realloc, &free);
    if (!mem) return result;

    lzcomp = MTX_LZCOMP_Create1(mem);
    if (!lzcomp) {
        free(mem);
        return result;
    }

    buf = (uint8_t*)MTX_LZCOMP_UnPackMemory(
        lzcomp, input, length, &bufsize, version);
    if (!buf) {
        MTX_LZCOMP_Destroy(lzcomp);
        free(mem);
        return result;
    }

    // call Python callback function to write output bytes 
    num_written = callback(callback_data, buf, bufsize);
    if (num_written == bufsize) {
        result = 1;  // success!
    }
    MTX_LZCOMP_Destroy(lzcomp);
    free(mem);
    return result;
}
