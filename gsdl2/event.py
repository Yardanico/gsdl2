from .sdllibs import sdl_lib, SDLError
from .sdlffi import sdl_ffi, to_string
from .locals import (
    utf8, QUIT, WINDOWEVENT, SYSWMEVENT,
    KEYDOWN, KEYUP, TEXTEDITING, TEXTINPUT,
    MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEWHEEL,
    JOYAXISMOTION, JOYBALLMOTION, JOYHATMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYDEVICEADDED, JOYDEVICEREMOVED,
    CONTROLLERAXISMOTION, CONTROLLERBUTTONDOWN, CONTROLLERBUTTONUP, CONTROLLERDEVICEADDED, CONTROLLERDEVICEREMOVED,
    CONTROLLERDEVICEREMAPPED,
    FINGERDOWN, FINGERUP, FINGERMOTION, DOLLARGESTURE, DOLLARRECORD, MULTIGESTURE,
    CLIPBOARDUPDATE, DROPFILE, RENDER_TARGETS_RESET, USEREVENT, NOEVENT,
)
from .sdlconstants import SDL_INIT_VIDEO, SDL_QUERY, SDL_IGNORE, SDL_DISABLE, SDL_ENABLE



# TODO: __all__


class _Struct(dict):
    def __init__(self, **kwargs):
        dict.__init__(self, **kwargs)
        self.__dict__.update(**kwargs)


class NoEvent(_Struct):
    def __init__(self, type=None):
        _Struct.__init__(self, type=type)


class QuitEvent(_Struct):
    def __init__(self, type=None):
        _Struct.__init__(self, type=type)


class WindowEvent(_Struct):
    def __init__(self, type=None, window=None, event=None, data1=None, data2=None):
        _Struct.__init__(self, type=type, window=window, event=event, data1=data1, data2=data2)


class SysWMEvent(_Struct):
    def __init__(self, type=None, msg=None):
        _Struct.__init__(self, type=type, msg=msg)


class KeyEvent(_Struct):
    def __init__(self, type=None, window=None, state=None, repeat=None, key=None, mod=None, scancode=None):
        _Struct.__init__(self, type=type, window=window, state=state, repeat=repeat, key=key, mod=mod, scancode=scancode)


class TextEditingEvent(_Struct):
    def __init__(self, type=None, window=None, text=None, start=None, length=None):
        _Struct.__init__(self, type=type, window=window, text=text, start=start, length=length)


class TextInputEvent(_Struct):
    def __init__(self, type=None, window=None, text=None):
        _Struct.__init__(self, type=type, window=window, text=text)


class MouseMotionEvent(_Struct):
    def __init__(self, type=None, window=None, mouse=None, state=None, pos=None, rel=None):
        _Struct.__init__(self, type=type, window=window, mouse=mouse, state=state, pos=pos, rel=rel)


class MouseButtonEvent(_Struct):
    def __init__(self, type=None, window=None, mouse=None, state=None, clicks=None, pos=None):
        _Struct.__init__(self, type=type, window=window, mouse=mouse, state=state, clicks=clicks, pos=pos)


class MouseWheelEvent(_Struct):
    def __init__(self, type=None, window=None, mouse=None, pos=None):
        _Struct.__init__(self, type=type, window=window, mouse=mouse, pos=pos)


class JoyAxisEvent(_Struct):
    def __init__(self, type=None, joy=None, axis=None, value=None):
        _Struct.__init__(self, type=type, joy=joy, axis=axis, value=value)


class JoyBallEvent(_Struct):
    def __init__(self, type=None, joy=None, ball=None, rel=None):
        _Struct.__init__(self, type=type, joy=joy, ball=ball, rel=rel)


class JoyHatEvent(_Struct):
    def __init__(self, type=None, joy=None, hat=None, value=None):
        _Struct.__init__(self, type=type, joy=joy, hat=hat, value=value)


class JoyButtonEvent(_Struct):
    def __init__(self, type=None, joy=None, button=None, state=None):
        _Struct.__init__(self, type=type, joy=joy, button=button, state=state)


class JoyDeviceEvent(_Struct):
    def __init__(self, type=None, joy=None):
        _Struct.__init__(self, type=type, joy=joy)


class ControllerAxisEvent(_Struct):
    def __init__(self, type=None, joy=None, axis=None, value=None):
        _Struct.__init__(self, type=type, joy=joy, axis=axis, value=value)


class ControllerButtonEvent(_Struct):
    def __init__(self, type=None, joy=None, button=None, state=None):
        _Struct.__init__(self, type=type, joy=joy, button=button, state=state)


class ControllerDeviceEvent(_Struct):
    def __init__(self, type=None, joy=None):
        _Struct.__init__(self, type=type, joy=joy)


