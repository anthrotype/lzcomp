"""The functions in this module allow compression and decompression using the
LZCOMP library.
"""
from ._lzcomp_cffi import ffi, lib


class error(Exception):
    pass

def compress(string):
    """Compress a byte string.

Signature:
  compress(string)

Args:
  string (bytes): The input data.

Returns:
  The compressed byte string.

Raises:
  lzcomp.error: If arguments are invalid, or compressor fails."""

    length = len(string)
    p_output_length = ffi.new("long[1]", [0])
    output = lib.do_compress(length, string, p_output_length)
    if not output:
        raise error("MTX_LZCOMP_PackMemory failed")
    return ffi.buffer(output, p_output_length[0])[:]


def decompress(string):
    """Decompress a compressed byte string.

Signature:
  decompress(string)

Args:
  string (bytes): The compressed input data.

Returns:
  The decompressed byte string.

Raises:
  brotli.error: If decompressor fails."""

    length = len(string)
    p_output_length = ffi.new("long[1]", [0])
    output = lib.do_decompress(length, string, p_output_length)
    if not output:
        raise error("MTX_LZCOMP_UnpackMemory failed")
    return ffi.buffer(output, p_output_length[0])[:]
