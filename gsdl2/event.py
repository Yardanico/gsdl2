from collections import namedtuple

from .sdllibs import sdl_lib, SDLError
from .sdlffi import sdl_ffi
from .locals import (
    QUIT, WINDOWEVENT, SYSWMEVENT,
    KEYDOWN, KEYUP, TEXTEDITING, TEXTINPUT,
    MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEWHEEL,
    JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYDEVICEADDED, JOYDEVICEREMOVED,
    CONTROLLERAXISMOTION, CONTROLLERBUTTONDOWN, CONTROLLERBUTTONUP, CONTROLLERDEVICEADDED, CONTROLLERDEVICEREMOVED,
    CONTROLLERDEVICEREMAPPED,
    FINGERDOWN, FINGERUP, FINGERMOTION, DOLLARGESTURE, DOLLARRECORD, MULTIGESTURE,
    CLIPBOARDUPDATE, DROPFILE, RENDER_TARGETS_RESET, USEREVENT, NOEVENT
)
from .sdlconstants import SDL_INIT_VIDEO


# TODO: __all__


NoEvent = namedtuple('NoEvent', 'type')
QuitEvent = namedtuple('QuitEvent', 'type')
WindowEvent = namedtuple('WindowEvent', 'type window event data1 data2')
SysWMEvent = namedtuple('SysWMEvent', 'type msg')
KeyEvent = namedtuple('KeyDownEvent', 'type window state repeat key mod scancode')
TextEditingEvent = namedtuple('TextEditingEvent', 'type window text start length')
TextInputEvent = namedtuple('TextInputEvent', 'type window text')
MouseMotionEvent = namedtuple('MouseMotionEvent', 'type window mouse state pos rel')
MouseButtonEvent = namedtuple('MouseButtonEvent', 'type window mouse state clicks pos')
MouseWheelEvent = namedtuple('MouseWheelEvent', 'type window mouse pos')
JoyAxisEvent = namedtuple('JoyAxisEvent', 'type joy axis value')
JoyBallEvent = namedtuple('JoyBallEvent', 'type joy ball rel')
JoyHatEvent = namedtuple('JoyHatEvent', 'type joy hat value')
JoyButtonEvent = namedtuple('JoyButtonEvent', 'type joy button state')
JoyDeviceEvent = namedtuple('JoyDeviceEvent', 'type joy')
ControllerAxisEvent = namedtuple('MouseWheelEvent', 'type joy ')
ControllerButtonEvent = namedtuple('MouseWheelEvent', 'type joy ')
ControllerDeviceEvent = namedtuple('MouseWheelEvent', 'type joy ')
TouchFingerEvent = namedtuple('MouseWheelEvent', 'type touch finger pos rel pressure')
MultiGestureEvent = namedtuple('MouseWheelEvent', 'type touch dtheta ddist pos numfingers')
DollarGestureEvent = namedtuple('MouseWheelEvent', 'type touch gesture numfingers error pos')
DropEvent = namedtuple('MouseWheelEvent', 'type file')
UserEvent = namedtuple('MouseWheelEvent', 'type window code data1 data2')


def _NoEvent(e):
    e = sdl_ffi.cast('SDL_CommonEvent *', e)
    return NoEvent(e.type)


def _QuitEvent(e):
    e = sdl_ffi.cast('SDL_QuitEvent *', e)
    return QuitEvent(e.type)


def _WindowEvent(e):
    e = sdl_ffi.cast('SDL_WindowEvent *', e)
    return WindowEvent(e.type, e.windowID, e.event, e.data1, e.data2)


def _SysWMEvent(e):
    e = sdl_ffi.cast('SDL_SysWMEvent *')
    return SysWMEvent(e.type, e.msg)


def _KeyEvent(e):
    e = sdl_ffi.cast('SDL_KeyboardEvent *', e)
    if e.repeat:
        return None
    keysym = e.keysym
    return KeyEvent(e.type, e.windowID, e.state, e.repeat, keysym.sym, keysym.mod, keysym.scancode)


def _TextEditingEvent(e):
    e = sdl_ffi.cast('SDL_TextEditingEvent *', e)
    return TextEditingEvent(e.type, e.windowID, e.text, e.start, e.length)


def _TextInputEvent(e):
    e = sdl_ffi.cast('SDL_TextInputEvent *', e)
    return TextInputEvent(e.type, e.windowID, e.text)


