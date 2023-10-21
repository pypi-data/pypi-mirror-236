from PIL import Image, ImageFile
import io
import cython
from libc.stdint cimport uint8_t
from libcpp cimport bool
from libc.stdlib cimport malloc, free
from libc.string cimport  memcpy

cdef extern from "astc_dec/astc_decomp.h" namespace "basisu::astc":
    # Unpacks a single ASTC block to pDst
    # If isSRGB is true, the spec requires the decoder to scale the LDR 8-bit endpoints to 16-bit before interpolation slightly differently,
    # which will lead to different outputs. So be sure to set it correctly (ideally it should match whatever the encoder did).
    cdef bool decompress(uint8_t* pDst, const uint8_t* data, bool isSRGB, int blockWidth, int blockHeight);

# define decoder
class ASTCDecoder(ImageFile.PyDecoder):
    dstChannelBytes = 1
    dstChannels = 4

    def decode(self, buffer):
        if isinstance(buffer, (io.BufferedReader, io.BytesIO)):
            data = buffer.read()
        else:
            data = buffer

        width  = self.state.xsize
        height = self.state.ysize
        block_width, block_height = self.args[:2]
        if len(self.args) > 2:
            is_srgb = self.args[2]
        else:
            is_srgb = False
        if block_width == 0:
            raise ValueError("block_width is 0 and will lead to a ZeroDivision. Double check for valid image data.")
        if (width + block_width - 1) == 0:
            raise ValueError("(width + block_width - 1) is 0 and leads to 0-width blocks. Double check for valid image data.")
        self.set_as_raw(
            decompress_astc(
                data,
                width,
                height,
                block_width,  # self.args[0]
                block_height, # self.args[1]
                is_srgb,  # self.args[2] if len(self.args) > 2 else False
            )
        )
        return -1, 0


@cython.cdivision(True)
cpdef bytes decompress_astc(const uint8_t[:] astc_data, size_t width, size_t height, size_t block_width, size_t block_height,
                    bint is_srgb=False):
    """
    Decompresses ASTC LDR image data to a RGBA32 buffer.
    Supports formats defined in the KHR_texture_compression_astc_ldr spec and
    returns UNORM8 values.  sRGB is not supported, and should be implemented
    by the caller.
    :param astc_data: - Compressed ASTC image buffer, must be at least |astc_data_size|
        bytes long.
    :param width: - Image width, in pixels.
    :param height: - Image height, in pixels.
    :param block_width: - Block width, in pixels.
    :param block_height: - BLock height, in pixels.
    :param is_srgb: - True/False (default)
    :returns: - Returns a buffer where the decompressed image will be
        stored, must be at least |out_buffer_size| bytes long if decompression succeeded,
        or b'' if it failed or if the astc_data_size was too small for the given width, height,
        and footprint, or if out_buffer_size is too small.
    """
    cdef size_t k_size_in_bytes = 16
    cdef size_t k_bytes_per_pixel_unorm8 = 4

    cdef size_t block_index
    cdef size_t block_x
    cdef size_t block_y
    cdef size_t blocks_wide = (width + block_width - 1) / block_width
    cdef size_t row_length = block_width * k_bytes_per_pixel_unorm8
    # some more cdefs
    cdef size_t i, y, px, py
    cdef int dst_pixel_pos, src_pixel_pos
    # cdef bytes src
    cdef uint8_t *src
    cdef uint8_t *block
    cdef const uint8_t *astc_data_ptr = &astc_data[0]
    # getting these few other right was critical for performance, and took a bit
    # of trial and error to finally figure them out
    cdef bytes img_data_ret
    cdef uint8_t *img_data = <uint8_t *> malloc(2 * width * height * 4 * sizeof(uint8_t))
    #                                           ^
    # this part in particular is important because without it, the processing
    # may overflow and crashes everything without even printing an error message


    block = <uint8_t*> malloc(block_width * block_height * 4 * sizeof(uint8_t))
    src = <uint8_t*> malloc(16 * sizeof(uint8_t))
    # we can actually get the block allocated here and re-use it as a scratchpad
    # just with one malloc() and one free() at the end
    for i in range(0, len(astc_data), 16):
        block_index = i / 16
        block_x = block_index % blocks_wide
        block_y = block_index / blocks_wide

        # src = astc_data[i:i + 16]
        memcpy(src, astc_data_ptr + i, 16)
        # block = bytes(block_width * block_height * 4)
        decompress(block, src, <bool> is_srgb, <int> block_width, <int> block_height)

        for y in range(block_height):
            py = block_height * block_y + y

            px = block_width * block_x
            dst_pixel_pos = (py * width + px) * k_bytes_per_pixel_unorm8
            src_pixel_pos = (y * block_width) * k_bytes_per_pixel_unorm8
            # img_data[dst_pixel_pos: dst_pixel_pos + row_length] = block[src_pixel_pos: src_pixel_pos + row_length]
            memcpy(img_data + dst_pixel_pos, block + src_pixel_pos, row_length)
            """
            LDR only - no pixel decoding required
            for x in range(block_width):
                px = block_width * block_x + x

                # Skip out of bounds
                if px >= width or py >= height:
                    continue

                dst_pixel_pos = (py * width + px) * k_bytes_per_pixel_unorm8
                src_pixel_pos = (y * block_width + x) * k_bytes_per_pixel_unorm8
                for j in range(k_bytes_per_pixel_unorm8):
                    img_data[dst_pixel_pos + j] = block[src_pixel_pos + j]
            """
    free(block)
    free(src)
    img_data_ret = bytes(img_data[:width * height * 4])
    free(img_data)
    return img_data_ret

# register decoder
if 'astc' not in Image.DECODERS:
    Image.register_decoder('astc', ASTCDecoder)
