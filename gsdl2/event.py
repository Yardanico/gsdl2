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
    def __init__(self, type=None, window=None, mouse=None, button=None, state=None, clicks=None, pos=None):
        _Struct.__init__(self, type=type, window=window, mouse=mouse, button=button, state=state, clicks=clicks, pos=pos)


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
    return MouseButtonEvent(e.type, e.windowID, e.which, e.button, e.state, e.clicks, pos)


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


# singleton SDL event for internal use
def _Event():
    return sdl_ffi.new('SDL_Event *')
_event = _Event()


def pump():
    """internally process pygame event handlers
    pump() -> None

    :return: None
    """
    if sdl_lib.SDL_WasInit(SDL_INIT_VIDEO):
        sdl_lib.SDL_PumpEvents()


def _get_internal(filter_type=None):
    if not sdl_lib.SDL_WasInit(SDL_INIT_VIDEO):
        return []

    append = queued_events.append
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
            # local filter in arg
            if is_list and e.type not in filter_type:
                continue
            elif e.type != filter_type:
                continue
        # global filter
        if get_blocked(e.type):
            continue
        factories = get(e.type, None)
        if factories:
            factory = factories[0]
            e_obj = factory(e)
            # handle: _KeyEvent returns None if it's a repeat event
            if e_obj:
                append(e_obj)


def get(filter_type=None):
    """get events from the queue
    get() -> Eventlist
    get(type) -> Eventlist
    get(typelist) -> Eventlist

    :param filter_type: event type, type list, or None
    :return: Event list
    """
    _get_internal(filter_type)
    if filter_type is None:
        copy_events = list(queued_events)
    elif isinstance(filter_type, type(NOEVENT)):
        copy_events = [e for e in queued_events if e.type == filter_type]
    else:
        copy_events = [e for e in queued_events if e.type in filter_type]
    del queued_events[:]
    return copy_events
queued_events = []


def poll():
    """get a single event from the queue
    poll() -> EventType instance

    :return: Event
    """
    if not sdl_lib.SDL_WasInit(SDL_INIT_VIDEO):
        return None

    if queued_events:
        return queued_events.pop(0)
    else:
        _event.type = NOEVENT  # dunno if this is necessary
        sdl_lib.SDL_PollEvent(_event)
        factories = _factories.get(_event.type, _factories[NOEVENT])
        if factories:
            factory = factories[0]
            e_obj = factory(_event)
            return e_obj


def wait():
    """wait for a single event from the queue
    wait() -> EventType instance

    :return: Event
    """
    if not sdl_lib.SDL_WasInit(SDL_INIT_VIDEO):
        return None

    if queued_events:
        return queued_events.pop(0)
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
    """test if event types are waiting on the queue

    :param filter_type: an event type or list of types
    :return: bool
    """
    _get_internal()
    if isinstance(filter_type, type(NOEVENT)):
        return any([True for e in queued_events if e.type == filter_type])
    else:
        return any([True for e in queued_events if e.type in filter_type])


def clear(event_type):
    # TODO
    """remove all events from the queue
    clear() -> None
    clear(type) -> None
    clear(typelist) -> None

    :param event_type: event type, type list, or None
    :return: None
    """
    pass


def event_name(event_type):
    """get the string name from and event id
    event_name(type) -> string

    :param event_type: event ID
    :return: name string
    """
    return event_names[event_type]