def _MouseMotionEvent(e):
    e = sdl_ffi.cast('SDL_MouseMotionEvent *', e)
    pos = e.x, e.y
    rel = e.xrel, e.yrel
    return MouseMotionEvent(e.type, e.windowID, e.which, e.state, pos, rel)


def _MouseButtonEvent(e):
    e = sdl_ffi.cast('SDL_MouseButtonEvent *', e)
    pos = e.x, e.y
    return MouseButtonEvent(e.type, e.windowID, e.which, e.state, e.clicks, pos)


def _MouseWheelEvent(e):
    e = sdl_ffi.cast('SDL_MouseWheelEvent *', e)
    pos = e.x, e.y
    return MouseWheelEvent(e.type, e.windowID, e.which, pos)


def _JoyAxisEvent(e):
    e = sdl_ffi.cast('SDL_JoyAxisEvent *', e)
    value = e.value / 32767.0
    return JoyAxisEvent(e.type, e.which, e.axis, value)


def _JoyBallEvent(e):
    e = sdl_ffi.cast('SDL_JoyBallEvent *', e)
    rel = e.xrel, e.yrel
    return JoyBallEvent(e.type, e.which, e.ball, rel)


def _JoyHatEvent(e):
    e = sdl_ffi.cast('SDL_JoyHatEvent *', e)
    return JoyHatEvent(e.type, e.which, e.hat, e.value)


def _JoyButtonEvent(e):
    e = sdl_ffi.cast('SDL_JoyButtonEvent *', e)
    return JoyButtonEvent(e.type, e.which, e.button, e.state)


def _JoyDeviceEvent(e):
    e = sdl_ffi.cast('SDL_JoyDeviceEvent *', e)
    return JoyDeviceEvent(e.type, e.which)


def _ControllerAxisEvent(e):
    e = sdl_ffi.cast('SDL_ControllerAxisEvent *', e)
    return ControllerAxisEvent(e.type, e.which, e.axis, e.value)


def _ControllerButtonEvent(e):
    e = sdl_ffi.cast('SDL_ControllerButtonEvent *', e)
    return ControllerButtonEvent(e.type, e.which, e.button, e.state)


def _ControllerDeviceEvent(e):
    e = sdl_ffi.cast('SDL_ControllerDeviceEvent *', e)
    return ControllerDeviceEvent(e.type, e.which)


def _TouchFingerEvent(e):
    e = sdl_ffi.cast('SDL_TouchFingerEvent *', e)
    pos = e.x, e.y
    rel = e.dx, e.dy
    return TouchFingerEvent(e.type, e.touchID, e.fingerID, pos, rel, e.pressure)


def _MultiGestureEvent(e):
    e = sdl_ffi.cast('SDL_MultiGestureEvent *', e)
    pos = e.x, e.y
    return MultiGestureEvent(e.type, e.touchID, e.dTheta, e.dDist, pos, e.numFingers)


def _DollarGestureEvent(e):
    e = sdl_ffi.cast('SDL_DollarGestureEvent *', e)
    pos = e.x, e.y
    return DollarGestureEvent(e.type, e.touchID, e.gestureID, e.numFingers, e.error, pos)


def _DropEvent(e):
    e = sdl_ffi.cast('SDL_DropEvent *', e)
    return DropEvent(e.type, e.file)


def _UserEvent(e):
    e = sdl_ffi.cast('SDL_UserEvent *', e)
    return UserEvent(e.type, e.windowID, e.code, e.data1, e.data2)


# Map event type to a factory.
_factories = {
    NOEVENT: _NoEvent,
    QUIT: _QuitEvent,
    # QUIT: _OSEvent,  # ??? see SDL_event.h
    WINDOWEVENT: _WindowEvent,
    SYSWMEVENT: _SysWMEvent,
    KEYDOWN: _KeyEvent,
    KEYUP: _KeyEvent,
    TEXTEDITING: _TextEditingEvent,
    TEXTINPUT: _TextInputEvent,
    MOUSEMOTION: _MouseMotionEvent,
    MOUSEBUTTONDOWN: _MouseButtonEvent,
    MOUSEBUTTONUP: _MouseButtonEvent,
    MOUSEWHEEL: _MouseWheelEvent,
    JOYAXISMOTION: _JoyAxisEvent,
    JOYBALLMOTION: _JoyBallEvent,
    JOYHATMOTION: _JoyHatEvent,
    JOYBUTTONDOWN: _JoyButtonEvent,
    JOYBUTTONUP: _JoyButtonEvent,
    JOYDEVICEADDED: _JoyDeviceEvent,
    JOYDEVICEREMOVED: _JoyDeviceEvent,
    CONTROLLERAXISMOTION: _ControllerAxisEvent,
    CONTROLLERBUTTONDOWN: _ControllerButtonEvent,
    CONTROLLERBUTTONUP: _ControllerButtonEvent,
    CONTROLLERDEVICEADDED: _ControllerDeviceEvent,
    CONTROLLERDEVICEREMOVED: _ControllerDeviceEvent,
    CONTROLLERDEVICEREMAPPED: _ControllerDeviceEvent,
    FINGERDOWN: _TouchFingerEvent,
    FINGERUP: _TouchFingerEvent,
    FINGERMOTION: _TouchFingerEvent,
    MULTIGESTURE: _MultiGestureEvent,
    DOLLARGESTURE: _DollarGestureEvent,
    DOLLARRECORD: _DollarGestureEvent,
    DROPFILE: _DropEvent,
    USEREVENT: _UserEvent,
}