class TouchFingerEvent(_Struct):
    def __init__(self, type=None, touch=None, finger=None, pos=None, rel=None, pressure=None):
        _Struct.__init__(self, type=type, touch=touch, finger=finger, pos=pos, rel=rel, pressure=pressure)


class MultiGestureEvent(_Struct):
    def __init__(self, type=None, touch=None, dtheta=None, ddist=None, pos=None, numfingers=None):
        _Struct.__init__(self, type=type, touch=touch, dtheta=dtheta, ddist=ddist, pos=pos, numfingers=numfingers)


class DollarGestureEvent(_Struct):
    def __init__(self, type=None, touch=None, gesture=None, numfingers=None, error=None, pos=None):
        _Struct.__init__(self, type=type, touch=touch, gesture=gesture, numfingers=numfingers, error=error, pos=pos)


class DropEvent(_Struct):
    def __init__(self, type=None, file=None):
        _Struct.__init__(self, type=type, file=file)


class UserEvent(_Struct):
    def __init__(self, type=None, window=None, code=None, data1=None, data2=None):
        _Struct.__init__(self, type=type, window=window, code=code, data1=data1, data2=data2)


def _NoEvent(e):
    e = sdl_ffi.cast('SDL_CommonEvent *', e)
    return NoEvent(e.type)


def _QuitEvent(e):
    e = sdl_ffi.cast('SDL_QuitEvent *', e)
    return QuitEvent(e.type)


def _WindowEvent(e):
    e2 = sdl_ffi.cast('SDL_WindowEvent *', e)
    return WindowEvent(e2.type, e2.windowID, e2.event, e2.data1, e2.data2)


def _SysWMEvent(e):
    e = sdl_ffi.cast('SDL_SysWMEvent *', e)
    return SysWMEvent(e.type, e.msg)


def _KeyEvent(e):
    e = sdl_ffi.cast('SDL_KeyboardEvent *', e)
    if e.repeat:
        return None
    keysym = e.keysym
    return KeyEvent(e.type, e.windowID, e.state, e.repeat, keysym.sym, keysym.mod, keysym.scancode)


def _TextEditingEvent(e):
    e = sdl_ffi.cast('SDL_TextEditingEvent *', e)
    # NULL-terminated char[32-1]
    text = str(e.text).replace('\x00', '')
    return TextEditingEvent(e.type, e.windowID, utf8(text), e.start, e.length)


def _TextInputEvent(e):
    e = sdl_ffi.cast('SDL_TextInputEvent *', e)
    # NULL-terminated char[32-1]
    text = str(e.text).replace('\x00', '')
    return TextInputEvent(e.type, e.windowID, utf8(text))


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
    data1 = to_string(sdl_ffi.cast('char *', e.data1))
    data2 = to_string(sdl_ffi.cast('char *', e.data2))
    return UserEvent(e.type, e.windowID, e.code, data1, data2)


# Map event type to a factory.
_factories = {
    NOEVENT: (_NoEvent, NoEvent),
    QUIT: (_QuitEvent, QuitEvent),
    # QUIT: _OSEvent,  # ??? see SDL_event.h
    WINDOWEVENT: (_WindowEvent, WindowEvent),
    SYSWMEVENT: (_SysWMEvent, SysWMEvent),
    KEYDOWN: (_KeyEvent, KeyEvent),
    KEYUP: (_KeyEvent, KeyEvent),
    TEXTEDITING: (_TextEditingEvent, TextEditingEvent),
    TEXTINPUT: (_TextInputEvent, TextInputEvent),
    MOUSEMOTION: (_MouseMotionEvent, MouseMotionEvent),
    MOUSEBUTTONDOWN: (_MouseButtonEvent, MouseButtonEvent),
    MOUSEBUTTONUP: (_MouseButtonEvent, MouseButtonEvent),
    MOUSEWHEEL: (_MouseWheelEvent, MouseWheelEvent),
    JOYAXISMOTION: (_JoyAxisEvent, JoyAxisEvent),
    JOYBALLMOTION: (_JoyBallEvent, JoyBallEvent),
    JOYHATMOTION: (_JoyHatEvent, JoyHatEvent),
    JOYBUTTONDOWN: (_JoyButtonEvent, JoyButtonEvent),
    JOYBUTTONUP: (_JoyButtonEvent, JoyButtonEvent),
    JOYDEVICEADDED: (_JoyDeviceEvent, JoyDeviceEvent),
    JOYDEVICEREMOVED: (_JoyDeviceEvent, JoyDeviceEvent),
    CONTROLLERAXISMOTION: (_ControllerAxisEvent, ControllerAxisEvent),
    CONTROLLERBUTTONDOWN: (_ControllerButtonEvent, ControllerButtonEvent),
    CONTROLLERBUTTONUP: (_ControllerButtonEvent, ControllerButtonEvent),
    CONTROLLERDEVICEADDED: (_ControllerDeviceEvent, ControllerDeviceEvent),
    CONTROLLERDEVICEREMOVED: (_ControllerDeviceEvent, ControllerDeviceEvent),
    CONTROLLERDEVICEREMAPPED: (_ControllerDeviceEvent, ControllerDeviceEvent),
    FINGERDOWN: (_TouchFingerEvent, TouchFingerEvent),
    FINGERUP: (_TouchFingerEvent, TouchFingerEvent),
    FINGERMOTION: (_TouchFingerEvent, TouchFingerEvent),
    MULTIGESTURE: (_MultiGestureEvent, MultiGestureEvent),
    DOLLARGESTURE: (_DollarGestureEvent, DollarGestureEvent),
    DOLLARRECORD: (_DollarGestureEvent, DollarGestureEvent),
    DROPFILE: (_DropEvent, DropEvent),
    USEREVENT: (_UserEvent, UserEvent),
}


