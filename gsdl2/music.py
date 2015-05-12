from .sdllibs import mixer_lib
from .locals import utf8


class _globals:

    current = None
    queue = None
    channel = None


def load(filename):
    if get_busy():
        stop()
    _globals.current = mixer_lib.Mix_LoadMUS(utf8(filename))
    _globals.queue = None
    set_volume(1.0)


def play(loops=0, start=0.0):
    if _globals.current:
        _globals.channel = None
        if start > 0.0:
            set_pos(start)
        _globals.channel = mixer_lib.Mix_PlayMusic(_globals.current, loops)


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
    # TODO: this needs some auto-polling method
    if _globals.current is None:
        load(filename)
        play()
    else:
        _globals.queue = mixer_lib.Mix_LoadMUS(utf8(filename))


def set_endevent(type_):
    # TODO: see queue()
    pass


def get_endevent():
    # return type_
    # TODO: see queue()
    pass