def _Event():
    return sdl_ffi.new('SDL_Event *')
_event = _Event()


def pump():
    if sdl_lib.SDL_WasInit(SDL_INIT_VIDEO):
        sdl_lib.PumpEvents()


def get(filter_type=None):
    events = []

    if not sdl_lib.SDL_WasInit(SDL_INIT_VIDEO):
        return events

    append = events.append
    e = _event
    get = _factories.get

    is_none = filter_type is None
    is_list = isinstance(filter_type, list)
    use_filter = not (is_none or is_list)

    while sdl_lib.SDL_PollEvent(e):
        if use_filter:
            if is_list and e.type not in filter_type:
                continue
            elif e.type != filter_type:
                continue
        factory = get(e.type, None)
        if factory:
            e_obj = factory(e)
            # _KeyEvent returns None if it's a repeat event
            if e_obj:
                append(e_obj)
    return events


# int SDL_PeepEvents(SDL_Event * events, int numevents, SDL_eventaction action, Uint32 minType, Uint32 maxType);
# SDL_bool SDL_HasEvent(Uint32 type);
# SDL_bool SDL_HasEvents(Uint32 minType, Uint32 maxType);
# void SDL_FlushEvent(Uint32 type);
# void SDL_FlushEvents(Uint32 minType, Uint32 maxType);
# int SDL_PollEvent(SDL_Event * event);
# int SDL_WaitEvent(SDL_Event * event);
# int SDL_WaitEventTimeout(SDL_Event * event, int timeout);
# int SDL_PushEvent(SDL_Event * event);
# typedef int (* SDL_EventFilter) (void *userdata, SDL_Event * event);
# void SDL_SetEventFilter(SDL_EventFilter filter, void *userdata);
# SDL_bool SDL_GetEventFilter(SDL_EventFilter * filter, void **userdata);
# void SDL_AddEventWatch(SDL_EventFilter filter, void *userdata);
# void SDL_DelEventWatch(SDL_EventFilter filter, void *userdata);
# void SDL_FilterEvents(SDL_EventFilter filter, void *userdata);
# #define SDL_QUERY   -1
# #define SDL_IGNORE   0
# #define SDL_DISABLE  0
# #define SDL_ENABLE   1
# Uint8 SDL_EventState(Uint32 type, int state);
# #define SDL_GetEventState(type) SDL_EventState(type, SDL_QUERY)
# Uint32 SDL_RegisterEvents(int numevents);

def poll():
    if sdl_lib.SDL_WasInit(SDL_INIT_VIDEO):
        _event.type = NOEVENT  # dunno if this is necessary
        sdl_lib.SDL_PollEvent(_event)
        factory = _factories.get(_event.type, _factories[NOEVENT])
        if factory:
            e_obj = factory(_event)
            return e_obj


def wait():
    if sdl_lib.SDL_WasInit(SDL_INIT_VIDEO):
        status = sdl_lib.SDL_WaitEvent(_event)
        if not status:
            raise SDLError()
        factory = _factories.get(_event.type, None)
        if factory:
            e_obj = factory(_event)
            return e_obj


def peek(filter_type):
    # TODO
    pass


def event_name(event_type):
    # TODO
    pass


def set_blocked(filter_type):
    # TODO
    pass


def set_allowed(filter_type):
    # TODO
    pass


def get_blocked(event_type):
    # TODO
    pass


def set_grab(boolean):
    # TODO
    pass


def get_grab():
    # TODO
    pass


def post(event):
    # TODO
    pass


def Event(event_type, *args, **kwargs):
    # TODO
    pass