event_names = {
    0: 'FIRSTEVENT',
    0x100: 'QUIT',
    0x101: 'APP_TERMINATING',
    0x102: 'APP_LOWMEMORY',
    0x103: 'APP_WILLENTERBACKGROUND',
    0x104: 'APP_DIDENTERBACKGROUND',
    0x105: 'APP_WILLENTERFOREGROUND',
    0x106: 'APP_DIDENTERFOREGROUND',
    0x200: 'WINDOWEVENT',
    0x201: 'SYSWMEVENT',
    0x300: 'KEYDOWN',
    0x301: 'KEYUP',
    0x302: 'TEXTEDITING',
    0x303: 'TEXTINPUT',
    0x400: 'MOUSEMOTION',
    0x401: 'MOUSEBUTTONDOWN',
    0x402: 'MOUSEBUTTONUP',
    0x403: 'MOUSEWHEEL',
    0x600: 'JOYAXISMOTION',
    0x601: 'JOYBALLMOTION',
    0x602: 'JOYHATMOTION',
    0x603: 'JOYBUTTONDOWN',
    0x604: 'JOYBUTTONUP',
    0x605: 'JOYDEVICEADDED',
    0x606: 'JOYDEVICEREMOVED',
    0x650: 'CONTROLLERAXISMOTION',
    0x651: 'CONTROLLERBUTTONDOWN',
    0x652: 'CONTROLLERBUTTONUP',
    0x653: 'CONTROLLERDEVICEADDED',
    0x654: 'CONTROLLERDEVICEREMOVED',
    0x655: 'CONTROLLERDEVICEREMAPPED',
    0x700: 'FINGERDOWN',
    0x701: 'FINGERUP',
    0x702: 'FINGERMOTION',
    0x800: 'DOLLARGESTURE',
    0x801: 'DOLLARRECORD',
    0x802: 'MULTIGESTURE',
    0x900: 'CLIPBOARDUPDATE',
    0x1000: 'DROPFILE',
    0x2000: 'RENDER_TARGETS_RESET',
    0x8000: 'USEREVENT',
    0xFFFF: 'LASTEVENT',
}


def set_blocked(filter_type):
    """control which events are allowed on the queue
    set_blocked(type) -> None
    set_blocked(typelist) -> None
    set_blocked(None) -> None

    :param filter_type: event type, type list, or None
    :return: None
    """
    if filter_type is None:
        del blocked_event_types[:]
    elif filter_type in event_names and filter_type not in blocked_event_types:
        blocked_event_types.append(filter_type)
    else:
        try:
            for etype in filter_type:
                if etype in event_names and etype not in blocked_event_types:
                    blocked_event_types.append(etype)
        except TypeError:
            pass
blocked_event_types = []


def set_allowed(filter_type):
    """control which events are allowed on the queue
    set_allowed(type) -> None
    set_allowed(typelist) -> None
    set_allowed(None) -> None

    :param filter_type: event type, type list, or None
    :return: None
    """
    if filter_type in blocked_event_types:
        blocked_event_types.remove(filter_type)
    else:
        try:
            for etype in filter_type:
                if etype in event_names and etype not in blocked_event_types:
                    blocked_event_types.append(etype)
        except TypeError:
            pass


def get_blocked(event_type):
    """test if a type of event is blocked from the queue
    get_blocked(event_type) -> bool

    :param event_type: event type
    :return: bool
    """
    return event_type in blocked_event_types


def set_grab(window, bool):
    """control the sharing of input devices with other applications
    set_grab(bool) -> None

    :param window: Window (e.g. gsdl2.display.get_window())
    :param bool: enable/disable grab for window
    :return: None
    """
    sdl_lib.SDL_SetWindowGrab(window.sdl_window, sdl_ffi.SDL_TRUE if bool else sdl_ffi.SDL_FALSE)


def get_grab(window):
    """test if the program is sharing input devices
    get_grab() -> bool

    :param window: Window (e.g. gsdl2.display.get_window())
    :return:
    """
    return sdl_lib.SDL_GetWindowGrab(window.sdl_window) == sdl_ffi.SDL_TRUE


def get_grabbed_window():
    """return the Window if input is grabbed, else return None
    get_grabbed_window() -> window

    :return: Window (e.g. gsdl2.display.get_window()) or None
    """
    sdl_window = sdl_lib.SDL_GetGrabbedWindow()
    if sdl_window == sdl_ffi.NULL:
        return None

    window = None
    for w in open_windows:
        if w.sdl_window == sdl_window:
            window = w
            break
    return window


def register_events(n):
    """register a number of USEREVENTS
    register_events(n) -> starting_event_number

    :param n: int
    :return: starting event number
    """
    return sdl_lib.SDL_RegisterEvents(n)


def post(event):
    """place a new event on the queue
    post(Event) -> None

    :param event: Event
    :return: None
    """
    if not get_blocked(event.type):
        _get_internal()
        queued_events.append(event)


def Event(event_type, *args, **kwargs):
    """internal event factory

    Event(type, dict) -> event
    Event(type, **kwargs) -> event
    Event(type, *args) -> event

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


from .window import open_windows