def _Event():
    return sdl_ffi.new('SDL_Event *')
_event = _Event()


def pump():
    if sdl_lib.SDL_WasInit(SDL_INIT_VIDEO):
        sdl_lib.SDL_PumpEvents()


def get(filter_type=None):
    if not sdl_lib.SDL_WasInit(SDL_INIT_VIDEO):
        return []

    append = events.append
    e = _event
    get = _factories.get

    is_none = filter_type is None
    is_list = isinstance(filter_type, list)
    use_filter = not (is_none or is_list)

    while sdl_lib.SDL_PollEvent(e):
        # f = get(e.type, None)
        # if f not in (_KeyEvent,):
        #     print(f)
        if use_filter:
            if is_list and e.type not in filter_type:
                continue
            elif e.type != filter_type:
                continue
        factories = get(e.type, None)
        if factories:
            factory = factories[0]
            e_obj = factory(e)
            # _KeyEvent returns None if it's a repeat event
            if e_obj:
                append(e_obj)
    copy_events = list(events)
    del events[:]
    return copy_events
events = []


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
    if not sdl_lib.SDL_WasInit(SDL_INIT_VIDEO):
        return None

    if events:
        return events.pop(0)
    else:
        _event.type = NOEVENT  # dunno if this is necessary
        sdl_lib.SDL_PollEvent(_event)
        factories = _factories.get(_event.type, _factories[NOEVENT])
        if factories:
            factory = factories[0]
            e_obj = factory(_event)
            return e_obj


def wait():
    if not sdl_lib.SDL_WasInit(SDL_INIT_VIDEO):
        return None

    if events:
        return events.pop(0)
    else:
        status = sdl_lib.SDL_WaitEvent(_event)
        if not status:
            raise SDLError()
        factories = _factories.get(_event.type, None)
        if factories:
            factory = factories[0]
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
    isblocked = sdl_lib.SDL_EventState(event.type, SDL_QUERY) == SDL_IGNORE
    rc = 0
    if not isblocked:
        events.append(event)


# def _fill_user_event(event_type, code, window_id, data1, data2):
#     e = sdl_ffi.new('SDL_UserEvent *')
#     e.type = event_type
#     e.code = code
#     e.windowID = window_id
#     data1 = sdl_ffi.new('char[]', utf8(data1))
#     data2 = sdl_ffi.new('char[]', utf8(data2))
#     e.data1 = sdl_ffi.cast('void *', data1)
#     e.data2 = sdl_ffi.cast('void *', data2)
#     userevent_dict[e] = data1, data2, time.time()
#     return e
# # ffi.new() objects cannot go out of scope or their storage is destroyed
# userevent_dict = {}


def Event(event_type, *args, **kwargs):
    """internal event factory

    Usages:
    Event(type, dict)
    Event(type, **kwargs)
    Event(type, *args)

    See the classes NoEvent through UserEvent for the constructor signatures.

    :param event_type: one of the SDL event types
    :param *args: varargs to complete the signature of the event constructor; args[0] may also be a dict
    :param **kwargs: kwargs to complete the signature of the event constructor
    :return: an event object that can be post()ed
    """
    factories = _factories.get(event_type, None)
    if factories:
        factory = factories[1]
        if args:
            if isinstance(args[0], dict):
                # Event(type, dict)
                event = factory(event_type, **args[0])
            else:
                # Event(type, *args)
                event = factory(event_type, *args)
        else:
            # Event(type, **kwargs)
            event = factory(event_type, **kwargs)
        return event
