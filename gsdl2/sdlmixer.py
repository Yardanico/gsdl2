#!/usr/bin/env python

__all__ = ['ffi', 'parse_headers']

import re

import cffi

from . import basesdl

ffi = cffi.FFI()
ffi.include(basesdl.ffi)


def parse_headers():
    """segregate C decls and macros into lists
    """
    macros = []
    headers = []

    sdl_defs_list = c_headers.split('\n')
    for line in sdl_defs_list:
        if re.match('#', line):
            macros.append(line)
        else:
            headers.append(line)
    return headers, macros


def get_cdefs(ffi):
    """retrieve _parser and _cdef_sources into ffi
    """
    headers, macros = parse_headers()
    ffi.cdef('\n'.join(headers))


c_headers = """
// SDL_mixer.h

const SDL_version * Mix_Linked_Version(void);
typedef enum
{
    MIX_INIT_FLAC        = 0x00000001,
    MIX_INIT_MOD         = 0x00000002,
    MIX_INIT_MODPLUG     = 0x00000004,
    MIX_INIT_MP3         = 0x00000008,
    MIX_INIT_OGG         = 0x00000010,
    MIX_INIT_FLUIDSYNTH  = 0x00000020
} MIX_InitFlags;
int Mix_Init(int flags);
void Mix_Quit(void);
#define MIX_CHANNELS    8
#define MIX_DEFAULT_FREQUENCY   22050
#if SDL_BYTEORDER == SDL_LIL_ENDIAN
#define MIX_DEFAULT_FORMAT  AUDIO_S16LSB
#else
#define MIX_DEFAULT_FORMAT  AUDIO_S16MSB
#endif
#define MIX_DEFAULT_CHANNELS    2
#define MIX_MAX_VOLUME          128 /* Volume of a chunk */
typedef struct Mix_Chunk {
    int allocated;
    Uint8 *abuf;
    Uint32 alen;
    Uint8 volume;       /* Per-sample volume, 0-128 */
} Mix_Chunk;
typedef enum {
    MIX_NO_FADING,
    MIX_FADING_OUT,
    MIX_FADING_IN
} Mix_Fading;
typedef enum {
    MUS_NONE,
    MUS_CMD,
    MUS_WAV,
    MUS_MOD,
    MUS_MID,
    MUS_OGG,
    MUS_MP3,
    MUS_MP3_MAD,
    MUS_FLAC,
    MUS_MODPLUG
} Mix_MusicType;
typedef struct _Mix_Music Mix_Music;
int Mix_OpenAudio(int frequency, Uint16 format, int channels, int chunksize);
int Mix_AllocateChannels(int numchans);
int Mix_QuerySpec(int *frequency,Uint16 *format,int *channels);
Mix_Chunk * Mix_LoadWAV_RW(SDL_RWops *src, int freesrc);
#define Mix_LoadWAV(file)   Mix_LoadWAV_RW(SDL_RWFromFile(file, "rb"), 1)
Mix_Music * Mix_LoadMUS(const char *file);
Mix_Music * Mix_LoadMUS_RW(SDL_RWops *src, int freesrc);
Mix_Music * Mix_LoadMUSType_RW(SDL_RWops *src, Mix_MusicType type, int freesrc);
Mix_Chunk * Mix_QuickLoad_WAV(Uint8 *mem);
Mix_Chunk * Mix_QuickLoad_RAW(Uint8 *mem, Uint32 len);
void Mix_FreeChunk(Mix_Chunk *chunk);
void Mix_FreeMusic(Mix_Music *music);
int Mix_GetNumChunkDecoders(void);
const char * Mix_GetChunkDecoder(int index);
int Mix_GetNumMusicDecoders(void);
const char * Mix_GetMusicDecoder(int index);
Mix_MusicType Mix_GetMusicType(const Mix_Music *music);
void Mix_SetPostMix(void (*mix_func)(void *udata, Uint8 *stream, int len), void *arg);
void Mix_HookMusic(void (*mix_func)(void *udata, Uint8 *stream, int len), void *arg);
void Mix_HookMusicFinished(void (*music_finished)(void));
void * Mix_GetMusicHookData(void);
void Mix_ChannelFinished(void (*channel_finished)(int channel));
#define MIX_CHANNEL_POST  -2
typedef void (*Mix_EffectFunc_t)(int chan, void *stream, int len, void *udata);
typedef void (*Mix_EffectDone_t)(int chan, void *udata);
int Mix_RegisterEffect(int chan, Mix_EffectFunc_t f, Mix_EffectDone_t d, void *arg);
int Mix_UnregisterEffect(int channel, Mix_EffectFunc_t f);
int Mix_UnregisterAllEffects(int channel);
#define MIX_EFFECTSMAXSPEED  "MIX_EFFECTSMAXSPEED"
int Mix_SetPanning(int channel, Uint8 left, Uint8 right);
int Mix_SetPosition(int channel, Sint16 angle, Uint8 distance);
int Mix_SetDistance(int channel, Uint8 distance);
int Mix_SetReverb(int channel, Uint8 echo);
int Mix_SetReverseStereo(int channel, int flip);
int Mix_ReserveChannels(int num);
int Mix_GroupChannel(int which, int tag);
int Mix_GroupChannels(int from, int to, int tag);
int Mix_GroupAvailable(int tag);
int Mix_GroupCount(int tag);
int Mix_GroupOldest(int tag);
int Mix_GroupNewer(int tag);
#define Mix_PlayChannel(channel,chunk,loops) Mix_PlayChannelTimed(channel,chunk,loops,-1)
int Mix_PlayChannelTimed(int channel, Mix_Chunk *chunk, int loops, int ticks);
int Mix_PlayMusic(Mix_Music *music, int loops);
int Mix_FadeInMusic(Mix_Music *music, int loops, int ms);
int Mix_FadeInMusicPos(Mix_Music *music, int loops, int ms, double position);
#define Mix_FadeInChannel(channel,chunk,loops,ms) Mix_FadeInChannelTimed(channel,chunk,loops,ms,-1)
int Mix_FadeInChannelTimed(int channel, Mix_Chunk *chunk, int loops, int ms, int ticks);
int Mix_Volume(int channel, int volume);
int Mix_VolumeChunk(Mix_Chunk *chunk, int volume);
int Mix_VolumeMusic(int volume);
int Mix_HaltChannel(int channel);
int Mix_HaltGroup(int tag);
int Mix_HaltMusic(void);
int Mix_ExpireChannel(int channel, int ticks);
int Mix_FadeOutChannel(int which, int ms);
int Mix_FadeOutGroup(int tag, int ms);
int Mix_FadeOutMusic(int ms);
Mix_Fading Mix_FadingMusic(void);
Mix_Fading Mix_FadingChannel(int which);
void Mix_Pause(int channel);
void Mix_Resume(int channel);
int Mix_Paused(int channel);
void Mix_PauseMusic(void);
void Mix_ResumeMusic(void);
void Mix_RewindMusic(void);
int Mix_PausedMusic(void);
int Mix_SetMusicPosition(double position);
int Mix_Playing(int channel);
int Mix_PlayingMusic(void);
int Mix_SetMusicCMD(const char *command);
int Mix_SetSynchroValue(int value);
int Mix_GetSynchroValue(void);
int Mix_SetSoundFonts(const char *paths);
const char* Mix_GetSoundFonts(void);
int Mix_EachSoundFont(int (*function)(const char*, void*), void *data);
Mix_Chunk * Mix_GetChunk(int channel);
void Mix_CloseAudio(void);
#define Mix_SetError    SDL_SetError
#define Mix_GetError    SDL_GetError


"""

get_cdefs(ffi)
