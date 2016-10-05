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


def flip(surface, xaxis, yaxis):
    raise NotImplementedError


def scale2x(surface, dest_surface=None):
    double_tuple = lambda double_tuple: [value * 2 for value in double_tuple]

    if dest_surface:
        scale(surface, [value * 2 for value in surface.get_size()], dest_surface=dest_surface)
    else:
        return scale(surface, [value * 2 for value in surface.get_size()])
