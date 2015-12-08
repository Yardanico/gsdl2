from .sdllibs import sdl_lib, mixer_lib
from .sdlffi import sdl_ffi
from .locals import utf8
from .sdlconstants import SDL_INIT_AUDIO

import event


class _globals:
    # TODO: this needs better logic, and probably a thread to monitor the queue
    current_name = ''
    current = None
    queued = None
    end_event = None


def get_init():
    return sdl_lib.SDL_WasInit(SDL_INIT_AUDIO)


# EXPERIMENTAL: enabled callback for pypy 4.0.0
# https://cffi.readthedocs.org/en/latest
#
if True:
    @sdl_ffi.callback('void (*)()')
    def _music_finished():
        if _globals.queued is not None:
            load(_globals.queued)
            _globals.queued = None
            play()
        if _globals.end_event:
            event.post(event.Event(_globals.end_event, data1=_globals.current_name))
        # TODO: post an event if configured on the Channel
    mixer_lib.Mix_HookMusicFinished(_music_finished)


def load(filename):
    if get_busy():
        stop()
    _globals.current = mixer_lib.Mix_LoadMUS(utf8(filename))
    _globals.current_name = filename
    set_volume(1.0)


def play(loops=0, start=0.0):
    if _globals.current is not None:
        mixer_lib.Mix_PlayMusic(_globals.current, loops)
        if start > 0.0:
            set_pos(start)


def rewind():
    if get_busy():
        mixer_lib.Mix_RewindMusic()


def stop():
    if get_busy():
        mixer_lib.Mix_HaltMusic()


def pause():
    if get_busy():
        mixer_lib.Mix_PauseMusic()


def unpause():
    if get_busy() and mixer_lib.Mix_PausedMusic():
        mixer_lib.Mix_ResumeMusic()


def fadeout(ms):
    if get_busy():
        mixer_lib.Mix_FadeOutMusic(ms)


def set_volume(volume):
    if not (0.0 < volume < 1.0):
        volume = 1.0
    v = int(volume * 128)
    mixer_lib.Mix_VolumeMusic(v)


def get_volume(volume):
    mixer_lib.Mix_VolumeMusic(-1) / 128.0


def get_busy():
    return mixer_lib.Mix_PlayingMusic()


def set_pos(pos):
    if pos > 0.0:
        # TODO: if ogg, flac, etc... see comments in SDL_mixer.h
        mixer_lib.Mix_SetMusicPosition(pos)


def get_pos(pos):
    # TODO: looking at pygame source, I guess this is a non-SDL calculation
    # return ms
    pass


def queue(filename):
    # TODO: this needs better logic and some auto-polling method
    current = _globals.current
    if current is None:
        _globals.current = mixer_lib.Mix_LoadMUS(utf8(filename))
    else:
        # _globals.queued = mixer_lib.Mix_LoadMUS(utf8(filename))
        _globals.queued = utf8(filename)
    if not get_busy():
        play()


def set_endevent(type_):
    _globals.end_event = type_


def get_endevent():
    return _globals.end_event

import mixer
