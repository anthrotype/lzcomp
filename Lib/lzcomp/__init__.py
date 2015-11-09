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
    output_length = int(1.2 * length + 10240)
    output = ffi.new("uint8_t[]", output_length)
    p_output_length = ffi.new("long[1]", [output_length])
    ok = lib.do_compress(length, string, p_output_length, output)
    if not ok:
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

    output_pieces = []
    ok = lib.do_decompress(len(string), string, _decompress_callback,
                           ffi.new_handle(output_pieces))
    if not ok:
        raise error("MTX_LZCOMP_UnpackMemory failed")
    return b''.join(output_pieces)


@ffi.callback("int callback(void *, const uint8_t *, long)")
def _decompress_callback(data, output, output_size):
    buf = ffi.buffer(output, output_size)[:]
    ffi.from_handle(data).append(buf)
    return output_size
