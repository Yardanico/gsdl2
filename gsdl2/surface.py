# TODO: __all__ = []


from collections import namedtuple
import logging


from gsdl2 import sdl, ffi
from gsdl2.sdlconstants import get_sdl_byteorder
from gsdl2.sdlconstants import SDL_BYTEORDER, SDL_LIL_ENDIAN, SDL_BIG_ENDIAN, SDL_MUSTLOCK
from gsdl2 import sdlpixels, SDLError
from gsdl2.rect import Rect, sdl_rect_from_rect, game_rect_from_obj
from gsdl2.locals import palette_8bit, Color
from gsdl2.surflock import locked

PixelFormat = namedtuple('PixelFormat', 'format palette bitsperpixel bytesperpixel' +
                         ' rmask gmask bmask amask rloss gloss bloss aloss rshift gshift bshift ashift refcount next')
PixelPalette = namedtuple('PixelPalette', 'ncolors color')


# Color = namedtuple('Color', 'r g b a')


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
            self.__sdl_surface = sdl.createRGBSurface(flags, width, height, depth, *masks)
            do_blit = True
        else:
            if surface is None:
                width, height = size_or_surf
                self.__sdl_surface = sdl.createRGBSurface(flags, width, height, depth, *masks)
            else:
                self.__sdl_surface = surface
        if depth == 8:
            palette_colors = sdl.ffi.cast('SDL_Color *', self.__sdl_surface.format.palette.colors)
            for i in range(256):
                c = palette_colors[i]
                c.r, c.g, c.b, c.a = palette_8bit[i]
        if do_blit:
            self.blit(size_or_surf, (0, 0))

    def get_size(self):
        surf = self.__sdl_surface
        return surf.w, surf.h

    size = property(get_size)

    def get_width(self):
        return self.__sdl_surface.w

    width = property(get_width)
    w = width

    def get_height(self):
        return self.__sdl_surface.w

    height = property(get_height)
    h = height

    def get_flags(self):
        return self.__sdl_surface.flags

    flags = property(get_flags)

    def get_masks(self):
        f = self.__sdl_surface.format
        return f.Rmask, f.Gmask, f.Bmask, f.Amask

    masks = property(get_masks)

    def get_bitsize(self):
        return self.__sdl_surface.format.BitsPerPixel

    bitsize = property(get_bitsize)

    def get_colorkey(self):
        surface = self.__sdl_surface
        c = Color(0, 0, 0, 0)
        sdl.getColorKey(surface, c.sdl_color)
        return c

    def set_colorkey(self, color, flag=1):
        """set flag=1 to enable, flag=0 to disable"""
        surface = self.__sdl_surface
        map_color = sdl.mapRGBA if len(color) == 4 else sdl.mapRGB
        sdl.setColorKey(surface, flag, map_color(surface.format, *color))

    colorkey = property(get_colorkey, set_colorkey)

    def get_blendmode(self):
        cdata = sdl.ffi.new('SDL_BlendMode *')

        sdl.getTextureBlendMode(self.sdl_surface, cdata)
        value = int(cdata[0])
        return value

    def set_blendmode(self, mode):
        sdl.setTextureBlendMode(self.sdl_surface, mode)

    blendmode = property(get_blendmode, set_blendmode)

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

    def get_bounding_rect(self, min_alpha=1):
        """ get_bounding_rect(min_alpha = 1) -> Rect
        find the smallest rect containing data
        """

        min_alpha = int(min_alpha)
        if min_alpha > 255:
            min_alpha = 255
        elif min_alpha < 0:
            min_alpha = 0

        r, g, b, a = (ffi.new('uint8_t *'), ffi.new('uint8_t *'),
                      ffi.new('uint8_t *'), ffi.new('uint8_t *'))

        format = self.sdl_surface.format
        if self.sdl_surface.flags & sdl.TRUE:
            keyr = ffi.new('uint8_t *')
            keyg = ffi.new('uint8_t *')
            keyb = ffi.new('uint8_t *')
            try:
                sdl.getRGBA(format.colorkey,
                                format, keyr, keyg, keyb, a)
                keyr, keyg, keyb = keyr[0], keyg[0], keyb[0]
            except:
                pass
        else:
            keyr = keyg = keyb = None

        min_x, min_y, max_x, max_y = 0, 0, self.w, self.h

        def check_alpha(x, y):
            value = self.get_at((x,y))
            sdl.getRGBA(value, format, r, g, b, a)
            if (keyr is None and a[0] >= min_alpha) or \
               (keyr is not None and (r[0] != keyr or
                                      g[0] != keyg or
                                      b[0] != keyb)):
               return True
            return False

        with locked(self.sdl_surface):
            found_alpha = False
            for y in range(max_y - 1, -1, -1):
                for x in range(min_x, max_x):
                    found_alpha = check_alpha(x, y)
                    if found_alpha:
                        break
                if found_alpha:
                    break
                max_y = y

            found_alpha = False
            for x in range(max_x - 1, -1, -1):
                for y in range(min_y, max_y):
                    found_alpha = check_alpha(x, y)
                    if found_alpha:
                        break
                if found_alpha:
                    break
                max_x = x

            found_alpha = False
            for y in range(min_y, max_y):
                min_y = y
                for x in range(min_x, max_x):
                    found_alpha = check_alpha(x, y)
                    if found_alpha:
                        break
                if found_alpha:
                    break

            found_alpha = False
            for x in range(min_x, max_x):
                min_x = x
                for y in range(min_y, max_y):
                    found_alpha = check_alpha(x, y)
                    if found_alpha:
                        break
                if found_alpha:
                    break

        return Rect._from4(min_x, min_y, max_x - min_x, max_y - min_y)


    def get_at(self, pos):
        # TODO; I think this is causing random segfaults

        x, y = pos
        surf = self.__sdl_surface
        format = surf.format
        bpp = format.BytesPerPixel
        pixels = surf.pixels
        rgba = sdl.ffi.new('Uint8 [4]')

        if SDL_MUSTLOCK(surf):
            if not self.lock():
                return

        # TODO: not well tested
        if bpp == 1:
            pixels = sdl.ffi.cast('Uint8 *', pixels)
            color_ = pixels[y * surf.w + x]
        elif bpp == 2:
            pixels = sdl.ffi.cast('Uint16 *', pixels)
            color_ = pixels[y * surf.w + x]
        elif bpp == 3:
            pixels = sdl.ffi.cast('Uint8 *', pixels)
            pix = pixels[(y * surf.w + x) * 3]
            if SDL_BYTEORDER == SDL_LIL_ENDIAN:
                color_ = pix[0] + pix[1] << 8 + pix[2] << 16
            else:
                color_ = pix[2] + pix[1] << 8 + pix[0] << 16
        else:  # bpp == 4
            pixels = sdl.ffi.cast('Uint32 *', pixels)
            color_ = pixels[y * surf.w + x]

        self.unlock()

        sdl.getRGBA(color_, format, rgba, rgba + 1, rgba + 2, rgba + 3)

        # TODO: return tuple instead?
        return Color(*rgba)

    def set_at(self, pos, color_):
        x, y = pos
        surf = self.__sdl_surface
        pixels = surf.pixels
        surf_format = surf.format
        bpp = surf_format.BytesPerPixel
        if not isinstance(color_, Color):
            color_ = Color(*color_)

        if (x < surf.clip_rect.x or x >= surf.clip_rect.x + surf.clip_rect.w or
                    y < surf.clip_rect.y or y >= surf.clip_rect.y + surf.clip_rect.h):
            # out of clip area
            return

        if SDL_MUSTLOCK(surf):
            if not self.lock():
                return

        c = sdl.mapRGBA(surf_format, color_.r, color_.g, color_.b, color_.a)
        if bpp == 1:
            buf = sdl.ffi.cast('Uint8 *', pixels)
            buf[y * surf.w + x] = c
        elif bpp == 2:
            buf = sdl.ffi.cast('Uint16 *', pixels)
            buf[y * surf.w + x] = c
        elif bpp == 3:
            # TODO: test 24 bit
            buf = sdl.ffi.cast('Uint8 *', pixels)
            rgb = sdl.ffi.new('Uint8 [4]')
            color = sdl.ffi.cast('Uint32 *', color_.sdl_color)
            sdl.getRGB(color[0], surf.format, rgb, rgb + 1, rgb + 2)
            byte_buf = buf + y * surf.pitch + x * 3
            if SDL_BYTEORDER == SDL_BIG_ENDIAN:
                byte_buf[0] = rgb[0]
                byte_buf[1] = rgb[1]
                byte_buf[2] = rgb[2]
            else:
                byte_buf[2] = rgb[0]
                byte_buf[1] = rgb[1]
                byte_buf[0] = rgb[2]
        else:  # bpp == 4
            buf = sdl.ffi.cast('Uint32 *', pixels)
            buf[y * surf.w + x] = c

        self.unlock()

    def fill(self, color, rect=None, special_flags=0):
        surface = self.__sdl_surface
        map_color = sdl.mapRGBA if len(color) == 4 else sdl.mapRGB

        if SDL_MUSTLOCK(surface):
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
        rect = sdl_rect_from_rect(rect)
        sdl.fillRect(surface, rect, map_color(surface.format, *color))
        self.unlock()
        # return Rect()  # rather a tuple?
    def blit(self, source, dest_rect, area=None, special_flags=0):
        dest_surface = self.__sdl_surface
        if SDL_MUSTLOCK(dest_surface):
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
        area, dest_rect = sdl_rect_from_rect(area, dest_rect)
        sdl.upperBlit(source.sdl_surface, area, dest_surface, dest_rect)
        self.unlock()

    def blit_scaled(self, source, dest_rect, area=None):
        dest_surface = self.__sdl_surface
        if SDL_MUSTLOCK(dest_surface):
            self.lock()
        if area is None:
            size = source.get_size()
            area = self.__src_rect
            area[:] = 0, 0, int(size[0]), int(size[1])
        elif not isinstance(area, Rect):
            self.__src_rect[:] = area
            area = self.__src_rect
        sdl_dest_rect = self.__dst_rect.sdl_rect
        x, y, w, h = [int(n) for n in dest_rect]
        # The following adjustment is intended to prevent jiggling which occurs when the size is an odd unit.
        if w % 2:
            x -= 1
            w += 1
        if h % 2:
            y -= 1
            h += 1
        sdl_dest_rect.x = x
        sdl_dest_rect.y = y
        sdl_dest_rect.w = w
        sdl_dest_rect.h = h
        sdl.upperBlitScaled(source.sdl_surface, area.sdl_rect, dest_surface, sdl_dest_rect)
        self.unlock()

    def set_alpha(self, value=None, flags=0):
        """ set_alpha(value, flags=0) -> None
        set the alpha value for the full Surface image
        """
        if value is not None:
            value = int(value)
            if value > 255:
                value = 255
            if value < 0:
                value = 0
        else:
            value = 255

        with locked(self.sdl_surface):
            if sdl.setSurfaceAlphaMod(self.sdl_surface, value) == -1:
                raise SDLError()

    def convert(self, format=None):
        surf = get_window_list()[0].surface.sdl_surface
        if format is None:
            format = surf.format
        new_surf = sdl.convertSurface(self.__sdl_surface, format, 0)
        if new_surf is None:
            # TODO: proper exception
            raise Exception('could not convert surface')
        new_surf = Surface((new_surf.w, new_surf.h), surface=new_surf)
        if not new_surf:
            SDLError()
        return new_surf

    def _set_at(self, x, y, c_color):
        bpp = self.sdl_surface.format.BytesPerPixel
        if bpp == 1:
            pixels = ffi.cast("uint8_t*", self.sdl_surface.pixels)
            pixels[y * self.sdl_surface.pitch // bpp + x] = c_color
        elif bpp == 2:
            pixels = ffi.cast("uint16_t*", self.sdl_surface.pixels)
            pixels[y * self.sdl_surface.pitch // bpp + x] = c_color
        elif bpp == 3:
            pixels = ffi.cast("uint8_t*", self.sdl_surface.pixels)
            base = y * self.sdl_surface.pitch + x * 3
            fmt = self.sdl_surface.format
            if get_sdl_byteorder() == SDL_LIL_ENDIAN:
                pixels[base + (fmt.Rshift >> 3)] = ffi.cast('uint8_t', c_color >> 16)
                pixels[base + (fmt.Gshift >> 3)] = ffi.cast('uint8_t', c_color >> 8)
                pixels[base + (fmt.Bshift >> 3)] = ffi.cast('uint8_t', c_color)
            else:
                pixels[base + 2 - (fmt.Rshift >> 3)] = ffi.cast('uint8_t', c_color >> 16)
                pixels[base + 2 - (fmt.Gshift >> 3)] = ffi.cast('uint8_t', c_color >> 8)
                pixels[base + 2 - (fmt.Bshift >> 3)] = ffi.cast('uint8_t', c_color)
        elif bpp == 4:
            pixels = ffi.cast("uint32_t*", self.sdl_surface.pixels)
            pixels[y * (self.sdl_surface.pitch // bpp) + x] = c_color
        else:
            raise RuntimeError("invalid color depth for surface")

    def get_clip(self):
        """ get_clip() -> Rect
        get the current clipping area of the Surface
        """
        c_rect = self.sdl_surface.clip_rect
        return Rect._from4(c_rect.x, c_rect.y, c_rect.w, c_rect.h)

    def convert_alpha(self, format=None):
        # This gets the best blit performance on my system.
        # new format=SDL_PIXELFORMAT_ARGB8888
        # window format=SDL_PIXELFORMAT_RGB888
        # surface1 format=SDL_PIXELFORMAT_ABGR8888
        # surface2 format=SDL_PIXELFORMAT_ARGB8888  <<<
        converted_surface = self
        if format:
            surf = sdl.convertSurfaceFormat(self.sdl_surface, format, 0)
            converted_surface = Surface((surf.w, surf.h), surface=surf)
        else:
            # TODO: there's probably a more elegant way to do this
            window_format = get_window_list()[0].surface.sdl_surface.format.format
            surface_format = self.sdl_surface.format.format
            surface_layout = sdlpixels.layout_to_name[sdlpixels.pixel_layout(surface_format)]
            window_order = sdlpixels.order_to_name[sdlpixels.pixel_order(window_format)]

            if sdlpixels.is_pixel_format_alpha(surface_format):
                target_order = window_order.replace('X', 'A')
                format_name = 'SDL_PIXELFORMAT_' + target_order + surface_layout
                logging.log(logging.DEBUG, 'convert_alpha: new format={}'.format(format_name))
                format = getattr(sdlpixels, format_name)
                surf = sdl.convertSurfaceFormat(self.sdl_surface, format, 0)
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
        sdl.lockSurface(self.__sdl_surface)

    def unlock(self):
        sdl.unlockSurface(self.__sdl_surface)

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
                sdl.freeSurface(garbage)
            except Exception as e:
                pass


from gsdl2.window import get_list as get_window_list
