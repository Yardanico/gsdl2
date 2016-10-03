import sdl

__all__ = [
    'init', 'get_init', 'close', 'fade_out', 'stop', 'pause', 'unpause', 'find_channel', 'set_reserved', 'get_busy',
    'Sound', 'Channel', 'music',
]

import logging

from _sdl.structs import SDLError
from .sdlconstants import MIX_DEFAULT_FORMAT, SDL_INIT_AUDIO
from . import music
from .locals import utf8

from . import music


# log = logging.getLogger(__name__)


def get_init():
    return sdl.wasInit(SDL_INIT_AUDIO)


# {chanid: sound, ...}
_channels = {}


def init(frequency=44100, format=MIX_DEFAULT_FORMAT, channels=2, chunksize=1024):
    if not get_init():
        return
    c = sdl.ffi.cast
    if sdl.mixer.openAudio(c('int', frequency), c('Uint16', format), c('int', channels), c('int', chunksize)) < 0:
        logging.log(logging.ERROR, 'SDL_mixer failed to open audio format {}'.format(format))


# EXPERIMENTAL: enabled callback for pypy 4.0.0
# https://cffi.readthedocs.org/en/latest
#
if True:
    @sdl.ffi.callback('void (*)(int)')
    def _channel_stopped(channel_id):
        # remove channel_id from _channels
        # print('channel_id={}'.format(channel_id))
        if channel_id in _channels:
            channel = _channels[channel_id]
            del _channels[channel_id]
        # TODO: post an event if configured on the Channel
        sdl.mixer.channelFinished(_channel_stopped)
        # # OR #
        # callback = sdl_ffi.callback('void (*)(int)', _channel_stopped)
        # mixer_lib.Mix_ChannelFinished(callback)


def close():
    if get_init():
        sdl.mixer.closeAudio()


def fade_out(ms):
    if not get_init():
        return
        sdl.mixer.fadeOutChannel(-1, ms)


def stop():
    if get_init():
        sdl.mixer.haltChannel(-1)


def pause():
    if get_init():
        sdl.mixer.pause(-1)


def unpause():
    if get_init():
        sdl.mixer.resume(-1)


def find_channel(force=False):
    if not get_init():
        return None

    chan = sdl.mixer.groupAvailable(-1)
    if chan == -1:
        if not force:
            return None
        chan = sdl.mixer.groupOldest(-1)

    return Channel(chan)


def set_reserved(num_channels):
    if not get_init():
        return
    return sdl.mixer.reserveChannels(num_channels)


def set_num_channels(num_channels):
    if not get_init():
        return
    return sdl.mixer.allocateChannels(num_channels)


def get_num_channels():
    if not get_init():
        return
    return sdl.mixer.groupCount(-1)


def get_busy():
    if not get_init():
        return False
    return sdl.mixer.playing(-1)


class Sound(object):
    def __init__(self, filename):
        self.__filename = filename

        self.__sdl_chunk = sdl.mixer.loadWAV_RW(sdl.RWFromFile(utf8(filename), utf8('rb')), 1)
        if self.__sdl_chunk == sdl.ffi.NULL:
            raise SDLError()

    def play(self, loops=0, maxtime=0, fade_ms=0):
        if fade_ms > 0:
            channel_id = sdl.mixer.fadeInChannelTimed(-1, self.__sdl_chunk, loops, fade_ms, maxtime)
        else:
            channel_id = sdl.mixer.playChannelTimed(-1, self.__sdl_chunk, loops, maxtime)

        # TODO: enable for callbacks (see init())
        # channeldata[channelnum].queue = NULL;
        # channeldata[channelnum].sound = self;
        _channels[channel_id] = self

        # make sure volume on this arbitrary channel is set to full
        sdl.mixer.volume(channel_id, 128)

        channel = Channel(channel_id)
        return channel

    def stop(self):
        for c in tuple(_channels):
            if _channels[c] is self and c.get_busy():
                sdl.mixer.haltChannel(c)

    def fadeout(self, ms):
        for c in tuple(_channels):
            if _channels[c] is self and c.get_busy():
                sdl.mixer.fadeOutChannel(c, ms)

    def set_volume(self, volume):
        """0.0 to 1.0"""
        if not (0.0 < volume < 1.0):
            volume = 1.0
            sdl.mixer.volumeChunk(self.__sdl_chunk, int(volume * 128))

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
                sdl.mixer.freeChunk(garbage)
            except Exception as e:
                pass


class Channel(object):
    def __init__(self, channel_id):
        self.__channel_id = channel_id

    def play(self, sound, loops=0, maxtime=0, fade_ms=0):
        if fade_ms > 0:
            sdl.mixer.fadeInChannelTimed(self.__channel_id, sound.sdl_chunk, loops, fade_ms, maxtime)
        else:
            sdl.mixer.playChannelTimed(self.channel_id, sound.sdl_chunk, loops, maxtime)
        return self

    def stop(self):
        if self.get_busy():
            sdl.mixer.haltChannel(self.__channel_id)

    def pause(self):
        if self.get_busy():
            sdl.mixer.pause(self.__channel_id)

    def unpause(self):
        if self.get_busy():
            sdl.mixer.resume(self.__channel_id)

    def fadeout(self, ms):
        if self.get_busy():
            sdl.mixer.fadeOutChannel(self.__channel_id, ms)

    def set_volume(self, volume):
        """0.0 to 1.0"""
        if self.get_busy():
            if not (0.0 < volume < 1.0):
                volume = 1.0
            v = int(volume * 128)
            sdl.mixer.volume(self.__channel_id, v)

    def get_volume(self):
        return sdl.mixer.volume(self.__channel_id, -1) / 128.0

    def get_busy(self):
        return sdl.mixer.playing(self.__channel_id)

    def get_sound(self):
        if not self.get_busy():
            return None
        return _channels[self.__channel_id]

    def queue(self, sound):
        # TODO
        raise NotImplemented

    def get_queue(self):
        # TODO
        raise NotImplemented

    def send_endevent(self, type=None):
        # TODO
        raise NotImplemented

    def get_endevent(self):
        # TODO
        raise NotImplemented

    def __get_channelid(self):
        return self.__channel_id

    channel_id = property(__get_channelid)
