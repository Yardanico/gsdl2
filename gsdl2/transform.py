import sdl

from gsdl2 import SDLError
from gsdl2.surflock import locked


def new_surface_from_surface(surface, w, h):
    if 4 < surface.format.BytesPerPixel <= 0:
        raise ValueError("unsupported Surface bit depth for transform")

    format = surface.format
    newsurf = sdl.createRGBSurface(surface.flags, w, h,
                                       format.BitsPerPixel,
                                       format.Rmask, format.Gmask,
                                       format.Bmask, format.Amask)
    if not newsurf:
        raise SDLError()

    if format.BytesPerPixel == 1 and format.palette:
        sdl.setPaletteColors(format.palette, format.palette.colors, 0,
                          format.palette.ncolors)
        sdl.setSurfacePalette(newsurf, format.palette)
    if surface.flags & sdl.TRUE:
        sdl.setColorKey(newsurf, (surface.flags & sdl.RLEACCEL) |
                            sdl.TRUE, format.colorkey)

    if surface.flags & sdl.TRUE:
        result = sdl.setSurfaceAlphaMod(newsurf, format.alpha)
        if result == -1:
            raise SDLError()

    return newsurf

def scale(surface, size, dest_surface=None):
    """ scale(Surface, (width, height), DestSurface = None) -> Surface
    resize to new resolution
    """
    width, height = size
    if width < 0 or height < 0:
        raise ValueError("Cannot scale to negative size")
    c_surf = surface._Surface__sdl_surface

    if dest_surface is None:
        new_surf = new_surface_from_surface(c_surf, width, height)
    else:
        new_surf = dest_surface

    if new_surf.w != width or new_surf.h != height:
        raise ValueError("Destination surface not the given width or height.")

    if c_surf.format.BytesPerPixel != new_surf.format.BytesPerPixel:
        raise ValueError(
            "Source and destination surfaces need the same format.")

    if width and height:
        with locked(new_surf):
            with locked(c_surf):
                return sdl.blitSurface(c_surf, sdl.ffi.NULL, new_surf, sdl.ffi.NULL)