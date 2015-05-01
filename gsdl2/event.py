from collections import namedtuple

from .sdllibs import sdl_lib
from .sdlffi import sdl_ffi
from .locals import KEYDOWN, KEYUP, QUIT


# TODO: __all__


# TODO: more event types
KeyDownEvent = namedtuple('KeyDownEvent', 'type key mod scancode')
KeyUpEvent = namedtuple('KeyUpEvent', 'type key scancode')
QuitEvent = namedtuple('QuitEvent', 'type')


def Event():
    return sdl_ffi.new('SDL_Event *')

# TODO: def Event()


_event = Event()


def get():
    events = []
    append = events.append
    e = _event
    while sdl_lib.SDL_PollEvent(_event):
        # TODO: add a behavior toggle to return these
        event_type = e.type
        if event_type == KEYDOWN:
            if e.key.repeat:
                continue
            keysym = e.key.keysym
            append(KeyDownEvent(event_type, keysym.sym, keysym.mod, keysym.scancode))
        elif event_type == KEYUP:
            keysym = e.key.keysym
            append(KeyUpEvent(event_type, keysym.sym, keysym.scancode))
        elif event_type == QUIT:
            append(QuitEvent(event_type))
    return events
