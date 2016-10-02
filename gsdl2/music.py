import sdl

from gsdl2.locals import utf8, USEREVENT
from gsdl2.sdlconstants import SDL_INIT_AUDIO
from gsdl2 import event


class _globals:
    current_name = ''
    current = None
    queued = None
    end_event = None
    code = 0


def get_init():
    return sdl.mixer.wasInit(SDL_INIT_AUDIO)


# EXPERIMENTAL: enabled callback for pypy 4.0.0
# https://cffi.readthedocs.org/en/latest
#
@sdl.ffi.callback('void (*)()')
def _music_finished():
    if _globals.queued is not None:
        load(_globals.queued)
        _globals.queued = None
        play()
    if _globals.end_event is not None:
        event.post(event.Event(
            _globals.end_event, code=_globals.code, window=0, data1=_globals.current_name, data2=None))
sdl.mixer.hookMusicFinished(_music_finished)


def load(filename):
    clear_queue()
    if get_busy():
        stop()
    _globals.current = sdl.mixer.loadMUS(utf8(filename))
    _globals.current_name = filename
    set_volume(1.0)


def play(loops=0, start=0.0):
    if _globals.current is not None:
        sdl.mixer.playMusic(_globals.current, loops)
        if start > 0.0:
            set_pos(start)


def rewind():
    if get_busy():
        sdl.mixer.rewindMusic()


def stop():
    if get_busy():
        sdl.mixer.haltMusic()


def pause():
    if get_busy():
        sdl.mixer.pauseMusic()


def unpause():
    if get_busy() and sdl.mixer.pausedMusic():
        sdl.mixer.resumeMusic()


def fadein(music, loops=0, ms=1000):
    load(music)
    sdl.mixer.fadeInMusic(_globals.current, loops, ms)


def fadeout(ms):
    clear_queue()
    if get_busy():
        sdl.mixer.fadeOutMusic(ms)


def set_volume(volume):
    if not (0.0 < volume < 1.0):
        volume = 1.0
    v = int(volume * 128)
    sdl.mixer.volumeMusic(v)


def get_volume(volume):
    sdl.mixer.volumeMusic(-1) / 128.0


def get_busy():
    return sdl.mixer.playingMusic()


def set_pos(pos):
    if pos > 0.0:
        # TODO: if ogg, flac, etc... see comments in SDL_mixer.h
        sdl.mixer.setMusicPosition(pos)


def get_pos(pos):
    # TODO: looking at pygame source, I guess this is a non-SDL calculation
    # return ms
    pass


def queue(filename):
    """queue a file for playing

    A maximum of one current and one queued is supported. If there is no current song, the queued song will fill that
    slot and begin playing immediately. If the current slot is filled the queued song will be added to the queued slot,
    and when the current song ends the queued slot will advance to the current slot and begin playing.

    Queueing a song to the queued slot will overwrite the one currently in that slot.

    :param filename:
    :return:
    """
    current = _globals.current
    if current is None:
        _globals.current = sdl.mixer.loadMUS(utf8(filename))
        _globals.current_name = filename
    else:
        # _globals.queued = mixer_lib.Mix_LoadMUS(utf8(filename))
        _globals.queued = utf8(filename)
    if not get_busy():
        play()


def clear_queue():
    _globals.queued = None


def set_endevent(event_type=USEREVENT, code=0):
    """set or unset song-finished event and code

    If event_type is USEREVENT, a SDL USEREVENT will be posted when any song finishes. If event_type is None, no such
    events will be posted.

    code is an integer value intended to add a signature useful to event handlers.

    The USEREVENT's data1 member will contain the filename used to load the song.

    :param event_type: USEREVENT or None
    :param code: int
    :return: None
    """
    _globals.end_event = event_type
    _globals.code = int(code)


def get_endevent():
    return _globals.end_event
