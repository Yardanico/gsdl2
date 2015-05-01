__all__ = [
    'init', 'get_init', 'close', 'fade_out', 'stop', 'pause', 'unpause', 'find_channel', 'set_reserved', 'get_busy',
    'Sound', 'Channel', 'music',
]


import sys
import logging

from .sdllibs import mixer_lib, sdl_lib, SDLError
from .sdlffi import sdl_ffi, mixer_ffi
from .sdlconstants import MIX_DEFAULT_FORMAT, SDL_INIT_AUDIO
from . import music
from .locals import utf8


log = logging.getLogger(__name__)


def get_init():
    return sdl_lib.SDL_WasInit(SDL_INIT_AUDIO)


# {chanid: sound, ...}
_channels = {}


def init(frequency=44100, format=MIX_DEFAULT_FORMAT, channels=2, chunksize=1024):
    if not get_init():
        return
    if mixer_lib.Mix_OpenAudio(frequency, format, channels, chunksize) < 0:
        logging.log(logging.ERROR, 'SDL_mixer failed to open audio format {}'.format(format))
    else:
        # TODO: this segfaults on Python 27 whether using decorator or ffi.callback(func)
        # @sdl_ffi.callback('void (*)(int)')
        def _channel_stopped(channel_id):
            # remove channel_id from _channels
            if channel_id in _channels:
                del _channels[channel_id]
            # TODO: post an event if configured on the Channel
        # mixer_lib.Mix_ChannelFinished(_channel_stopped)
        # # OR #
        # callback = sdl_ffi.callback('void (*)(int)', _channel_stopped)
        # mixer_lib.Mix_ChannelFinished(callback)
        pass


def close():
    if get_init():
        mixer_lib.Mix_CloseAudio()


def fade_out(ms):
    if not get_init():
        return
    mixer_lib.Mix_FadeOutChannel(-1, ms)


def stop():
    if get_init():
        mixer_lib.Mix_HaltChannel(-1)


def pause():
    if get_init():
        mixer_lib.Mix_Pause(-1)


def unpause():
    if get_init():
        mixer_lib.Mix_Resume(-1)


def find_channel(force=False):
    if not get_init():
        return None

    chan = mixer_lib.Mix_GroupAvailable(-1)
    if chan == -1:
        if not force:
            return None
        chan = mixer_lib.Mix_GroupOldest(-1)

    return Channel(chan)


def set_reserved(num_channels):
    if not get_init():
        return
    return mixer_lib.Mix_ReserveChannels(num_channels)


def get_busy():
    if not get_init():
        return False
    return mixer_lib.Mix_Playing(-1)


class Sound(object):

    def __init__(self, filename):
        self.__filename = filename

        self.__sdl_chunk = mixer_lib.Mix_LoadWAV_RW(sdl_lib.SDL_RWFromFile(utf8(filename), utf8('rb')), 1)
        if self.__sdl_chunk == sdl_ffi.NULL:
            raise SDLError()

    def play(self, loops=0, maxtime=0, fade_ms=0):
        if fade_ms > 0:
            channel_id = mixer_lib.Mix_FadeInChannelTimed(-1, self.__sdl_chunk, loops, fade_ms, maxtime)
        else:
            channel_id = mixer_lib.Mix_PlayChannelTimed(-1, self.__sdl_chunk, loops, maxtime)

        # TODO:
        # channeldata[channelnum].queue = NULL;
        # channeldata[channelnum].sound = self;
        _channels[channel_id] = self

        # make sure volume on this arbitrary channel is set to full
        mixer_lib.Mix_Volume(channel_id, 128)

        channel = Channel(channel_id)
        return channel

    def stop(self):
        for c in tuple(_channels):
            if _channels[c] is self and c.get_busy():
                mixer_lib.Mix_HaltChannel(c)

    def fadeout(self, ms):
        for c in tuple(_channels):
            if _channels[c] is self and c.get_busy():
                mixer_lib.Mix_FadeOutChannel(c, ms)

    def set_volume(self, volume):
        """0.0 to 1.0"""
        if not (0.0 < volume < 1.0):
            volume = 1.0
        mixer_lib.Mix_VolumeChunk(self.__sdl_chunk, int(volume * 128))

    def get_volume(self):
        return self.__sdl_chunk.volume / 128.0

    def get_num_channels(self):
        return len([c for c in _channels if _channels[c] is self])

    def get_length(self):
        return self.__sdl_chunk.alen

    def get_raw(self):
        return self.__sdl_chunk.abuf

    def __get_filename(self):
        return self.__filename
    filename = property(__get_filename)

    def __get_sdlchunk(self):
        return self.__sdl_chunk
    sdl_chunk = property(__get_sdlchunk)

    def __del__(self):
        # TODO: unreliable
        if self.__sdl_chunk:
            try:
                garbage = self.__sdl_chunk
                self.__sdl_chunk = None
                mixer_lib.Mix_FreeChunk(garbage)
            except Exception as e:
                pass


class Channel(object):

    def __init__(self, channel_id):
        self.__channel_id = channel_id

    def play(self, sound, loops=0, maxtime=0, fade_ms=0):
        if fade_ms > 0:
            mixer_lib.Mix_FadeInChannelTimed(self.__channel_id, sound.sdl_chunk, loops, fade_ms, maxtime)
        else:
            mixer_lib.Mix_PlayChannelTimed(self.channel_id, sound.sdl_chunk, loops, maxtime)
        return self

    def stop(self):
        if self.get_busy():
            mixer_lib.Mix_HaltChannel(self.__channel_id)

    def pause(self):
        if self.get_busy():
            mixer_lib.Mix_Pause(self.__channel_id)

    def unpause(self):
        if self.get_busy():
            mixer_lib.Mix_Resume(self.__channel_id)

    def fadeout(self, ms):
        if self.get_busy():
            mixer_lib.Mix_FadeOutChannel(self.__channel_id, ms)

    def set_volume(self, volume):
        """0.0 to 1.0"""
        if self.get_busy():
            if not (0.0 < volume < 1.0):
                volume = 1.0
            v = int(volume * 128)
            mixer_lib.Mix_Volume(self.__channel_id, v)

    def get_volume(self):
        return mixer_lib.Mix_Volume(self.__channel_id, -1) / 128.0

    def get_busy(self):
        return mixer_lib.Mix_Playing(self.__channel_id)

    def get_sound(self):
        if not self.get_busy():
            return None
        return _channels[self.__channel_id]

    def queue(self, sound):
        raise NotImplemented

    def get_queue(self):
        raise NotImplemented

    def send_endevent(self, type=None):
        raise NotImplemented

    def get_endevent(self):
        raise NotImplemented

    def __get_channelid(self):
        return self.__channel_id
    channel_id = property(__get_channelid)
