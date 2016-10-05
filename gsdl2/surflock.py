""" XXX """

from gsdl2 import SDLError
from gsdl2 import sdl


# TODO: prep and unprep surface


class locked(object):
    def __init__(self, surface):
        self.surface = surface

    def __enter__(self):
        res = sdl.lockSurface(self.surface)
        if res == -1:
            raise SDLError()

    def __exit__(self, *args):
        sdl.unlockSurface(self.surface)
