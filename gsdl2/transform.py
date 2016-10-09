import sdl
from sdl import ffi
import gsdl2
from gsdl2.surflock import locked


def copy_surface(surface):
    new_surf = gsdl2.Surface(surface.get_size())
    new_surf.blit(surface, surface.get_rect())
    return new_surf


def scale(surface, size, dest_surface=None):
    """ scale(Surface, (width, height), DestSurface = None) -> Surface
    resize to new resolution
    """
    width, height = size
    if width < 0 or height < 0:
        raise ValueError("Cannot scale to negative size")
    if width and height:
        if dest_surface:
            # TODO: Duplicated code
            # This is for pygame compat
            new_surf = gsdl2.Surface(size)
            new_surf.blit_scaled(surface, (0, 0, width, height))
            dest = dest_surface.blit_scaled(surface, (0, 0, width, height))
            return new_surf
        else:
            new_surf = gsdl2.Surface(size)
            new_surf.blit_scaled(surface, (0, 0, width, height))
            return new_surf


# http://lazyfoo.net/SDL_tutorials/lesson31/index.php
def get_pixel32(surface, x, y):
    return surface.pixels[(y * surface.w) + x]


def put_pixel32(surface, x, y, pixel):
    surface.pixels[(y * surface.w) + x] = pixel


def _sdl_flip(surface, flags):
    flipped = None
    if surface.flags & sdl.TRUE:  # colorkey
        flipped = sdl.createRGBSurface(sdl.SWSURFACE, surface.w, surface.h, surface.format.BitsPerPixel, surface.format.Rmask,
                                       surface.format.Gmask, surface.format.Bmask, 0)
    else:
        flipped = sdl.createRGBSurface(sdl.SWSURFACE, surface.w, surface.h, surface.format.BitsPerPixel, surface.format.Rmask,
                                       surface.format.Gmask, surface.format.Bmask, surface.format.Amask)
    sdl.lockSurface(surface)
    x = 0
    y = 0
    rx = flipped.w - 1
    ry = flipped.h - 1
    while x < flipped.x:
        x+=1
        rx-=1
        while y < flipped.h:
            y+=1
            ry-=1
            pixel = get_pixel32(surface, x, y)
            if (flags & sdl.FLIP_VERTICAL) and (flags & sdl.FLIP_HORIZONTAL):
                put_pixel32(flipped, rx, ry, pixel)
            elif flags & sdl.FLIP_HORIZONTAL:
                put_pixel32(flipped, rx, y, pixel)
            elif flags & sdl.FLIP_VERTICAL:
                put_pixel32(flipped, x , ry , pixel)
    if sdl.lockSurface(surface)==-1:
        sdl.unlockSurface(surface)
    if surface.flags & sdl.TRUE:
        sdl.setColorKey(flipped, sdl.RLEACCEL | sdl.TRUE, surface.format.colorkey)
    return flipped


def flip(surface, xaxis, yaxis):
    c_surf = surface.sdl_surface
    w, h = c_surf.w, c_surf.h
    new_surf = copy_surface(surface).sdl_surface
    bpp = c_surf.format.BytesPerPixel
    src_pitch = c_surf.pitch
    dest_pitch = new_surf.pitch
    step = w * bpp

    with locked(new_surf):
        with locked(surface.sdl_surface):
            # only have to deal with rows
            if not xaxis:
                srcpixels = ffi.cast('uint8_t*', c_surf.pixels)
                destpixels = ffi.cast('uint8_t*', new_surf.pixels)
                if not yaxis:
                    # no changes - just copy pixels
                    for y in range(h):
                        dest_start = y * dest_pitch
                        src_start = y * src_pitch
                        destpixels[dest_start:dest_start + step] = \
                                srcpixels[src_start:src_start + step]
                else:
                    for y in range(h):
                        dest_start = (h - y - 1) * dest_pitch
                        src_start = y * src_pitch
                        destpixels[dest_start:dest_start + step] = \
                                srcpixels[src_start:src_start + step]
            # have to calculate position for individual pixels
            else:
                if not yaxis:
                    def get_y(y):
                        return y
                else:
                    def get_y(y):
                        return h - y - 1

                if bpp in (1, 2, 4):
                    ptr_type = 'uint%s_t*' % c_surf.format.BitsPerPixel
                    srcpixels = ffi.cast(ptr_type, c_surf.pixels)
                    destpixels = ffi.cast(ptr_type, new_surf.pixels)
                    dest_step = dest_pitch // bpp
                    src_step = src_pitch // bpp
                    for y in range(h):
                        dest_row_start = get_y(y) * dest_step
                        src_row_start = y * src_step
                        for x in range(w):
                            destpixels[dest_row_start + (w - x - 1)] = \
                                    srcpixels[src_row_start + x]
                else:
                    srcpixels = ffi.cast('uint8_t*', c_surf.pixels)
                    destpixels = ffi.cast('uint8_t*', new_surf.pixels)
                    for y in range(h):
                        dest_row_start = get_y(y) * dest_pitch
                        src_row_start = y * src_pitch
                        for x in range(0, src_pitch, 3):
                            dest_pix_start = dest_row_start + (dest_pitch - x - 3)
                            src_pix_start = src_row_start + x
                            destpixels[dest_pix_start:dest_pix_start + 3] = \
                                srcpixels[src_pix_start:src_pix_start + 3]
    new_surf = gsdl2.Surface._from_sdl_surface(new_surf)
    return new_surf


def scale2x(surface, dest_surface=None):
    double_tuple = lambda double_tuple: [value * 2 for value in double_tuple]

    if dest_surface:
        scale(surface, [value * 2 for value in surface.get_size()], dest_surface=dest_surface)
    else:
        return scale(surface, [value * 2 for value in surface.get_size()])
