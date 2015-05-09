# TODO: __all__ = []


from collections import namedtuple
import logging
import struct

from cffi import FFI

from .sdllibs import sdl_lib
from .sdlffi import sdl_ffi
from . import sdlconstants
from . import sdlpixels
from . import color
from .rect import Rect
from .locals import palette_8bit


ffi = FFI()


PixelFormat = namedtuple('PixelFormat', 'format palette bitsperpixel bytesperpixel' +
                         ' rmask gmask bmask amask rloss gloss bloss aloss rshift gshift bshift ashift refcount next')
PixelPalette = namedtuple('PixelPalette', 'ncolors color')
# Color = namedtuple('Color', 'r g b a')


def pixel_format(cdata):
    """returns a PixelFormat
    """
    # TODO: this will be different for 8-bit surfaces with a palette
    buf = ffi.buffer(cdata)
    pixel_format_elements = struct.unpack('IIBBIIIIBBBBBBBBhI', buf)
    pixel_format = PixelFormat(*pixel_format_elements)
    # print(pixel_format)
    # print('format={}'.format(sdl.getPixelFormatName(pixel_format.format)))
    return pixel_format


class Surface(object):

    __src_rect = Rect(0, 0, 1, 1)
    __dst_rect = Rect(0, 0, 1, 1)

    def __init__(self, size_or_surf, flags=0, depth=0, masks=None, surface=None):
        if depth == 0:
            depth = 32
        if not masks:
            masks = [0] * 4
        do_blit = False
        if isinstance(size_or_surf, Surface):
            surf = size_or_surf
            width, height = surf.get_size()
            flags = surf.get_flags()
            depth = surf.get_bitsize()
            self.__sdl_surface = sdl_lib.SDL_CreateRGBSurface(flags, width, height, depth, *masks)
            do_blit = True
        else:
            width, height = size_or_surf
            if surface is None:
                self.__sdl_surface = sdl_lib.SDL_CreateRGBSurface(flags, width, height, depth, *masks)
            else:
                self.__sdl_surface = surface
        if depth == 8:
            palette_colors = sdl_ffi.cast('SDL_Color *', self.__sdl_surface.format.palette.colors)
            for i in range(256):
                c = palette_colors[i]
                c.r, c.g, c.b, c.a = palette_8bit[i]
        if do_blit:
            self.blit(size_or_surf, (0, 0))

    def get_size(self):
        surf = self.__sdl_surface
        return surf.w, surf.h

    def get_width(self):
        return self.__sdl_surface.w

    def get_height(self):
        return self.__sdl_surface.w

    def get_flags(self):
        return self.__sdl_surface.flags

    def get_bitsize(self):
        return self.__sdl_surface.format.BitsPerPixel

    def get_colorkey(self):
        surface = self.__sdl_surface
        c = color.Color(0, 0, 0, 0)
        sdl_lib.SDL_GetColorKey(surface, c.sdl_color)
        return c

    def set_colorkey(self, color, flag=1):
        """set flag=1 to enable, flag=0 to disable"""
        surface = self.__sdl_surface
        map_color = sdl_lib.SDL_MapRGBA if len(color) == 4 else sdl_lib.SDL_MapRGB
        sdl_lib.SDL_SetColorKey(surface, flag, map_color(surface.format, *color))

    def get_rect(self, **kwargs):
        """get_rect(rect=outrect, **{setattrs}) -> Rect
        If a rect is provided, its values are updated and it is returned. If rect is not provided, a new one will be
        constructed. The remaining kwargs are rect attributes to set.
        :param kwargs: rect=outrect, x=N, y=N, center=(X, Y), etc.
        :return:
        """
        if 'rect' in kwargs:
            r = kwargs['rect']
        else:
            w, h = self.get_size()
            r = Rect(0, 0, w, h)
        for k, v in kwargs.items():
            setattr(r, k, v)
        return r

    def get_at(self, pos):
        # TODO; I think this is causing random segfaults

        x, y = pos
        surf = self.__sdl_surface
        format = surf.format
        bpp = format.BytesPerPixel
        pixels = surf.pixels
        rgba = sdl_ffi.new('Uint8 [4]')

        if sdlconstants.SDL_MUSTLOCK(surf):
            if not self.lock():
                return

        # TODO: not well tested
        if bpp == 1:
            pixels = sdl_ffi.cast('Uint8 *', pixels)
            color_ = pixels[y * surf.w + x]
        elif bpp == 2:
            pixels = sdl_ffi.cast('Uint16 *', pixels)
            color_ = pixels[y * surf.w + x]
        elif bpp == 3:
            pixels = sdl_ffi.cast('Uint8 *', pixels)
            pix = pixels[(y * surf.w + x) * 3]
            if sdlconstants.SDL_BYTEORDER == sdlconstants.SDL_LIL_ENDIAN:
                    color_ = pix[0] + pix[1] << 8 + pix[2] << 16
            else:
                    color_ = pix[2] + pix[1] << 8 + pix[0] << 16
        else:  # bpp == 4
            pixels = sdl_ffi.cast('Uint32 *', pixels)
            color_ = pixels[y * surf.w + x]

        self.unlock()

        sdl_lib.SDL_GetRGBA(color_, format, rgba, rgba + 1, rgba + 2, rgba + 3)

        # TODO: return tuple instead?
        return color.Color(*rgba)

    def set_at(self, pos, color_):
        # TODO: test it

        x, y = pos
        surf = self.__sdl_surface
        format = surf.format
        bpp = format.BytesPerPixel
        if not isinstance(color_, color.Color):
            color_ = color.Color(*color_)

        if (x < surf.clip_rect.x or x >= surf.clip_rect.x + surf.clip_rect.w or
                y < surf.clip_rect.y or y >= surf.clip_rect.y + surf.clip_rect.h):
            # out of clip area
            return

        if sdlconstants.SDL_MUSTLOCK(self.__sdl_surface):
            if not self.lock():
                return

        pixels = surf.pixels

        if bpp == 1:
            buf = sdl_ffi.cast('Uint8 *', pixels)
            buf[y * surf.w + x] = sdl_lib.SDL_MapRGBA(format, color_.r, color_.g, color_.b, color_.a)
        elif bpp == 2:
            buf = sdl_ffi.cast('Uint16 *', pixels)
            buf[y * surf.w + x] = sdl_lib.SDL_MapRGBA(format, color_.r, color_.g, color_.b, color_.a)
        elif bpp == 3:
            pixels = sdl_ffi.cast('Uint8 *', pixels)
            byte_buf = pixels[(y * surf.w + x) * 3]
            if sdlconstants.SDL_BYTEORDER == sdlconstants.SDL_LIL_ENDIAN:
                # TODO
                # *(byte_buf + (format->Rshift >> 3)) = (Uint8) (color >> 16);
                # *(byte_buf + (format->Gshift >> 3)) = (Uint8) (color >> 8);
                # *(byte_buf + (format->Bshift >> 3)) = (Uint8) color;
                pass
            else:
                # TODO
                # *(byte_buf + 2 - (format->Rshift >> 3)) = (Uint8) (color >> 16);
                # *(byte_buf + 2 - (format->Gshift >> 3)) = (Uint8) (color >> 8);
                # *(byte_buf + 2 - (format->Bshift >> 3)) = (Uint8) color;
                pass
        else:  # bpp == 4
            buf = sdl_ffi.cast('Uint32 *', pixels)
            buf[y * surf.w + x] = sdl_lib.SDL_MapRGBA(format, color_.r, color_.g, color_.b, color_.a)

        self.unlock()

    def fill(self, color, rect=None, special_flags=0):
        surface = self.__sdl_surface
        map_color = sdl_lib.SDL_MapRGBA if len(color) == 4 else sdl_lib.SDL_MapRGB

        if sdlconstants.SDL_MUSTLOCK(surface):
            self.lock()
        if rect is None:
            size = self.get_size()
            self.__src_rect[:] = 0, 0, size[0], size[1]
            # rect = Rect(0, 0, size[0], size[1])
            rect = self.__src_rect
        elif not isinstance(rect, Rect):
            # rect = Rect(*rect)
            self.__src_rect[:] = rect
            rect = self.__src_rect
        sdl_lib.SDL_FillRect(surface, rect.sdl_rect, map_color(surface.format, *color))
        self.unlock()
        # return Rect()  # rather a tuple?

    def blit(self, source, dest_rect, area=None, special_flags=0):
        dest_surface = self.__sdl_surface
        if sdlconstants.SDL_MUSTLOCK(dest_surface):
            self.lock()
        if area is None:
            size = source.get_size()
            # area = Rect(0, 0, int(size[0]), int(size[1]))
            area = self.__src_rect
            area[:] = 0, 0, size[0], size[1]
        elif not isinstance(area, Rect):
            # area = Rect(*area)
            self.__src_rect[:] = area
            area = self.__src_rect
        if not isinstance(dest_rect, Rect):
            # dest_rect = Rect(dest_rect)
            size = source.get_size()
            d = self.__dst_rect
            d.topleft = dest_rect[0:2]
            d.size = size
            dest_rect = d
        sdl_lib.SDL_UpperBlit(source.sdl_surface, area.sdl_rect, dest_surface, dest_rect.sdl_rect)
        self.unlock()

    def blit_scaled(self, source, dest_rect, area=None):
        # def round_rect(r):
        #     x, y, w, h = r[0:4]
        #     x = int(round(x))
        #     w = int(round(w + r[0] - x))
        #     y = int(round(y))
        #     h = int(round(h + r[1] - y))
        #     return x, y, w, h
        dest_surface = self.__sdl_surface
        if sdlconstants.SDL_MUSTLOCK(dest_surface):
            self.lock()
        if area is None:
            # area = source.get_rect()
            size = source.get_size()
            area = self.__src_rect
            area[:] = 0, 0, int(size[0]), int(size[1])
        elif not isinstance(area, Rect):
            # area = Rect(*area)
            self.__src_rect[:] = area
            area = self.__src_rect
        if not isinstance(dest_rect, Rect):
            # dest_rect = Rect(dest_rect)
            self.__dst_rect[:] = dest_rect
            dest_rect = self.__dst_rect
        sdl_lib.SDL_UpperBlitScaled(source.sdl_surface, area.sdl_rect, dest_surface, dest_rect.sdl_rect)
        self.unlock()

    def convert(self, format=None):
        surf = get_window_list()[0].surface.sdl_surface
        if format is None:
            format = surf.format
        new_surf = sdl_lib.SDL_ConvertSurface(self.__sdl_surface, format, 0)
        if new_surf is None:
            # TODO: proper exception
            raise Exception('could not convert surface')
        return Surface((new_surf.w, new_surf.h), surface=new_surf)

    def convert_alpha(self, format=None):
        # This gets the best blit performance on my system.
        # new format=SDL_PIXELFORMAT_ARGB8888
        # window format=SDL_PIXELFORMAT_RGB888
        # surface1 format=SDL_PIXELFORMAT_ABGR8888
        # surface2 format=SDL_PIXELFORMAT_ARGB8888  <<<
        converted_surface = self
        if format:
            surf = sdl_lib.SDL_ConvertSurfaceFormat(self.sdl_surface, format, 0)
            converted_surface = Surface((surf.w, surf.h), surface=surf)
        else:
            # TODO: there's probably a more elegant way to do this
            window_format = pixel_format(get_window_list()[0].surface.sdl_surface.format).format
            surface_format = pixel_format(self.sdl_surface.format).format
            surface_layout = sdlpixels.layout_to_name[sdlpixels.pixel_layout(surface_format)]
            window_order = sdlpixels.order_to_name[sdlpixels.pixel_order(window_format)]

            if sdlpixels.is_pixel_format_alpha(surface_format):
                target_order = window_order.replace('X', 'A')
                format_name = 'SDL_PIXELFORMAT_' + target_order + surface_layout
                logging.log(logging.DEBUG, 'convert_alpha: new format={}'.format(format_name))
                format = getattr(sdlpixels, format_name)
                surf = sdl_lib.SDL_ConvertSurfaceFormat(self.sdl_surface, format, 0)
                converted_surface = Surface((surf.w, surf.h), surface=surf)
            elif sdlpixels.is_pixel_format_indexed(surface_format):
                # TODO
                pass
            elif sdlpixels.is_pixel_format_fourcc(surface_format):
                # TODO
                pass
        return converted_surface

    def copy(self):
        return Surface(self)

    def lock(self):
        sdl_lib.SDL_LockSurface(self.__sdl_surface)

    def unlock(self):
        sdl_lib.SDL_UnlockSurface(self.__sdl_surface)

    def __getsdlsurface(self):
        return self.__sdl_surface
    sdl_surface = property(__getsdlsurface)

    def __str__(self):
        return '<{}({}, {}) x {}>'.format(
            self.__class__.__name__, self.get_width(), self.get_height(), self.get_bitsize())

    def __del__(self):
        # TODO: unreliable
        if self.__sdl_surface:
            try:
                garbage = self.__sdl_surface
                self.__sdl_surface = None
                sdl_lib.SDL_FreeSurface(garbage)
            except Exception as e:
                pass


from .window import get_list as get_window_list
