#!/usr/bin/env python

__all__ = ['ffi', 'parse_headers']


import re

import cffi


ffi = cffi.FFI()


# TODO: wrappers to make ffi.new() and populate the structure
# TODO: ffi isinstance()-like?


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

// std

typedef size_t MAX_SIZE;

// SDL_stdinc.h

typedef struct _FILE FILE;
#define SDL_arraysize(array)    (sizeof(array)/sizeof(array[0]))
#define SDL_TABLESIZE(table)    SDL_arraysize(table)
#define SDL_reinterpret_cast(type, expression) ((type)(expression))
#define SDL_static_cast(type, expression) ((type)(expression))
#define SDL_const_cast(type, expression) ((type)(expression))
#define SDL_FOURCC(A, B, C, D) ((SDL_static_cast(Uint32, SDL_static_cast(Uint8, (A))) << 0) | (SDL_static_cast(Uint32, SDL_static_cast(Uint8, (B))) << 8) | (SDL_static_cast(Uint32, SDL_static_cast(Uint8, (C))) << 16) | (SDL_static_cast(Uint32, SDL_static_cast(Uint8, (D))) << 24))
typedef enum
{
    SDL_FALSE = 0,
    SDL_TRUE = 1
} SDL_bool;
typedef int8_t Sint8;
typedef uint8_t Uint8;
typedef int16_t Sint16;
typedef uint16_t Uint16;
typedef int32_t Sint32;
typedef uint32_t Uint32;
typedef int64_t Sint64;
typedef uint64_t Uint64;
typedef uint32_t va_list;
#define SDL_COMPILE_TIME_ASSERT(name, x) typedef int SDL_dummy_ ## name[(x) * 2 - 1]
typedef enum
{
    DUMMY_ENUM_VALUE
} SDL_DUMMY_ENUM;
void *SDL_malloc(size_t size);
void *SDL_calloc(size_t nmemb, size_t size);
void *SDL_realloc(void *mem, size_t size);
void SDL_free(void *mem);
char *SDL_getenv(const char *name);
int SDL_setenv(const char *name, const char *value, int overwrite);
void SDL_qsort(void *base, size_t nmemb, size_t size, int (*compare) (const void *, const void *));
int SDL_abs(int x);
int SDL_isdigit(int x);
int SDL_isspace(int x);
int SDL_toupper(int x);
int SDL_tolower(int x);
void *SDL_memset(void *dst, int c, size_t len);
#define SDL_zero(x) SDL_memset(&(x), 0, sizeof((x)))
#define SDL_zerop(x) SDL_memset((x), 0, sizeof(*(x)))
void *SDL_memcpy(void *dst, const void *src, size_t len);
void *SDL_memmove(void *dst, const void *src, size_t len);
int SDL_memcmp(const void *s1, const void *s2, size_t len);
size_t SDL_wcslen(const wchar_t *wstr);
size_t SDL_wcslcpy(wchar_t *dst, const wchar_t *src, size_t maxlen);
size_t SDL_wcslcat(wchar_t *dst, const wchar_t *src, size_t maxlen);
size_t SDL_strlen(const char *str);
size_t SDL_strlcpy(char *dst, const char *src, size_t maxlen);
size_t SDL_utf8strlcpy(char *dst, const char *src, size_t dst_bytes);
size_t SDL_strlcat(char *dst, const char *src, size_t maxlen);
char *SDL_strdup(const char *str);
char *SDL_strrev(char *str);
char *SDL_strupr(char *str);
char *SDL_strlwr(char *str);
char *SDL_strchr(const char *str, int c);
char *SDL_strrchr(const char *str, int c);
char *SDL_strstr(const char *haystack, const char *needle);
char *SDL_itoa(int value, char *str, int radix);
char *SDL_uitoa(unsigned int value, char *str, int radix);
char *SDL_ltoa(long value, char *str, int radix);
char *SDL_ultoa(unsigned long value, char *str, int radix);
char *SDL_lltoa(Sint64 value, char *str, int radix);
char *SDL_ulltoa(Uint64 value, char *str, int radix);
int SDL_atoi(const char *str);
double SDL_atof(const char *str);
long SDL_strtol(const char *str, char **endp, int base);
unsigned long SDL_strtoul(const char *str, char **endp, int base);
Sint64 SDL_strtoll(const char *str, char **endp, int base);
Uint64 SDL_strtoull(const char *str, char **endp, int base);
double SDL_strtod(const char *str, char **endp);
int SDL_strcmp(const char *str1, const char *str2);
int SDL_strncmp(const char *str1, const char *str2, size_t maxlen);
int SDL_strcasecmp(const char *str1, const char *str2);
int SDL_strncasecmp(const char *str1, const char *str2, size_t len);
int SDL_sscanf(const char *text, const char *fmt, ...);
int SDL_vsscanf(const char *text, const char *fmt, va_list ap);
int SDL_snprintf(char *text, size_t maxlen, const char *fmt, ...);
int SDL_vsnprintf(char *text, size_t maxlen, const char *fmt, va_list ap);
double SDL_acos(double x);
double SDL_asin(double x);
double SDL_atan(double x);
double SDL_atan2(double x, double y);
double SDL_ceil(double x);
double SDL_copysign(double x, double y);
double SDL_cos(double x);
float SDL_cosf(float x);
double SDL_fabs(double x);
double SDL_floor(double x);
double SDL_log(double x);
double SDL_pow(double x, double y);
double SDL_scalbn(double x, int n);
double SDL_sin(double x);
float SDL_sinf(float x);
double SDL_sqrt(double x);
/* The SDL implementation of iconv() returns these error codes */
#define SDL_ICONV_ERROR     (size_t)-1
#define SDL_ICONV_E2BIG     (size_t)-2
#define SDL_ICONV_EILSEQ    (size_t)-3
#define SDL_ICONV_EINVAL    (size_t)-4
/* SDL_iconv_* are now always real symbols/types, not macros or inlined. */
//typedef struct _SDL_iconv_t *SDL_iconv_t;
//SDL_iconv_t SDL_iconv_open(const char *tocode, const char *fromcode);
//int SDL_iconv_close(SDL_iconv_t cd);
//size_t SDL_iconv(SDL_iconv_t cd, const char **inbuf, size_t * inbytesleft, char **outbuf, size_t * outbytesleft);
//char *SDL_iconv_string(const char *tocode, const char *fromcode, const char *inbuf, size_t inbytesleft);
//#define SDL_iconv_utf8_locale(S)    SDL_iconv_string("", "UTF-8", S, SDL_strlen(S)+1)
//#define SDL_iconv_utf8_ucs2(S)      (Uint16 *)SDL_iconv_string("UCS-2-INTERNAL", "UTF-8", S, SDL_strlen(S)+1)
//#define SDL_iconv_utf8_ucs4(S)      (Uint32 *)SDL_iconv_string("UCS-4-INTERNAL", "UTF-8", S, SDL_strlen(S)+1)

// SDL_main.h

int SDL_main(int argc, char *argv[]);
void SDL_SetMainReady(void);
int SDL_RegisterApp(char *name, Uint32 style, void *hInst);
void SDL_UnregisterApp(void);
int SDL_WinRTRunApp(int (*mainFunction)(int, char **), void * xamlBackgroundPanel);

// assert.h

typedef enum
{
    SDL_ASSERTION_RETRY,  /**< Retry the assert immediately. */
    SDL_ASSERTION_BREAK,  /**< Make the debugger trigger a breakpoint. */
    SDL_ASSERTION_ABORT,  /**< Terminate the program. */
    SDL_ASSERTION_IGNORE,  /**< Ignore the assert. */
    SDL_ASSERTION_ALWAYS_IGNORE  /**< Ignore the assert from now on. */
} SDL_assert_state;
typedef struct SDL_assert_data
{
    int always_ignore;
    unsigned int trigger_count;
    const char *condition;
    const char *filename;
    int linenum;
    const char *function;
    const struct SDL_assert_data *next;
} SDL_assert_data;
typedef SDL_assert_state (*SDL_AssertionHandler)(const SDL_assert_data* data, void* userdata);
/* Never call this directly. Use the SDL_assert* macros. */
// Gumm note: There are many such macros spanning multiple lines. Not gonna tackle those (yet?).
SDL_assert_state SDL_ReportAssertion(SDL_assert_data *, const char *, const char *, int);
void SDL_SetAssertionHandler(SDL_AssertionHandler handler, void *userdata);
SDL_AssertionHandler SDL_GetDefaultAssertionHandler(void);
SDL_AssertionHandler SDL_GetAssertionHandler(void **puserdata);
const SDL_assert_data * SDL_GetAssertionReport(void);
void SDL_ResetAssertionReport(void);

// SDL_atomic.h

typedef int SDL_SpinLock;
SDL_bool SDL_AtomicTryLock(SDL_SpinLock *lock);
void SDL_AtomicLock(SDL_SpinLock *lock);
void SDL_AtomicUnlock(SDL_SpinLock *lock);
typedef struct { int value; } SDL_atomic_t;
SDL_bool SDL_AtomicCAS(SDL_atomic_t *a, int oldval, int newval);
int SDL_AtomicSet(SDL_atomic_t *a, int v);
int SDL_AtomicGet(SDL_atomic_t *a);
int SDL_AtomicAdd(SDL_atomic_t *a, int v);
#define SDL_AtomicIncRef(a)    SDL_AtomicAdd(a, 1)
#define SDL_AtomicDecRef(a)    (SDL_AtomicAdd(a, -1) == 1)
SDL_bool SDL_AtomicCASPtr(void **a, void *oldval, void *newval);
void* SDL_AtomicSetPtr(void **a, void* v);
void* SDL_AtomicGetPtr(void **a);

// SDL_error.h

int SDL_SetError(const char *fmt, ...);
const char *SDL_GetError(void);
void SDL_ClearError(void);
#define SDL_OutOfMemory()   SDL_Error(SDL_ENOMEM)
#define SDL_Unsupported()   SDL_Error(SDL_UNSUPPORTED)
#define SDL_InvalidParamError(param)    SDL_SetError("Parameter '%s' is invalid", (param))
typedef enum
{
    SDL_ENOMEM,
    SDL_EFREAD,
    SDL_EFWRITE,
    SDL_EFSEEK,
    SDL_UNSUPPORTED,
    SDL_LASTERROR
} SDL_errorcode;
int SDL_Error(SDL_errorcode code);

// SDL_mutex.h

#define SDL_MUTEX_TIMEDOUT  1
#define SDL_MUTEX_MAXWAIT   (~(Uint32)0)
struct SDL_mutex;
typedef struct SDL_mutex SDL_mutex;
SDL_mutex *SDL_CreateMutex(void);
#define SDL_mutexP(m)   SDL_LockMutex(m)
int SDL_LockMutex(SDL_mutex * mutex);
int SDL_TryLockMutex(SDL_mutex * mutex);
#define SDL_mutexV(m)   SDL_UnlockMutex(m)
int SDL_UnlockMutex(SDL_mutex * mutex);
void SDL_DestroyMutex(SDL_mutex * mutex);
struct SDL_semaphore;
typedef struct SDL_semaphore SDL_sem;
SDL_sem *SDL_CreateSemaphore(Uint32 initial_value);
void SDL_DestroySemaphore(SDL_sem * sem);
int SDL_SemWait(SDL_sem * sem);
int SDL_SemTryWait(SDL_sem * sem);
int SDL_SemWaitTimeout(SDL_sem * sem, Uint32 ms);
int SDL_SemPost(SDL_sem * sem);
Uint32 SDL_SemValue(SDL_sem * sem);
struct SDL_cond;
typedef struct SDL_cond SDL_cond;
SDL_cond *SDL_CreateCond(void);
void SDL_DestroyCond(SDL_cond * cond);
int SDL_CondSignal(SDL_cond * cond);
int SDL_CondBroadcast(SDL_cond * cond);
int SDL_CondWait(SDL_cond * cond, SDL_mutex * mutex);
int SDL_CondWaitTimeout(SDL_cond * cond, SDL_mutex * mutex, Uint32 ms);

// SDL_thread.h

//   Gumm note: seems nothing of use in here for now.

// SDL_rwops.h

#define SDL_RWOPS_UNKNOWN   0   /* Unknown stream type */
#define SDL_RWOPS_WINFILE   1   /* Win32 file */
#define SDL_RWOPS_STDFILE   2   /* Stdio file */
#define SDL_RWOPS_JNIFILE   3   /* Android asset */
#define SDL_RWOPS_MEMORY    4   /* Memory stream */
#define SDL_RWOPS_MEMORY_RO 5   /* Read-Only memory stream */
typedef struct SDL_RWops
{
    Sint64 ( * size) (struct SDL_RWops * context);
    Sint64 ( * seek) (struct SDL_RWops * context, Sint64 offset, int whence);
    size_t ( * read) (struct SDL_RWops * context, void *ptr, size_t size, size_t maxnum);
    size_t ( * write) (struct SDL_RWops * context, const void *ptr, size_t size, size_t num);
    int ( * close) (struct SDL_RWops * context);
    Uint32 type;
    union
    {
        struct
        {
            SDL_bool autoclose;
            FILE *fp;
        } stdio;
        struct
        {
            Uint8 *base;
            Uint8 *here;
            Uint8 *stop;
        } mem;
        struct
        {
            void *data1;
            void *data2;
        } unknown;
    } hidden;
} SDL_RWops;
SDL_RWops *SDL_RWFromFile(const char *file, const char *mode);
SDL_RWops *SDL_RWFromFP(FILE * fp, SDL_bool autoclose);
SDL_RWops *SDL_RWFromMem(void *mem, int size);
SDL_RWops *SDL_RWFromConstMem(const void *mem, int size);
SDL_RWops *SDL_AllocRW(void);
void SDL_FreeRW(SDL_RWops * area);
#define RW_SEEK_SET 0       /**< Seek from the beginning of data */
#define RW_SEEK_CUR 1       /**< Seek relative to current read point */
#define RW_SEEK_END 2       /**< Seek relative to the end of data */
#define SDL_RWsize(ctx)         (ctx)->size(ctx)
#define SDL_RWseek(ctx, offset, whence) (ctx)->seek(ctx, offset, whence)
#define SDL_RWtell(ctx)         (ctx)->seek(ctx, 0, RW_SEEK_CUR)
#define SDL_RWread(ctx, ptr, size, n)   (ctx)->read(ctx, ptr, size, n)
#define SDL_RWwrite(ctx, ptr, size, n)  (ctx)->write(ctx, ptr, size, n)
#define SDL_RWclose(ctx)        (ctx)->close(ctx)
Uint8 SDL_ReadU8(SDL_RWops * src);
Uint16 SDL_ReadLE16(SDL_RWops * src);
Uint16 SDL_ReadBE16(SDL_RWops * src);
Uint32 SDL_ReadLE32(SDL_RWops * src);
Uint32 SDL_ReadBE32(SDL_RWops * src);
Uint64 SDL_ReadLE64(SDL_RWops * src);
Uint64 SDL_ReadBE64(SDL_RWops * src);
size_t SDL_WriteU8(SDL_RWops * dst, Uint8 value);
size_t SDL_WriteLE16(SDL_RWops * dst, Uint16 value);
size_t SDL_WriteBE16(SDL_RWops * dst, Uint16 value);
size_t SDL_WriteLE32(SDL_RWops * dst, Uint32 value);
size_t SDL_WriteBE32(SDL_RWops * dst, Uint32 value);
size_t SDL_WriteLE64(SDL_RWops * dst, Uint64 value);
size_t SDL_WriteBE64(SDL_RWops * dst, Uint64 value);

// SDL_audio.h

typedef Uint16 SDL_AudioFormat;
#define SDL_AUDIO_MASK_BITSIZE       (0xFF)
#define SDL_AUDIO_MASK_DATATYPE      (1<<8)
#define SDL_AUDIO_MASK_ENDIAN        (1<<12)
#define SDL_AUDIO_MASK_SIGNED        (1<<15)
#define SDL_AUDIO_BITSIZE(x)         (x & SDL_AUDIO_MASK_BITSIZE)
#define SDL_AUDIO_ISFLOAT(x)         (x & SDL_AUDIO_MASK_DATATYPE)
#define SDL_AUDIO_ISBIGENDIAN(x)     (x & SDL_AUDIO_MASK_ENDIAN)
#define SDL_AUDIO_ISSIGNED(x)        (x & SDL_AUDIO_MASK_SIGNED)
#define SDL_AUDIO_ISINT(x)           (!SDL_AUDIO_ISFLOAT(x))
#define SDL_AUDIO_ISLITTLEENDIAN(x)  (!SDL_AUDIO_ISBIGENDIAN(x))
#define SDL_AUDIO_ISUNSIGNED(x)      (!SDL_AUDIO_ISSIGNED(x))
#define AUDIO_U8        0x0008  /**< Unsigned 8-bit samples */
#define AUDIO_S8        0x8008  /**< Signed 8-bit samples */
#define AUDIO_U16LSB    0x0010  /**< Unsigned 16-bit samples */
#define AUDIO_S16LSB    0x8010  /**< Signed 16-bit samples */
#define AUDIO_U16MSB    0x1010  /**< As above, but big-endian byte order */
#define AUDIO_S16MSB    0x9010  /**< As above, but big-endian byte order */
#define AUDIO_U16       AUDIO_U16LSB
#define AUDIO_S16       AUDIO_S16LSB
#define AUDIO_S32LSB    0x8020  /**< 32-bit integer samples */
#define AUDIO_S32MSB    0x9020  /**< As above, but big-endian byte order */
#define AUDIO_S32       AUDIO_S32LSB
#define AUDIO_F32LSB    0x8120  /**< 32-bit floating point samples */
#define AUDIO_F32MSB    0x9120  /**< As above, but big-endian byte order */
#define AUDIO_F32       AUDIO_F32LSB
#define SDL_AUDIO_ALLOW_FREQUENCY_CHANGE    0x00000001
#define SDL_AUDIO_ALLOW_FORMAT_CHANGE       0x00000002
#define SDL_AUDIO_ALLOW_CHANNELS_CHANGE     0x00000004
#define SDL_AUDIO_ALLOW_ANY_CHANGE          (SDL_AUDIO_ALLOW_FREQUENCY_CHANGE|SDL_AUDIO_ALLOW_FORMAT_CHANGE|SDL_AUDIO_ALLOW_CHANNELS_CHANGE)
typedef void (* SDL_AudioCallback) (void *userdata, Uint8 * stream, int len);
typedef struct SDL_AudioSpec
{
    int freq;                   /**< DSP frequency -- samples per second */
    SDL_AudioFormat format;     /**< Audio data format */
    Uint8 channels;             /**< Number of channels: 1 mono, 2 stereo */
    Uint8 silence;              /**< Audio buffer silence value (calculated) */
    Uint16 samples;             /**< Audio buffer size in samples (power of 2) */
    Uint16 padding;             /**< Necessary for some compile environments */
    Uint32 size;                /**< Audio buffer size in bytes (calculated) */
    SDL_AudioCallback callback;
    void *userdata;
} SDL_AudioSpec;
struct SDL_AudioCVT;
typedef void (* SDL_AudioFilter) (struct SDL_AudioCVT * cvt, SDL_AudioFormat format);
typedef struct SDL_AudioCVT
{
    int needed;                 /**< Set to 1 if conversion possible */
    SDL_AudioFormat src_format; /**< Source audio format */
    SDL_AudioFormat dst_format; /**< Target audio format */
    double rate_incr;           /**< Rate conversion increment */
    Uint8 *buf;                 /**< Buffer to hold entire audio data */
    int len;                    /**< Length of original audio buffer */
    int len_cvt;                /**< Length of converted audio buffer */
    int len_mult;               /**< buffer must be len*len_mult big */
    double len_ratio;           /**< Given len, final size is len*len_ratio */
    SDL_AudioFilter filters[10];        /**< Filter list */
    int filter_index;           /**< Current audio conversion function */
} SDL_AudioCVT;
int SDL_GetNumAudioDrivers(void);
const char *SDL_GetAudioDriver(int index);
int SDL_AudioInit(const char *driver_name);
void SDL_AudioQuit(void);
const char *SDL_GetCurrentAudioDriver(void);
int SDL_OpenAudio(SDL_AudioSpec * desired, SDL_AudioSpec * obtained);
typedef Uint32 SDL_AudioDeviceID;
int SDL_GetNumAudioDevices(int iscapture);
const char *SDL_GetAudioDeviceName(int index, int iscapture);
SDL_AudioDeviceID SDL_OpenAudioDevice(const char *device, int iscapture, const SDL_AudioSpec * desired, SDL_AudioSpec * obtained, int allowed_changes);
typedef enum
{
    SDL_AUDIO_STOPPED = 0,
    SDL_AUDIO_PLAYING,
    SDL_AUDIO_PAUSED
} SDL_AudioStatus;
SDL_AudioStatus SDL_GetAudioStatus(void);
SDL_AudioStatus SDLCALL;
SDL_AudioStatus SDL_GetAudioDeviceStatus(SDL_AudioDeviceID dev);
void SDL_PauseAudio(int pause_on);
void SDL_PauseAudioDevice(SDL_AudioDeviceID dev, int pause_on);
SDL_AudioSpec *SDL_LoadWAV_RW(SDL_RWops * src, int freesrc, SDL_AudioSpec * spec, Uint8 ** audio_buf, Uint32 * audio_len);
#define SDL_LoadWAV(file, spec, audio_buf, audio_len) SDL_LoadWAV_RW(SDL_RWFromFile(file, "rb"),1, spec,audio_buf,audio_len)
void SDL_FreeWAV(Uint8 * audio_buf);
int SDL_BuildAudioCVT(SDL_AudioCVT * cvt, SDL_AudioFormat src_format, Uint8 src_channels, int src_rate, SDL_AudioFormat dst_format, Uint8 dst_channels, int dst_rate);
int SDL_ConvertAudio(SDL_AudioCVT * cvt);
void SDL_MixAudio(Uint8 * dst, const Uint8 * src, Uint32 len, int volume);
void SDL_MixAudioFormat(Uint8 * dst, const Uint8 * src, SDL_AudioFormat format, Uint32 len, int volume);
void SDL_LockAudio(void);
void SDL_LockAudioDevice(SDL_AudioDeviceID dev);
void SDL_UnlockAudio(void);
void SDL_UnlockAudioDevice(SDL_AudioDeviceID dev);
void SDL_CloseAudio(void);
void SDL_CloseAudioDevice(SDL_AudioDeviceID dev);

// SDL_clipboard.h

int SDL_SetClipboardText(const char *text);
char * SDL_GetClipboardText(void);
SDL_bool SDL_HasClipboardText(void);

// SDL_cpuinfo.h

#define SDL_CACHELINE_SIZE  128
int SDL_GetCPUCount(void);
int SDL_GetCPUCacheLineSize(void);
SDL_bool SDL_HasRDTSC(void);
SDL_bool SDL_HasAltiVec(void);
SDL_bool SDL_HasMMX(void);
SDL_bool SDL_Has3DNow(void);
SDL_bool SDL_HasSSE(void);
SDL_bool SDL_HasSSE2(void);
SDL_bool SDL_HasSSE3(void);
SDL_bool SDL_HasSSE41(void);
SDL_bool SDL_HasSSE42(void);
SDL_bool SDL_HasAVX(void);
int SDL_GetSystemRAM(void);

// SDL_endian.h

//    Gumm note: tons of macros in here. Skipping for now.

// SDL_pixels.h

#define SDL_ALPHA_OPAQUE 255
#define SDL_ALPHA_TRANSPARENT 0
enum
{
    SDL_PIXELTYPE_UNKNOWN,
    SDL_PIXELTYPE_INDEX1,
    SDL_PIXELTYPE_INDEX4,
    SDL_PIXELTYPE_INDEX8,
    SDL_PIXELTYPE_PACKED8,
    SDL_PIXELTYPE_PACKED16,
    SDL_PIXELTYPE_PACKED32,
    SDL_PIXELTYPE_ARRAYU8,
    SDL_PIXELTYPE_ARRAYU16,
    SDL_PIXELTYPE_ARRAYU32,
    SDL_PIXELTYPE_ARRAYF16,
    SDL_PIXELTYPE_ARRAYF32
};
enum
{
    SDL_BITMAPORDER_NONE,
    SDL_BITMAPORDER_4321,
    SDL_BITMAPORDER_1234
};
enum
{
    SDL_PACKEDORDER_NONE,
    SDL_PACKEDORDER_XRGB,
    SDL_PACKEDORDER_RGBX,
    SDL_PACKEDORDER_ARGB,
    SDL_PACKEDORDER_RGBA,
    SDL_PACKEDORDER_XBGR,
    SDL_PACKEDORDER_BGRX,
    SDL_PACKEDORDER_ABGR,
    SDL_PACKEDORDER_BGRA
};
enum
{
    SDL_ARRAYORDER_NONE,
    SDL_ARRAYORDER_RGB,
    SDL_ARRAYORDER_RGBA,
    SDL_ARRAYORDER_ARGB,
    SDL_ARRAYORDER_BGR,
    SDL_ARRAYORDER_BGRA,
    SDL_ARRAYORDER_ABGR
};
enum
{
    SDL_PACKEDLAYOUT_NONE,
    SDL_PACKEDLAYOUT_332,
    SDL_PACKEDLAYOUT_4444,
    SDL_PACKEDLAYOUT_1555,
    SDL_PACKEDLAYOUT_5551,
    SDL_PACKEDLAYOUT_565,
    SDL_PACKEDLAYOUT_8888,
    SDL_PACKEDLAYOUT_2101010,
    SDL_PACKEDLAYOUT_1010102
};
#define SDL_DEFINE_PIXELFOURCC(A, B, C, D) SDL_FOURCC(A, B, C, D)
#define SDL_DEFINE_PIXELFORMAT(type, order, layout, bits, bytes) ((1 << 28) | ((type) << 24) | ((order) << 20) | ((layout) << 16) | ((bits) << 8) | ((bytes) << 0))
#define SDL_PIXELFLAG(X)    (((X) >> 28) & 0x0F)
#define SDL_PIXELTYPE(X)    (((X) >> 24) & 0x0F)
#define SDL_PIXELORDER(X)   (((X) >> 20) & 0x0F)
#define SDL_PIXELLAYOUT(X)  (((X) >> 16) & 0x0F)
#define SDL_BITSPERPIXEL(X) (((X) >> 8) & 0xFF)
#define SDL_BYTESPERPIXEL(X) (SDL_ISPIXELFORMAT_FOURCC(X) ? ((((X) == SDL_PIXELFORMAT_YUY2) || ((X) == SDL_PIXELFORMAT_UYVY) || ((X) == SDL_PIXELFORMAT_YVYU)) ? 2 : 1) : (((X) >> 0) & 0xFF))
#define SDL_ISPIXELFORMAT_INDEXED(format)   (!SDL_ISPIXELFORMAT_FOURCC(format) && ((SDL_PIXELTYPE(format) == SDL_PIXELTYPE_INDEX1) || (SDL_PIXELTYPE(format) == SDL_PIXELTYPE_INDEX4) || (SDL_PIXELTYPE(format) == SDL_PIXELTYPE_INDEX8)))
#define SDL_ISPIXELFORMAT_ALPHA(format) (!SDL_ISPIXELFORMAT_FOURCC(format) && ((SDL_PIXELORDER(format) == SDL_PACKEDORDER_ARGB) || (SDL_PIXELORDER(format) == SDL_PACKEDORDER_RGBA) || (SDL_PIXELORDER(format) == SDL_PACKEDORDER_ABGR) || (SDL_PIXELORDER(format) == SDL_PACKEDORDER_BGRA)))
#define SDL_ISPIXELFORMAT_FOURCC(format) ((format) && (SDL_PIXELFLAG(format) != 1))
enum
{
    // Gumm note: had to comment these macros. They are not gonna turn out right.
    SDL_PIXELFORMAT_UNKNOWN,
    SDL_PIXELFORMAT_INDEX1LSB, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_INDEX1, SDL_BITMAPORDER_4321, 0, 1, 0), */
    SDL_PIXELFORMAT_INDEX1MSB, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_INDEX1, SDL_BITMAPORDER_1234, 0, 1, 0), */
    SDL_PIXELFORMAT_INDEX4LSB, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_INDEX4, SDL_BITMAPORDER_4321, 0, 4, 0), */
    SDL_PIXELFORMAT_INDEX4MSB, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_INDEX4, SDL_BITMAPORDER_1234, 0, 4, 0), */
    SDL_PIXELFORMAT_INDEX8, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_INDEX8, 0, 0, 8, 1), */
    SDL_PIXELFORMAT_RGB332, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED8, SDL_PACKEDORDER_XRGB, SDL_PACKEDLAYOUT_332, 8, 1), */
    SDL_PIXELFORMAT_RGB444, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED16, SDL_PACKEDORDER_XRGB, SDL_PACKEDLAYOUT_4444, 12, 2), */
    SDL_PIXELFORMAT_RGB555, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED16, SDL_PACKEDORDER_XRGB, SDL_PACKEDLAYOUT_1555, 15, 2), */
    SDL_PIXELFORMAT_BGR555, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED16, SDL_PACKEDORDER_XBGR, SDL_PACKEDLAYOUT_1555, 15, 2), */
    SDL_PIXELFORMAT_ARGB4444, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED16, SDL_PACKEDORDER_ARGB, SDL_PACKEDLAYOUT_4444, 16, 2), */
    SDL_PIXELFORMAT_RGBA4444, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED16, SDL_PACKEDORDER_RGBA, SDL_PACKEDLAYOUT_4444, 16, 2), */
    SDL_PIXELFORMAT_ABGR4444, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED16, SDL_PACKEDORDER_ABGR, SDL_PACKEDLAYOUT_4444, 16, 2), */
    SDL_PIXELFORMAT_BGRA4444, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED16, SDL_PACKEDORDER_BGRA, SDL_PACKEDLAYOUT_4444, 16, 2), */
    SDL_PIXELFORMAT_ARGB1555, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED16, SDL_PACKEDORDER_ARGB, SDL_PACKEDLAYOUT_1555, 16, 2), */
    SDL_PIXELFORMAT_RGBA5551, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED16, SDL_PACKEDORDER_RGBA, SDL_PACKEDLAYOUT_5551, 16, 2), */
    SDL_PIXELFORMAT_ABGR1555, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED16, SDL_PACKEDORDER_ABGR, SDL_PACKEDLAYOUT_1555, 16, 2), */
    SDL_PIXELFORMAT_BGRA5551, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED16, SDL_PACKEDORDER_BGRA, SDL_PACKEDLAYOUT_5551, 16, 2), */
    SDL_PIXELFORMAT_RGB565, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED16, SDL_PACKEDORDER_XRGB, SDL_PACKEDLAYOUT_565, 16, 2), */
    SDL_PIXELFORMAT_BGR565, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED16, SDL_PACKEDORDER_XBGR, SDL_PACKEDLAYOUT_565, 16, 2), */
    SDL_PIXELFORMAT_RGB24, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_ARRAYU8, SDL_ARRAYORDER_RGB, 0, 24, 3), */
    SDL_PIXELFORMAT_BGR24, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_ARRAYU8, SDL_ARRAYORDER_BGR, 0, 24, 3), */
    SDL_PIXELFORMAT_RGB888, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED32, SDL_PACKEDORDER_XRGB, SDL_PACKEDLAYOUT_8888, 24, 4), */
    SDL_PIXELFORMAT_RGBX8888, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED32, SDL_PACKEDORDER_RGBX, SDL_PACKEDLAYOUT_8888, 24, 4), */
    SDL_PIXELFORMAT_BGR888, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED32, SDL_PACKEDORDER_XBGR, SDL_PACKEDLAYOUT_8888, 24, 4), */
    SDL_PIXELFORMAT_BGRX8888, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED32, SDL_PACKEDORDER_BGRX, SDL_PACKEDLAYOUT_8888, 24, 4), */
    SDL_PIXELFORMAT_ARGB8888, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED32, SDL_PACKEDORDER_ARGB, SDL_PACKEDLAYOUT_8888, 32, 4), */
    SDL_PIXELFORMAT_RGBA8888, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED32, SDL_PACKEDORDER_RGBA, SDL_PACKEDLAYOUT_8888, 32, 4), */
    SDL_PIXELFORMAT_ABGR8888, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED32, SDL_PACKEDORDER_ABGR, SDL_PACKEDLAYOUT_8888, 32, 4), */
    SDL_PIXELFORMAT_BGRA8888, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED32, SDL_PACKEDORDER_BGRA, SDL_PACKEDLAYOUT_8888, 32, 4), */
    SDL_PIXELFORMAT_ARGB2101010, /* = SDL_DEFINE_PIXELFORMAT(SDL_PIXELTYPE_PACKED32, SDL_PACKEDORDER_ARGB, SDL_PACKEDLAYOUT_2101010, 32, 4), */
    SDL_PIXELFORMAT_YV12, /* = SDL_DEFINE_PIXELFOURCC('Y', 'V', '1', '2'), */
    SDL_PIXELFORMAT_IYUV, /* = SDL_DEFINE_PIXELFOURCC('I', 'Y', 'U', 'V'), */
    SDL_PIXELFORMAT_YUY2, /* = SDL_DEFINE_PIXELFOURCC('Y', 'U', 'Y', '2'), */
    SDL_PIXELFORMAT_UYVY, /* = SDL_DEFINE_PIXELFOURCC('U', 'Y', 'V', 'Y'), */
    SDL_PIXELFORMAT_YVYU, /* = SDL_DEFINE_PIXELFOURCC('Y', 'V', 'Y', 'U') */
};
typedef struct SDL_Color
{
    Uint8 r;
    Uint8 g;
    Uint8 b;
    Uint8 a;
} SDL_Color;
#define SDL_Colour SDL_Color
typedef struct SDL_Palette
{
    int ncolors;
    SDL_Color *colors;
    Uint32 version;
    int refcount;
} SDL_Palette;
typedef struct SDL_PixelFormat
{
    Uint32 format;
    SDL_Palette *palette;
    Uint8 BitsPerPixel;
    Uint8 BytesPerPixel;
    Uint8 padding[2];
    Uint32 Rmask;
    Uint32 Gmask;
    Uint32 Bmask;
    Uint32 Amask;
    Uint8 Rloss;
    Uint8 Gloss;
    Uint8 Bloss;
    Uint8 Aloss;
    Uint8 Rshift;
    Uint8 Gshift;
    Uint8 Bshift;
    Uint8 Ashift;
    int refcount;
    struct SDL_PixelFormat *next;
} SDL_PixelFormat;
const char* SDL_GetPixelFormatName(Uint32 format);
SDL_bool SDL_PixelFormatEnumToMasks(Uint32 format, int *bpp, Uint32 * Rmask, Uint32 * Gmask, Uint32 * Bmask, Uint32 * Amask);
Uint32 SDL_MasksToPixelFormatEnum(int bpp, Uint32 Rmask, Uint32 Gmask, Uint32 Bmask, Uint32 Amask);
SDL_PixelFormat * SDL_AllocFormat(Uint32 pixel_format);
void SDL_FreeFormat(SDL_PixelFormat *format);
SDL_Palette *SDL_AllocPalette(int ncolors);
int SDL_SetPixelFormatPalette(SDL_PixelFormat * format, SDL_Palette *palette);
int SDL_SetPaletteColors(SDL_Palette * palette, const SDL_Color * colors, int firstcolor, int ncolors);
void SDL_FreePalette(SDL_Palette * palette);
Uint32 SDL_MapRGB(const SDL_PixelFormat * format, Uint8 r, Uint8 g, Uint8 b);
Uint32 SDL_MapRGBA(const SDL_PixelFormat * format, Uint8 r, Uint8 g, Uint8 b, Uint8 a);
void SDL_GetRGB(Uint32 pixel, const SDL_PixelFormat * format, Uint8 * r, Uint8 * g, Uint8 * b);
void SDL_GetRGBA(Uint32 pixel, const SDL_PixelFormat * format, Uint8 * r, Uint8 * g, Uint8 * b, Uint8 * a);
void SDL_CalculateGammaRamp(float gamma, Uint16 * ramp);

// SDL_rect.h

typedef struct SDL_Point
{
    int x;
    int y;
} SDL_Point;
typedef struct SDL_Rect
{
    int x, y;
    int w, h;
} SDL_Rect;
/* Gumm note: Inline. Argh.
SDL_bool SDL_RectEmpty(const SDL_Rect *r)
{
    return ((!r) || (r->w <= 0) || (r->h <= 0)) ? SDL_TRUE : SDL_FALSE;
}
SDL_bool SDL_RectEquals(const SDL_Rect *a, const SDL_Rect *b)
{
    return (a && b && (a->x == b->x) && (a->y == b->y) &&
            (a->w == b->w) && (a->h == b->h)) ? SDL_TRUE : SDL_FALSE;
}
*/
SDL_bool SDL_HasIntersection(const SDL_Rect * A, const SDL_Rect * B);
SDL_bool SDL_IntersectRect(const SDL_Rect * A, const SDL_Rect * B, SDL_Rect * result);
void SDL_UnionRect(const SDL_Rect * A, const SDL_Rect * B, SDL_Rect * result);
SDL_bool SDL_EnclosePoints(const SDL_Point * points, int count, const SDL_Rect * clip, SDL_Rect * result);
SDL_bool SDL_IntersectRectAndLine(const SDL_Rect * rect, int *X1, int *Y1, int *X2, int *Y2);

// SDL_blendmode.h

typedef enum
{
    SDL_BLENDMODE_NONE = 0x00000000,     /**< no blending: dstRGBA = srcRGBA */
    SDL_BLENDMODE_BLEND = 0x00000001,    /**< alpha blending: dstRGB = (srcRGB * srcA) + (dstRGB * (1-srcA)); dstA = srcA + (dstA * (1-srcA)) */
    SDL_BLENDMODE_ADD = 0x00000002,      /**< additive blending: dstRGB = (srcRGB * srcA) + dstRGB; dstA = dstA */
    SDL_BLENDMODE_MOD = 0x00000004       /**< color modulate: dstRGB = srcRGB * dstRGB; dstA = dstA */
} SDL_BlendMode;

// SDL_surface.h

#define SDL_SWSURFACE       0           /**< Just here for compatibility */
#define SDL_PREALLOC        0x00000001  /**< Surface uses preallocated memory */
#define SDL_RLEACCEL        0x00000002  /**< Surface is RLE encoded */
#define SDL_DONTFREE        0x00000004  /**< Surface is referenced internally */
#define SDL_MUSTLOCK(S) (((S)->flags & SDL_RLEACCEL) != 0)
typedef struct SDL_Surface
{
    Uint32 flags;               /**< Read-only */
    SDL_PixelFormat *format;    /**< Read-only */
    int w, h;                   /**< Read-only */
    int pitch;                  /**< Read-only */
    void *pixels;               /**< Read-write */
    void *userdata;             /**< Read-write */
    int locked;                 /**< Read-only */
    void *lock_data;            /**< Read-only */
    SDL_Rect clip_rect;         /**< Read-only */
    struct SDL_BlitMap *map;    /**< Private */
    int refcount;               /**< Read-mostly */
} SDL_Surface;
typedef int (*SDL_blit) (struct SDL_Surface * src, SDL_Rect * srcrect, struct SDL_Surface * dst, SDL_Rect * dstrect);
SDL_Surface *SDL_CreateRGBSurface(Uint32 flags, int width, int height, int depth, Uint32 Rmask, Uint32 Gmask, Uint32 Bmask, Uint32 Amask);
SDL_Surface *SDL_CreateRGBSurfaceFrom(void *pixels, int width, int height, int depth, int pitch, Uint32 Rmask, Uint32 Gmask, Uint32 Bmask, Uint32 Amask);
void SDL_FreeSurface(SDL_Surface * surface);
int SDL_SetSurfacePalette(SDL_Surface * surface, SDL_Palette * palette);
int SDL_LockSurface(SDL_Surface * surface);
void SDL_UnlockSurface(SDL_Surface * surface);
SDL_Surface *SDL_LoadBMP_RW(SDL_RWops * src, int freesrc);
#define SDL_LoadBMP(file)   SDL_LoadBMP_RW(SDL_RWFromFile(file, "rb"), 1)
int SDL_SaveBMP_RW (SDL_Surface * surface, SDL_RWops * dst, int freedst);
#define SDL_SaveBMP(surface, file) SDL_SaveBMP_RW(surface, SDL_RWFromFile(file, "wb"), 1)
int SDL_SetSurfaceRLE(SDL_Surface * surface, int flag);
int SDL_SetColorKey(SDL_Surface * surface, int flag, Uint32 key);
int SDL_GetColorKey(SDL_Surface * surface, Uint32 * key);
int SDL_SetSurfaceColorMod(SDL_Surface * surface, Uint8 r, Uint8 g, Uint8 b);
int SDL_GetSurfaceColorMod(SDL_Surface * surface, Uint8 * r, Uint8 * g, Uint8 * b);
int SDL_SetSurfaceAlphaMod(SDL_Surface * surface, Uint8 alpha);
int SDL_GetSurfaceAlphaMod(SDL_Surface * surface, Uint8 * alpha);
int SDL_SetSurfaceBlendMode(SDL_Surface * surface, SDL_BlendMode blendMode);
int SDL_GetSurfaceBlendMode(SDL_Surface * surface, SDL_BlendMode *blendMode);
SDL_bool SDL_SetClipRect(SDL_Surface * surface, const SDL_Rect * rect);
void SDL_GetClipRect(SDL_Surface * surface, SDL_Rect * rect);
SDL_Surface *SDL_ConvertSurface(SDL_Surface * src, const SDL_PixelFormat * fmt, Uint32 flags);
SDL_Surface *SDL_ConvertSurfaceFormat(SDL_Surface * src, Uint32 pixel_format, Uint32 flags);
int SDL_ConvertPixels(int width, int height, Uint32 src_format, const void * src, int src_pitch, Uint32 dst_format, void * dst, int dst_pitch);
int SDL_FillRect (SDL_Surface * dst, const SDL_Rect * rect, Uint32 color);
int SDL_FillRects(SDL_Surface * dst, const SDL_Rect * rects, int count, Uint32 color);
#define SDL_BlitSurface SDL_UpperBlit
int SDL_UpperBlit(SDL_Surface * src, const SDL_Rect * srcrect, SDL_Surface * dst, SDL_Rect * dstrect);
int SDL_LowerBlit(SDL_Surface * src, SDL_Rect * srcrect, SDL_Surface * dst, SDL_Rect * dstrect);
int SDL_SoftStretch(SDL_Surface * src, const SDL_Rect * srcrect, SDL_Surface * dst, const SDL_Rect * dstrect);
#define SDL_BlitScaled SDL_UpperBlitScaled
int SDL_UpperBlitScaled(SDL_Surface * src, const SDL_Rect * srcrect, SDL_Surface * dst, SDL_Rect * dstrect);
int SDL_LowerBlitScaled(SDL_Surface * src, SDL_Rect * srcrect, SDL_Surface * dst, SDL_Rect * dstrect);

// SDL_video.h

typedef struct
{
    Uint32 format;              /**< pixel format */
    int w;                      /**< width */
    int h;                      /**< height */
    int refresh_rate;           /**< refresh rate (or zero for unspecified) */
    void *driverdata;           /**< driver-specific data, initialize to 0 */
} SDL_DisplayMode;
typedef struct SDL_Window SDL_Window;
typedef enum
{
    SDL_WINDOW_FULLSCREEN = 0x00000001,         /**< fullscreen window */
    SDL_WINDOW_OPENGL = 0x00000002,             /**< window usable with OpenGL context */
    SDL_WINDOW_SHOWN = 0x00000004,              /**< window is visible */
    SDL_WINDOW_HIDDEN = 0x00000008,             /**< window is not visible */
    SDL_WINDOW_BORDERLESS = 0x00000010,         /**< no window decoration */
    SDL_WINDOW_RESIZABLE = 0x00000020,          /**< window can be resized */
    SDL_WINDOW_MINIMIZED = 0x00000040,          /**< window is minimized */
    SDL_WINDOW_MAXIMIZED = 0x00000080,          /**< window is maximized */
    SDL_WINDOW_INPUT_GRABBED = 0x00000100,      /**< window has grabbed input focus */
    SDL_WINDOW_INPUT_FOCUS = 0x00000200,        /**< window has input focus */
    SDL_WINDOW_MOUSE_FOCUS = 0x00000400,        /**< window has mouse focus */
    SDL_WINDOW_FULLSCREEN_DESKTOP = 0x00001001, /** hacked by Gumm ( SDL_WINDOW_FULLSCREEN | 0x00001000 ), */
    SDL_WINDOW_FOREIGN = 0x00000800,            /**< window not created by SDL */
    SDL_WINDOW_ALLOW_HIGHDPI = 0x00002000       /**< window should be created in high-DPI mode if supported */
} SDL_WindowFlags;
#define SDL_WINDOWPOS_UNDEFINED_MASK    0x1FFF0000
#define SDL_WINDOWPOS_UNDEFINED_DISPLAY(X)  (SDL_WINDOWPOS_UNDEFINED_MASK|(X))
#define SDL_WINDOWPOS_UNDEFINED         SDL_WINDOWPOS_UNDEFINED_DISPLAY(0)
#define SDL_WINDOWPOS_ISUNDEFINED(X)  (((X)&0xFFFF0000) == SDL_WINDOWPOS_UNDEFINED_MASK)
#define SDL_WINDOWPOS_CENTERED_MASK    0x2FFF0000
#define SDL_WINDOWPOS_CENTERED_DISPLAY(X)  (SDL_WINDOWPOS_CENTERED_MASK|(X))
#define SDL_WINDOWPOS_CENTERED         SDL_WINDOWPOS_CENTERED_DISPLAY(0)
#define SDL_WINDOWPOS_ISCENTERED(X)  (((X)&0xFFFF0000) == SDL_WINDOWPOS_CENTERED_MASK)
typedef enum
{
    SDL_WINDOWEVENT_NONE,           /**< Never used */
    SDL_WINDOWEVENT_SHOWN,          /**< Window has been shown */
    SDL_WINDOWEVENT_HIDDEN,         /**< Window has been hidden */
    SDL_WINDOWEVENT_EXPOSED,        /**< Window has been exposed and should be
                                         redrawn */
    SDL_WINDOWEVENT_MOVED,          /**< Window has been moved to data1, data2
                                     */
    SDL_WINDOWEVENT_RESIZED,        /**< Window has been resized to data1xdata2 */
    SDL_WINDOWEVENT_SIZE_CHANGED,   /**< The window size has changed, either as a result of an API call or through the system or user changing the window size. */
    SDL_WINDOWEVENT_MINIMIZED,      /**< Window has been minimized */
    SDL_WINDOWEVENT_MAXIMIZED,      /**< Window has been maximized */
    SDL_WINDOWEVENT_RESTORED,       /**< Window has been restored to normal size
                                         and position */
    SDL_WINDOWEVENT_ENTER,          /**< Window has gained mouse focus */
    SDL_WINDOWEVENT_LEAVE,          /**< Window has lost mouse focus */
    SDL_WINDOWEVENT_FOCUS_GAINED,   /**< Window has gained keyboard focus */
    SDL_WINDOWEVENT_FOCUS_LOST,     /**< Window has lost keyboard focus */
    SDL_WINDOWEVENT_CLOSE           /**< The window manager requests that the
                                         window be closed */
} SDL_WindowEventID;
typedef void *SDL_GLContext;
typedef enum
{
    SDL_GL_RED_SIZE,
    SDL_GL_GREEN_SIZE,
    SDL_GL_BLUE_SIZE,
    SDL_GL_ALPHA_SIZE,
    SDL_GL_BUFFER_SIZE,
    SDL_GL_DOUBLEBUFFER,
    SDL_GL_DEPTH_SIZE,
    SDL_GL_STENCIL_SIZE,
    SDL_GL_ACCUM_RED_SIZE,
    SDL_GL_ACCUM_GREEN_SIZE,
    SDL_GL_ACCUM_BLUE_SIZE,
    SDL_GL_ACCUM_ALPHA_SIZE,
    SDL_GL_STEREO,
    SDL_GL_MULTISAMPLEBUFFERS,
    SDL_GL_MULTISAMPLESAMPLES,
    SDL_GL_ACCELERATED_VISUAL,
    SDL_GL_RETAINED_BACKING,
    SDL_GL_CONTEXT_MAJOR_VERSION,
    SDL_GL_CONTEXT_MINOR_VERSION,
    SDL_GL_CONTEXT_EGL,
    SDL_GL_CONTEXT_FLAGS,
    SDL_GL_CONTEXT_PROFILE_MASK,
    SDL_GL_SHARE_WITH_CURRENT_CONTEXT,
    SDL_GL_FRAMEBUFFER_SRGB_CAPABLE
} SDL_GLattr;
typedef enum
{
    SDL_GL_CONTEXT_PROFILE_CORE           = 0x0001,
    SDL_GL_CONTEXT_PROFILE_COMPATIBILITY  = 0x0002,
    SDL_GL_CONTEXT_PROFILE_ES             = 0x0004 /* GLX_CONTEXT_ES2_PROFILE_BIT_EXT */
} SDL_GLprofile;
typedef enum
{
    SDL_GL_CONTEXT_DEBUG_FLAG              = 0x0001,
    SDL_GL_CONTEXT_FORWARD_COMPATIBLE_FLAG = 0x0002,
    SDL_GL_CONTEXT_ROBUST_ACCESS_FLAG      = 0x0004,
    SDL_GL_CONTEXT_RESET_ISOLATION_FLAG    = 0x0008
} SDL_GLcontextFlag;
int SDL_GetNumVideoDrivers(void);
const char *SDL_GetVideoDriver(int index);
int SDL_VideoInit(const char *driver_name);
void SDL_VideoQuit(void);
const char *SDL_GetCurrentVideoDriver(void);
int SDL_GetNumVideoDisplays(void);
const char * SDL_GetDisplayName(int displayIndex);
int SDL_GetDisplayBounds(int displayIndex, SDL_Rect * rect);
int SDL_GetNumDisplayModes(int displayIndex);
int SDL_GetDisplayMode(int displayIndex, int modeIndex, SDL_DisplayMode * mode);
int SDL_GetDesktopDisplayMode(int displayIndex, SDL_DisplayMode * mode);
int SDL_GetCurrentDisplayMode(int displayIndex, SDL_DisplayMode * mode);
SDL_DisplayMode * SDL_GetClosestDisplayMode(int displayIndex, const SDL_DisplayMode * mode, SDL_DisplayMode * closest);
int SDL_GetWindowDisplayIndex(SDL_Window * window);
int SDL_SetWindowDisplayMode(SDL_Window * window, const SDL_DisplayMode * mode);
int SDL_GetWindowDisplayMode(SDL_Window * window, SDL_DisplayMode * mode);
Uint32 SDL_GetWindowPixelFormat(SDL_Window * window);
SDL_Window * SDL_CreateWindow(const char *title, int x, int y, int w, int h, Uint32 flags);
SDL_Window * SDL_CreateWindowFrom(const void *data);
Uint32 SDL_GetWindowID(SDL_Window * window);
SDL_Window * SDL_GetWindowFromID(Uint32 id);
Uint32 SDL_GetWindowFlags(SDL_Window * window);
void SDL_SetWindowTitle(SDL_Window * window, const char *title);
const char *SDL_GetWindowTitle(SDL_Window * window);
void SDL_SetWindowIcon(SDL_Window * window, SDL_Surface * icon);
void* SDL_SetWindowData(SDL_Window * window, const char *name, void *userdata);
void *SDL_GetWindowData(SDL_Window * window, const char *name);
void SDL_SetWindowPosition(SDL_Window * window, int x, int y);
void SDL_GetWindowPosition(SDL_Window * window, int *x, int *y);
void SDL_SetWindowSize(SDL_Window * window, int w, int h);
void SDL_GetWindowSize(SDL_Window * window, int *w, int *h);
void SDL_SetWindowMinimumSize(SDL_Window * window, int min_w, int min_h);
void SDL_GetWindowMinimumSize(SDL_Window * window, int *w, int *h);
void SDL_SetWindowMaximumSize(SDL_Window * window, int max_w, int max_h);
void SDL_GetWindowMaximumSize(SDL_Window * window, int *w, int *h);
void SDL_SetWindowBordered(SDL_Window * window, SDL_bool bordered);
void SDL_ShowWindow(SDL_Window * window);
void SDL_HideWindow(SDL_Window * window);
void SDL_RaiseWindow(SDL_Window * window);
void SDL_MaximizeWindow(SDL_Window * window);
void SDL_MinimizeWindow(SDL_Window * window);
void SDL_RestoreWindow(SDL_Window * window);
int SDL_SetWindowFullscreen(SDL_Window * window, Uint32 flags);
SDL_Surface * SDL_GetWindowSurface(SDL_Window * window);
int SDL_UpdateWindowSurface(SDL_Window * window);
int SDL_UpdateWindowSurfaceRects(SDL_Window * window, const SDL_Rect * rects, int numrects);
void SDL_SetWindowGrab(SDL_Window * window, SDL_bool grabbed);
SDL_bool SDL_GetWindowGrab(SDL_Window * window);
int SDL_SetWindowBrightness(SDL_Window * window, float brightness);
float SDL_GetWindowBrightness(SDL_Window * window);
int SDL_SetWindowGammaRamp(SDL_Window * window, const Uint16 * red, const Uint16 * green, const Uint16 * blue);
int SDL_GetWindowGammaRamp(SDL_Window * window, Uint16 * red, Uint16 * green, Uint16 * blue);
void SDL_DestroyWindow(SDL_Window * window);
SDL_bool SDL_IsScreenSaverEnabled(void);
void SDL_EnableScreenSaver(void);
void SDL_DisableScreenSaver(void);
int SDL_GL_LoadLibrary(const char *path);
void *SDL_GL_GetProcAddress(const char *proc);
void SDL_GL_UnloadLibrary(void);
SDL_bool SDL_GL_ExtensionSupported(const char *extension);
void SDL_GL_ResetAttributes(void);
int SDL_GL_SetAttribute(SDL_GLattr attr, int value);
int SDL_GL_GetAttribute(SDL_GLattr attr, int *value);
SDL_GLContext SDL_GL_CreateContext(SDL_Window * window);
int SDL_GL_MakeCurrent(SDL_Window * window, SDL_GLContext context);
SDL_Window* SDL_GL_GetCurrentWindow(void);
SDL_GLContext SDL_GL_GetCurrentContext(void);
void SDL_GL_GetDrawableSize(SDL_Window * window, int *w, int *h);
int SDL_GL_SetSwapInterval(int interval);
int SDL_GL_GetSwapInterval(void);
void SDL_GL_SwapWindow(SDL_Window * window);
void SDL_GL_DeleteContext(SDL_GLContext context);

// SDL_scancode.h

typedef enum
{
    SDL_SCANCODE_UNKNOWN = 0,
    SDL_SCANCODE_A = 4,
    SDL_SCANCODE_B = 5,
    SDL_SCANCODE_C = 6,
    SDL_SCANCODE_D = 7,
    SDL_SCANCODE_E = 8,
    SDL_SCANCODE_F = 9,
    SDL_SCANCODE_G = 10,
    SDL_SCANCODE_H = 11,
    SDL_SCANCODE_I = 12,
    SDL_SCANCODE_J = 13,
    SDL_SCANCODE_K = 14,
    SDL_SCANCODE_L = 15,
    SDL_SCANCODE_M = 16,
    SDL_SCANCODE_N = 17,
    SDL_SCANCODE_O = 18,
    SDL_SCANCODE_P = 19,
    SDL_SCANCODE_Q = 20,
    SDL_SCANCODE_R = 21,
    SDL_SCANCODE_S = 22,
    SDL_SCANCODE_T = 23,
    SDL_SCANCODE_U = 24,
    SDL_SCANCODE_V = 25,
    SDL_SCANCODE_W = 26,
    SDL_SCANCODE_X = 27,
    SDL_SCANCODE_Y = 28,
    SDL_SCANCODE_Z = 29,
    SDL_SCANCODE_1 = 30,
    SDL_SCANCODE_2 = 31,
    SDL_SCANCODE_3 = 32,
    SDL_SCANCODE_4 = 33,
    SDL_SCANCODE_5 = 34,
    SDL_SCANCODE_6 = 35,
    SDL_SCANCODE_7 = 36,
    SDL_SCANCODE_8 = 37,
    SDL_SCANCODE_9 = 38,
    SDL_SCANCODE_0 = 39,
    SDL_SCANCODE_RETURN = 40,
    SDL_SCANCODE_ESCAPE = 41,
    SDL_SCANCODE_BACKSPACE = 42,
    SDL_SCANCODE_TAB = 43,
    SDL_SCANCODE_SPACE = 44,
    SDL_SCANCODE_MINUS = 45,
    SDL_SCANCODE_EQUALS = 46,
    SDL_SCANCODE_LEFTBRACKET = 47,
    SDL_SCANCODE_RIGHTBRACKET = 48,
    SDL_SCANCODE_BACKSLASH = 49,
    SDL_SCANCODE_NONUSHASH = 50,
    SDL_SCANCODE_SEMICOLON = 51,
    SDL_SCANCODE_APOSTROPHE = 52,
    SDL_SCANCODE_GRAVE = 53,
    SDL_SCANCODE_COMMA = 54,
    SDL_SCANCODE_PERIOD = 55,
    SDL_SCANCODE_SLASH = 56,
    SDL_SCANCODE_CAPSLOCK = 57,
    SDL_SCANCODE_F1 = 58,
    SDL_SCANCODE_F2 = 59,
    SDL_SCANCODE_F3 = 60,
    SDL_SCANCODE_F4 = 61,
    SDL_SCANCODE_F5 = 62,
    SDL_SCANCODE_F6 = 63,
    SDL_SCANCODE_F7 = 64,
    SDL_SCANCODE_F8 = 65,
    SDL_SCANCODE_F9 = 66,
    SDL_SCANCODE_F10 = 67,
    SDL_SCANCODE_F11 = 68,
    SDL_SCANCODE_F12 = 69,
    SDL_SCANCODE_PRINTSCREEN = 70,
    SDL_SCANCODE_SCROLLLOCK = 71,
    SDL_SCANCODE_PAUSE = 72,
    SDL_SCANCODE_INSERT = 73,
    SDL_SCANCODE_HOME = 74,
    SDL_SCANCODE_PAGEUP = 75,
    SDL_SCANCODE_DELETE = 76,
    SDL_SCANCODE_END = 77,
    SDL_SCANCODE_PAGEDOWN = 78,
    SDL_SCANCODE_RIGHT = 79,
    SDL_SCANCODE_LEFT = 80,
    SDL_SCANCODE_DOWN = 81,
    SDL_SCANCODE_UP = 82,
    SDL_SCANCODE_NUMLOCKCLEAR = 83,
    SDL_SCANCODE_KP_DIVIDE = 84,
    SDL_SCANCODE_KP_MULTIPLY = 85,
    SDL_SCANCODE_KP_MINUS = 86,
    SDL_SCANCODE_KP_PLUS = 87,
    SDL_SCANCODE_KP_ENTER = 88,
    SDL_SCANCODE_KP_1 = 89,
    SDL_SCANCODE_KP_2 = 90,
    SDL_SCANCODE_KP_3 = 91,
    SDL_SCANCODE_KP_4 = 92,
    SDL_SCANCODE_KP_5 = 93,
    SDL_SCANCODE_KP_6 = 94,
    SDL_SCANCODE_KP_7 = 95,
    SDL_SCANCODE_KP_8 = 96,
    SDL_SCANCODE_KP_9 = 97,
    SDL_SCANCODE_KP_0 = 98,
    SDL_SCANCODE_KP_PERIOD = 99,
    SDL_SCANCODE_NONUSBACKSLASH = 100,
    SDL_SCANCODE_APPLICATION = 101,
    SDL_SCANCODE_POWER = 102,
    SDL_SCANCODE_KP_EQUALS = 103,
    SDL_SCANCODE_F13 = 104,
    SDL_SCANCODE_F14 = 105,
    SDL_SCANCODE_F15 = 106,
    SDL_SCANCODE_F16 = 107,
    SDL_SCANCODE_F17 = 108,
    SDL_SCANCODE_F18 = 109,
    SDL_SCANCODE_F19 = 110,
    SDL_SCANCODE_F20 = 111,
    SDL_SCANCODE_F21 = 112,
    SDL_SCANCODE_F22 = 113,
    SDL_SCANCODE_F23 = 114,
    SDL_SCANCODE_F24 = 115,
    SDL_SCANCODE_EXECUTE = 116,
    SDL_SCANCODE_HELP = 117,
    SDL_SCANCODE_MENU = 118,
    SDL_SCANCODE_SELECT = 119,
    SDL_SCANCODE_STOP = 120,
    SDL_SCANCODE_AGAIN = 121,
    SDL_SCANCODE_UNDO = 122,
    SDL_SCANCODE_CUT = 123,
    SDL_SCANCODE_COPY = 124,
    SDL_SCANCODE_PASTE = 125,
    SDL_SCANCODE_FIND = 126,
    SDL_SCANCODE_MUTE = 127,
    SDL_SCANCODE_VOLUMEUP = 128,
    SDL_SCANCODE_VOLUMEDOWN = 129,
    SDL_SCANCODE_KP_COMMA = 133,
    SDL_SCANCODE_KP_EQUALSAS400 = 134,

    SDL_SCANCODE_INTERNATIONAL1 = 135,
    SDL_SCANCODE_INTERNATIONAL2 = 136,
    SDL_SCANCODE_INTERNATIONAL3 = 137, /**< Yen */
    SDL_SCANCODE_INTERNATIONAL4 = 138,
    SDL_SCANCODE_INTERNATIONAL5 = 139,
    SDL_SCANCODE_INTERNATIONAL6 = 140,
    SDL_SCANCODE_INTERNATIONAL7 = 141,
    SDL_SCANCODE_INTERNATIONAL8 = 142,
    SDL_SCANCODE_INTERNATIONAL9 = 143,
    SDL_SCANCODE_LANG1 = 144, /**< Hangul/English toggle */
    SDL_SCANCODE_LANG2 = 145, /**< Hanja conversion */
    SDL_SCANCODE_LANG3 = 146, /**< Katakana */
    SDL_SCANCODE_LANG4 = 147, /**< Hiragana */
    SDL_SCANCODE_LANG5 = 148, /**< Zenkaku/Hankaku */
    SDL_SCANCODE_LANG6 = 149, /**< reserved */
    SDL_SCANCODE_LANG7 = 150, /**< reserved */
    SDL_SCANCODE_LANG8 = 151, /**< reserved */
    SDL_SCANCODE_LANG9 = 152, /**< reserved */
    SDL_SCANCODE_ALTERASE = 153, /**< Erase-Eaze */
    SDL_SCANCODE_SYSREQ = 154,
    SDL_SCANCODE_CANCEL = 155,
    SDL_SCANCODE_CLEAR = 156,
    SDL_SCANCODE_PRIOR = 157,
    SDL_SCANCODE_RETURN2 = 158,
    SDL_SCANCODE_SEPARATOR = 159,
    SDL_SCANCODE_OUT = 160,
    SDL_SCANCODE_OPER = 161,
    SDL_SCANCODE_CLEARAGAIN = 162,
    SDL_SCANCODE_CRSEL = 163,
    SDL_SCANCODE_EXSEL = 164,
    SDL_SCANCODE_KP_00 = 176,
    SDL_SCANCODE_KP_000 = 177,
    SDL_SCANCODE_THOUSANDSSEPARATOR = 178,
    SDL_SCANCODE_DECIMALSEPARATOR = 179,
    SDL_SCANCODE_CURRENCYUNIT = 180,
    SDL_SCANCODE_CURRENCYSUBUNIT = 181,
    SDL_SCANCODE_KP_LEFTPAREN = 182,
    SDL_SCANCODE_KP_RIGHTPAREN = 183,
    SDL_SCANCODE_KP_LEFTBRACE = 184,
    SDL_SCANCODE_KP_RIGHTBRACE = 185,
    SDL_SCANCODE_KP_TAB = 186,
    SDL_SCANCODE_KP_BACKSPACE = 187,
    SDL_SCANCODE_KP_A = 188,
    SDL_SCANCODE_KP_B = 189,
    SDL_SCANCODE_KP_C = 190,
    SDL_SCANCODE_KP_D = 191,
    SDL_SCANCODE_KP_E = 192,
    SDL_SCANCODE_KP_F = 193,
    SDL_SCANCODE_KP_XOR = 194,
    SDL_SCANCODE_KP_POWER = 195,
    SDL_SCANCODE_KP_PERCENT = 196,
    SDL_SCANCODE_KP_LESS = 197,
    SDL_SCANCODE_KP_GREATER = 198,
    SDL_SCANCODE_KP_AMPERSAND = 199,
    SDL_SCANCODE_KP_DBLAMPERSAND = 200,
    SDL_SCANCODE_KP_VERTICALBAR = 201,
    SDL_SCANCODE_KP_DBLVERTICALBAR = 202,
    SDL_SCANCODE_KP_COLON = 203,
    SDL_SCANCODE_KP_HASH = 204,
    SDL_SCANCODE_KP_SPACE = 205,
    SDL_SCANCODE_KP_AT = 206,
    SDL_SCANCODE_KP_EXCLAM = 207,
    SDL_SCANCODE_KP_MEMSTORE = 208,
    SDL_SCANCODE_KP_MEMRECALL = 209,
    SDL_SCANCODE_KP_MEMCLEAR = 210,
    SDL_SCANCODE_KP_MEMADD = 211,
    SDL_SCANCODE_KP_MEMSUBTRACT = 212,
    SDL_SCANCODE_KP_MEMMULTIPLY = 213,
    SDL_SCANCODE_KP_MEMDIVIDE = 214,
    SDL_SCANCODE_KP_PLUSMINUS = 215,
    SDL_SCANCODE_KP_CLEAR = 216,
    SDL_SCANCODE_KP_CLEARENTRY = 217,
    SDL_SCANCODE_KP_BINARY = 218,
    SDL_SCANCODE_KP_OCTAL = 219,
    SDL_SCANCODE_KP_DECIMAL = 220,
    SDL_SCANCODE_KP_HEXADECIMAL = 221,
    SDL_SCANCODE_LCTRL = 224,
    SDL_SCANCODE_LSHIFT = 225,
    SDL_SCANCODE_LALT = 226, /**< alt, option */
    SDL_SCANCODE_LGUI = 227, /**< windows, command (apple), meta */
    SDL_SCANCODE_RCTRL = 228,
    SDL_SCANCODE_RSHIFT = 229,
    SDL_SCANCODE_RALT = 230, /**< alt gr, option */
    SDL_SCANCODE_RGUI = 231, /**< windows, command (apple), meta */
    SDL_SCANCODE_MODE = 257,
    SDL_SCANCODE_AUDIONEXT = 258,
    SDL_SCANCODE_AUDIOPREV = 259,
    SDL_SCANCODE_AUDIOSTOP = 260,
    SDL_SCANCODE_AUDIOPLAY = 261,
    SDL_SCANCODE_AUDIOMUTE = 262,
    SDL_SCANCODE_MEDIASELECT = 263,
    SDL_SCANCODE_WWW = 264,
    SDL_SCANCODE_MAIL = 265,
    SDL_SCANCODE_CALCULATOR = 266,
    SDL_SCANCODE_COMPUTER = 267,
    SDL_SCANCODE_AC_SEARCH = 268,
    SDL_SCANCODE_AC_HOME = 269,
    SDL_SCANCODE_AC_BACK = 270,
    SDL_SCANCODE_AC_FORWARD = 271,
    SDL_SCANCODE_AC_STOP = 272,
    SDL_SCANCODE_AC_REFRESH = 273,
    SDL_SCANCODE_AC_BOOKMARKS = 274,
    SDL_SCANCODE_BRIGHTNESSDOWN = 275,
    SDL_SCANCODE_BRIGHTNESSUP = 276,
    SDL_SCANCODE_DISPLAYSWITCH = 277, /**< display mirroring/dual display switch, video mode switch */
    SDL_SCANCODE_KBDILLUMTOGGLE = 278,
    SDL_SCANCODE_KBDILLUMDOWN = 279,
    SDL_SCANCODE_KBDILLUMUP = 280,
    SDL_SCANCODE_EJECT = 281,
    SDL_SCANCODE_SLEEP = 282,
    SDL_SCANCODE_APP1 = 283,
    SDL_SCANCODE_APP2 = 284,
    SDL_NUM_SCANCODES = 512 /**< not a key, just marks the number of scancodes for array bounds */
} SDL_Scancode;

// SDL_keycode.h

typedef Sint32 SDL_Keycode;
#define SDLK_SCANCODE_MASK (1<<30)
#define SDL_SCANCODE_TO_KEYCODE(X)  (X | SDLK_SCANCODE_MASK)
// Gumm note: cffi can't parse keycodes. Too many problems to work around.
typedef enum
{
    KMOD_NONE = 0x0000,
    KMOD_LSHIFT = 0x0001,
    KMOD_RSHIFT = 0x0002,
    KMOD_LCTRL = 0x0040,
    KMOD_RCTRL = 0x0080,
    KMOD_LALT = 0x0100,
    KMOD_RALT = 0x0200,
    KMOD_LGUI = 0x0400,
    KMOD_RGUI = 0x0800,
    KMOD_NUM = 0x1000,
    KMOD_CAPS = 0x2000,
    KMOD_MODE = 0x4000,
    KMOD_RESERVED = 0x8000
} SDL_Keymod;
#define KMOD_CTRL   (KMOD_LCTRL|KMOD_RCTRL)
#define KMOD_SHIFT  (KMOD_LSHIFT|KMOD_RSHIFT)
#define KMOD_ALT    (KMOD_LALT|KMOD_RALT)
#define KMOD_GUI    (KMOD_LGUI|KMOD_RGUI)

// SDL_keyboard.h

typedef struct SDL_Keysym
{
    SDL_Scancode scancode;      /**< SDL physical key code - see ::SDL_Scancode for details */
    SDL_Keycode sym;            /**< SDL virtual key code - see ::SDL_Keycode for details */
    Uint16 mod;                 /**< current key modifiers */
    Uint32 unused;
} SDL_Keysym;
SDL_Window * SDL_GetKeyboardFocus(void);
const Uint8 *SDL_GetKeyboardState(int *numkeys);
SDL_Keymod SDL_GetModState(void);
void SDL_SetModState(SDL_Keymod modstate);
SDL_Keycode SDL_GetKeyFromScancode(SDL_Scancode scancode);
SDL_Scancode SDL_GetScancodeFromKey(SDL_Keycode key);
const char *SDL_GetScancodeName(SDL_Scancode scancode);
SDL_Scancode SDL_GetScancodeFromName(const char *name);
const char *SDL_GetKeyName(SDL_Keycode key);
SDL_Keycode SDL_GetKeyFromName(const char *name);
void SDL_StartTextInput(void);
SDL_bool SDL_IsTextInputActive(void);
void SDL_StopTextInput(void);
void SDL_SetTextInputRect(SDL_Rect *rect);
SDL_bool SDL_HasScreenKeyboardSupport(void);
SDL_bool SDL_IsScreenKeyboardShown(SDL_Window *window);

// SDL_mouse.h

typedef struct SDL_Cursor SDL_Cursor;   /* Implementation dependent */
typedef enum
{
    SDL_SYSTEM_CURSOR_ARROW,     /**< Arrow */
    SDL_SYSTEM_CURSOR_IBEAM,     /**< I-beam */
    SDL_SYSTEM_CURSOR_WAIT,      /**< Wait */
    SDL_SYSTEM_CURSOR_CROSSHAIR, /**< Crosshair */
    SDL_SYSTEM_CURSOR_WAITARROW, /**< Small wait cursor (or Wait if not available) */
    SDL_SYSTEM_CURSOR_SIZENWSE,  /**< Double arrow pointing northwest and southeast */
    SDL_SYSTEM_CURSOR_SIZENESW,  /**< Double arrow pointing northeast and southwest */
    SDL_SYSTEM_CURSOR_SIZEWE,    /**< Double arrow pointing west and east */
    SDL_SYSTEM_CURSOR_SIZENS,    /**< Double arrow pointing north and south */
    SDL_SYSTEM_CURSOR_SIZEALL,   /**< Four pointed arrow pointing north, south, east, and west */
    SDL_SYSTEM_CURSOR_NO,        /**< Slashed circle or crossbones */
    SDL_SYSTEM_CURSOR_HAND,      /**< Hand */
    SDL_NUM_SYSTEM_CURSORS
} SDL_SystemCursor;
SDL_Window * SDL_GetMouseFocus(void);
Uint32 SDL_GetMouseState(int *x, int *y);
Uint32 SDL_GetRelativeMouseState(int *x, int *y);
void SDL_WarpMouseInWindow(SDL_Window * window, int x, int y);
int SDL_SetRelativeMouseMode(SDL_bool enabled);
SDL_bool SDL_GetRelativeMouseMode(void);
SDL_Cursor *SDL_CreateCursor(const Uint8 * data, const Uint8 * mask, int w, int h, int hot_x, int hot_y);
SDL_Cursor *SDL_CreateColorCursor(SDL_Surface *surface, int hot_x, int hot_y);
SDL_Cursor *SDL_CreateSystemCursor(SDL_SystemCursor id);
void SDL_SetCursor(SDL_Cursor * cursor);
SDL_Cursor *SDL_GetCursor(void);
SDL_Cursor *SDL_GetDefaultCursor(void);
void SDL_FreeCursor(SDL_Cursor * cursor);
int SDL_ShowCursor(int toggle);
#define SDL_BUTTON(X)       (1 << ((X)-1))
#define SDL_BUTTON_LEFT     1
#define SDL_BUTTON_MIDDLE   2
#define SDL_BUTTON_RIGHT    3
#define SDL_BUTTON_X1       4
#define SDL_BUTTON_X2       5
#define SDL_BUTTON_LMASK    SDL_BUTTON(SDL_BUTTON_LEFT)
#define SDL_BUTTON_MMASK    SDL_BUTTON(SDL_BUTTON_MIDDLE)
#define SDL_BUTTON_RMASK    SDL_BUTTON(SDL_BUTTON_RIGHT)
#define SDL_BUTTON_X1MASK   SDL_BUTTON(SDL_BUTTON_X1)
#define SDL_BUTTON_X2MASK   SDL_BUTTON(SDL_BUTTON_X2)

// SDL_joystick.h

struct _SDL_Joystick;
typedef struct _SDL_Joystick SDL_Joystick;
typedef struct {
    Uint8 data[16];
} SDL_JoystickGUID;
typedef Sint32 SDL_JoystickID;
int SDL_NumJoysticks(void);
const char *SDL_JoystickNameForIndex(int device_index);
SDL_Joystick *SDL_JoystickOpen(int device_index);
const char *SDL_JoystickName(SDL_Joystick * joystick);
SDL_JoystickGUID SDL_JoystickGetDeviceGUID(int device_index);
SDL_JoystickGUID SDL_JoystickGetGUID(SDL_Joystick * joystick);
void SDL_JoystickGetGUIDString(SDL_JoystickGUID guid, char *pszGUID, int cbGUID);
SDL_JoystickGUID SDL_JoystickGetGUIDFromString(const char *pchGUID);
SDL_bool SDL_JoystickGetAttached(SDL_Joystick * joystick);
SDL_JoystickID SDL_JoystickInstanceID(SDL_Joystick * joystick);
int SDL_JoystickNumAxes(SDL_Joystick * joystick);
int SDL_JoystickNumBalls(SDL_Joystick * joystick);
int SDL_JoystickNumHats(SDL_Joystick * joystick);
int SDL_JoystickNumButtons(SDL_Joystick * joystick);
void SDL_JoystickUpdate(void);
int SDL_JoystickEventState(int state);
Sint16 SDL_JoystickGetAxis(SDL_Joystick * joystick, int axis);
#define SDL_HAT_CENTERED    0x00
#define SDL_HAT_UP      0x01
#define SDL_HAT_RIGHT       0x02
#define SDL_HAT_DOWN        0x04
#define SDL_HAT_LEFT        0x08
#define SDL_HAT_RIGHTUP     (SDL_HAT_RIGHT|SDL_HAT_UP)
#define SDL_HAT_RIGHTDOWN   (SDL_HAT_RIGHT|SDL_HAT_DOWN)
#define SDL_HAT_LEFTUP      (SDL_HAT_LEFT|SDL_HAT_UP)
#define SDL_HAT_LEFTDOWN    (SDL_HAT_LEFT|SDL_HAT_DOWN)
Uint8 SDL_JoystickGetHat(SDL_Joystick * joystick, int hat);
int SDL_JoystickGetBall(SDL_Joystick * joystick, int ball, int *dx, int *dy);
Uint8 SDL_JoystickGetButton(SDL_Joystick * joystick, int button);
void SDL_JoystickClose(SDL_Joystick * joystick);

// SDL_gamecontroller.h

struct _SDL_GameController;
typedef struct _SDL_GameController SDL_GameController;
typedef enum
{
    SDL_CONTROLLER_BINDTYPE_NONE = 0,
    SDL_CONTROLLER_BINDTYPE_BUTTON,
    SDL_CONTROLLER_BINDTYPE_AXIS,
    SDL_CONTROLLER_BINDTYPE_HAT
} SDL_GameControllerBindType;
typedef struct SDL_GameControllerButtonBind
{
    SDL_GameControllerBindType bindType;
    union
    {
        int button;
        int axis;
        struct {
            int hat;
            int hat_mask;
        } hat;
    } value;

} SDL_GameControllerButtonBind;
int SDL_GameControllerAddMappingsFromRW( SDL_RWops * rw, int freerw );
#define SDL_GameControllerAddMappingsFromFile(file)   SDL_GameControllerAddMappingsFromRW(SDL_RWFromFile(file, "rb"), 1)
int SDL_GameControllerAddMapping( const char* mappingString );
char * SDL_GameControllerMappingForGUID( SDL_JoystickGUID guid );
char * SDL_GameControllerMapping( SDL_GameController * gamecontroller );
SDL_bool SDL_IsGameController(int joystick_index);
const char *SDL_GameControllerNameForIndex(int joystick_index);
SDL_GameController *SDL_GameControllerOpen(int joystick_index);
const char *SDL_GameControllerName(SDL_GameController *gamecontroller);
SDL_bool SDL_GameControllerGetAttached(SDL_GameController *gamecontroller);
SDL_Joystick *SDL_GameControllerGetJoystick(SDL_GameController *gamecontroller);
int SDL_GameControllerEventState(int state);
void SDL_GameControllerUpdate(void);
typedef enum
{
    SDL_CONTROLLER_AXIS_INVALID = -1,
    SDL_CONTROLLER_AXIS_LEFTX,
    SDL_CONTROLLER_AXIS_LEFTY,
    SDL_CONTROLLER_AXIS_RIGHTX,
    SDL_CONTROLLER_AXIS_RIGHTY,
    SDL_CONTROLLER_AXIS_TRIGGERLEFT,
    SDL_CONTROLLER_AXIS_TRIGGERRIGHT,
    SDL_CONTROLLER_AXIS_MAX
} SDL_GameControllerAxis;
SDL_GameControllerAxis SDL_GameControllerGetAxisFromString(const char *pchString);
const char* SDL_GameControllerGetStringForAxis(SDL_GameControllerAxis axis);
SDL_GameControllerButtonBind SDL_GameControllerGetBindForAxis(SDL_GameController *gamecontroller, SDL_GameControllerAxis axis);
Sint16 SDL_GameControllerGetAxis(SDL_GameController *gamecontroller, SDL_GameControllerAxis axis);
typedef enum
{
    SDL_CONTROLLER_BUTTON_INVALID = -1,
    SDL_CONTROLLER_BUTTON_A,
    SDL_CONTROLLER_BUTTON_B,
    SDL_CONTROLLER_BUTTON_X,
    SDL_CONTROLLER_BUTTON_Y,
    SDL_CONTROLLER_BUTTON_BACK,
    SDL_CONTROLLER_BUTTON_GUIDE,
    SDL_CONTROLLER_BUTTON_START,
    SDL_CONTROLLER_BUTTON_LEFTSTICK,
    SDL_CONTROLLER_BUTTON_RIGHTSTICK,
    SDL_CONTROLLER_BUTTON_LEFTSHOULDER,
    SDL_CONTROLLER_BUTTON_RIGHTSHOULDER,
    SDL_CONTROLLER_BUTTON_DPAD_UP,
    SDL_CONTROLLER_BUTTON_DPAD_DOWN,
    SDL_CONTROLLER_BUTTON_DPAD_LEFT,
    SDL_CONTROLLER_BUTTON_DPAD_RIGHT,
    SDL_CONTROLLER_BUTTON_MAX
} SDL_GameControllerButton;
SDL_GameControllerButton SDL_GameControllerGetButtonFromString(const char *pchString);
const char* SDL_GameControllerGetStringForButton(SDL_GameControllerButton button);
SDL_GameControllerButtonBind SDL_GameControllerGetBindForButton(SDL_GameController *gamecontroller, SDL_GameControllerButton button);
Uint8 SDL_GameControllerGetButton(SDL_GameController *gamecontroller, SDL_GameControllerButton button);
void SDL_GameControllerClose(SDL_GameController *gamecontroller);

// SDL_quit.h

#define SDL_QuitRequested() (SDL_PumpEvents(), (SDL_PeepEvents(NULL,0,SDL_PEEKEVENT,SDL_QUIT,SDL_QUIT) > 0))

// SDL_touch.h

typedef Sint64 SDL_TouchID;
typedef Sint64 SDL_FingerID;
typedef struct SDL_Finger
{
    SDL_FingerID id;
    float x;
    float y;
    float pressure;
} SDL_Finger;
#define SDL_TOUCH_MOUSEID ((Uint32)-1)
int SDL_GetNumTouchDevices(void);
SDL_TouchID SDL_GetTouchDevice(int index);
int SDL_GetNumTouchFingers(SDL_TouchID touchID);
SDL_Finger * SDL_GetTouchFinger(SDL_TouchID touchID, int index);

// SDL_gesture.h

typedef Sint64 SDL_GestureID;
int SDL_RecordGesture(SDL_TouchID touchId);
int SDL_SaveAllDollarTemplates(SDL_RWops *dst);
int SDL_SaveDollarTemplate(SDL_GestureID gestureId,SDL_RWops *dst);
int SDL_LoadDollarTemplates(SDL_TouchID touchId, SDL_RWops *src);

// SDL_event.h

#define SDL_RELEASED    0
#define SDL_PRESSED 1
typedef enum
{
    SDL_FIRSTEVENT     = 0,     /**< Unused (do not remove) */
    /* Application events */
    SDL_QUIT           = 0x100, /**< User-requested quit */

    /* These application events have special meaning on iOS, see README-ios.txt for details */
    SDL_APP_TERMINATING,        /**< The application is being terminated by the OS
                                     Called on iOS in applicationWillTerminate()
                                     Called on Android in onDestroy()
                                */
    SDL_APP_LOWMEMORY,          /**< The application is low on memory, free memory if possible.
                                     Called on iOS in applicationDidReceiveMemoryWarning()
                                     Called on Android in onLowMemory()
                                */
    SDL_APP_WILLENTERBACKGROUND, /**< The application is about to enter the background
                                     Called on iOS in applicationWillResignActive()
                                     Called on Android in onPause()
                                */
    SDL_APP_DIDENTERBACKGROUND, /**< The application did enter the background and may not get CPU for some time
                                     Called on iOS in applicationDidEnterBackground()
                                     Called on Android in onPause()
                                */
    SDL_APP_WILLENTERFOREGROUND, /**< The application is about to enter the foreground
                                     Called on iOS in applicationWillEnterForeground()
                                     Called on Android in onResume()
                                */
    SDL_APP_DIDENTERFOREGROUND, /**< The application is now interactive
                                     Called on iOS in applicationDidBecomeActive()
                                     Called on Android in onResume()
                                */
    /* Window events */
    SDL_WINDOWEVENT    = 0x200, /**< Window state change */
    SDL_SYSWMEVENT,             /**< System specific event */
    /* Keyboard events */
    SDL_KEYDOWN        = 0x300, /**< Key pressed */
    SDL_KEYUP,                  /**< Key released */
    SDL_TEXTEDITING,            /**< Keyboard text editing (composition) */
    SDL_TEXTINPUT,              /**< Keyboard text input */
    /* Mouse events */
    SDL_MOUSEMOTION    = 0x400, /**< Mouse moved */
    SDL_MOUSEBUTTONDOWN,        /**< Mouse button pressed */
    SDL_MOUSEBUTTONUP,          /**< Mouse button released */
    SDL_MOUSEWHEEL,             /**< Mouse wheel motion */
    /* Joystick events */
    SDL_JOYAXISMOTION  = 0x600, /**< Joystick axis motion */
    SDL_JOYBALLMOTION,          /**< Joystick trackball motion */
    SDL_JOYHATMOTION,           /**< Joystick hat position change */
    SDL_JOYBUTTONDOWN,          /**< Joystick button pressed */
    SDL_JOYBUTTONUP,            /**< Joystick button released */
    SDL_JOYDEVICEADDED,         /**< A new joystick has been inserted into the system */
    SDL_JOYDEVICEREMOVED,       /**< An opened joystick has been removed */
    /* Game controller events */
    SDL_CONTROLLERAXISMOTION  = 0x650, /**< Game controller axis motion */
    SDL_CONTROLLERBUTTONDOWN,          /**< Game controller button pressed */
    SDL_CONTROLLERBUTTONUP,            /**< Game controller button released */
    SDL_CONTROLLERDEVICEADDED,         /**< A new Game controller has been inserted into the system */
    SDL_CONTROLLERDEVICEREMOVED,       /**< An opened Game controller has been removed */
    SDL_CONTROLLERDEVICEREMAPPED,      /**< The controller mapping was updated */
    /* Touch events */
    SDL_FINGERDOWN      = 0x700,
    SDL_FINGERUP,
    SDL_FINGERMOTION,
    /* Gesture events */
    SDL_DOLLARGESTURE   = 0x800,
    SDL_DOLLARRECORD,
    SDL_MULTIGESTURE,
    /* Clipboard events */
    SDL_CLIPBOARDUPDATE = 0x900, /**< The clipboard changed */
    /* Drag and drop events */
    SDL_DROPFILE        = 0x1000, /**< The system requests a file open */
    /* Render events */
    SDL_RENDER_TARGETS_RESET = 0x2000, /**< The render targets have been reset */
    /** Events ::SDL_USEREVENT through ::SDL_LASTEVENT are for your use,
     *  and should be allocated with SDL_RegisterEvents()
     */
    SDL_USEREVENT    = 0x8000,
    /**
     *  This last event is only for bounding internal arrays
     */
    SDL_LASTEVENT    = 0xFFFF
} SDL_EventType;
typedef struct SDL_CommonEvent
{
    Uint32 type;
    Uint32 timestamp;
} SDL_CommonEvent;
typedef struct SDL_WindowEvent
{
    Uint32 type;        /**< ::SDL_WINDOWEVENT */
    Uint32 timestamp;
    Uint32 windowID;    /**< The associated window */
    Uint8 event;        /**< ::SDL_WindowEventID */
    Uint8 padding1;
    Uint8 padding2;
    Uint8 padding3;
    Sint32 data1;       /**< event dependent data */
    Sint32 data2;       /**< event dependent data */
} SDL_WindowEvent;
typedef struct SDL_KeyboardEvent
{
    Uint32 type;        /**< ::SDL_KEYDOWN or ::SDL_KEYUP */
    Uint32 timestamp;
    Uint32 windowID;    /**< The window with keyboard focus, if any */
    Uint8 state;        /**< ::SDL_PRESSED or ::SDL_RELEASED */
    Uint8 repeat;       /**< Non-zero if this is a key repeat */
    Uint8 padding2;
    Uint8 padding3;
    SDL_Keysym keysym;  /**< The key that was pressed or released */
} SDL_KeyboardEvent;
#define SDL_TEXTEDITINGEVENT_TEXT_SIZE (32)
typedef struct SDL_TextEditingEvent
{
    Uint32 type;                                /**< ::SDL_TEXTEDITING */
    Uint32 timestamp;
    Uint32 windowID;                            /**< The window with keyboard focus, if any */
    char text[32];       /* Gumm hack: SDL_TEXTEDITINGEVENT_TEXT_SIZE]; */  /**< The editing text */
    Sint32 start;                               /**< The start cursor of selected editing text */
    Sint32 length;                              /**< The length of selected editing text */
} SDL_TextEditingEvent;
#define SDL_TEXTINPUTEVENT_TEXT_SIZE (32)
typedef struct SDL_TextInputEvent
{
    Uint32 type;                              /**< ::SDL_TEXTINPUT */
    Uint32 timestamp;
    Uint32 windowID;                          /**< The window with keyboard focus, if any */
    char text[32];       /* Gumm hack: SDL_TEXTINPUTEVENT_TEXT_SIZE]; */  /**< The input text */
} SDL_TextInputEvent;
typedef struct SDL_MouseMotionEvent
{
    Uint32 type;        /**< ::SDL_MOUSEMOTION */
    Uint32 timestamp;
    Uint32 windowID;    /**< The window with mouse focus, if any */
    Uint32 which;       /**< The mouse instance id, or SDL_TOUCH_MOUSEID */
    Uint32 state;       /**< The current button state */
    Sint32 x;           /**< X coordinate, relative to window */
    Sint32 y;           /**< Y coordinate, relative to window */
    Sint32 xrel;        /**< The relative motion in the X direction */
    Sint32 yrel;        /**< The relative motion in the Y direction */
} SDL_MouseMotionEvent;
typedef struct SDL_MouseButtonEvent
{
    Uint32 type;        /**< ::SDL_MOUSEBUTTONDOWN or ::SDL_MOUSEBUTTONUP */
    Uint32 timestamp;
    Uint32 windowID;    /**< The window with mouse focus, if any */
    Uint32 which;       /**< The mouse instance id, or SDL_TOUCH_MOUSEID */
    Uint8 button;       /**< The mouse button index */
    Uint8 state;        /**< ::SDL_PRESSED or ::SDL_RELEASED */
    Uint8 clicks;       /**< 1 for single-click, 2 for double-click, etc. */
    Uint8 padding1;
    Sint32 x;           /**< X coordinate, relative to window */
    Sint32 y;           /**< Y coordinate, relative to window */
} SDL_MouseButtonEvent;
typedef struct SDL_MouseWheelEvent
{
    Uint32 type;        /**< ::SDL_MOUSEWHEEL */
    Uint32 timestamp;
    Uint32 windowID;    /**< The window with mouse focus, if any */
    Uint32 which;       /**< The mouse instance id, or SDL_TOUCH_MOUSEID */
    Sint32 x;           /**< The amount scrolled horizontally, positive to the right and negative to the left */
    Sint32 y;           /**< The amount scrolled vertically, positive away from the user and negative toward the user */
} SDL_MouseWheelEvent;
typedef struct SDL_JoyAxisEvent
{
    Uint32 type;        /**< ::SDL_JOYAXISMOTION */
    Uint32 timestamp;
    SDL_JoystickID which; /**< The joystick instance id */
    Uint8 axis;         /**< The joystick axis index */
    Uint8 padding1;
    Uint8 padding2;
    Uint8 padding3;
    Sint16 value;       /**< The axis value (range: -32768 to 32767) */
    Uint16 padding4;
} SDL_JoyAxisEvent;
typedef struct SDL_JoyBallEvent
{
    Uint32 type;        /**< ::SDL_JOYBALLMOTION */
    Uint32 timestamp;
    SDL_JoystickID which; /**< The joystick instance id */
    Uint8 ball;         /**< The joystick trackball index */
    Uint8 padding1;
    Uint8 padding2;
    Uint8 padding3;
    Sint16 xrel;        /**< The relative motion in the X direction */
    Sint16 yrel;        /**< The relative motion in the Y direction */
} SDL_JoyBallEvent;
typedef struct SDL_JoyHatEvent
{
    Uint32 type;        /**< ::SDL_JOYHATMOTION */
    Uint32 timestamp;
    SDL_JoystickID which; /**< The joystick instance id */
    Uint8 hat;          /**< The joystick hat index */
    Uint8 value;        /**< The hat position value.
                         *   \sa ::SDL_HAT_LEFTUP ::SDL_HAT_UP ::SDL_HAT_RIGHTUP
                         *   \sa ::SDL_HAT_LEFT ::SDL_HAT_CENTERED ::SDL_HAT_RIGHT
                         *   \sa ::SDL_HAT_LEFTDOWN ::SDL_HAT_DOWN ::SDL_HAT_RIGHTDOWN
                         *
                         *   Note that zero means the POV is centered.
                         */
    Uint8 padding1;
    Uint8 padding2;
} SDL_JoyHatEvent;
typedef struct SDL_JoyButtonEvent
{
    Uint32 type;        /**< ::SDL_JOYBUTTONDOWN or ::SDL_JOYBUTTONUP */
    Uint32 timestamp;
    SDL_JoystickID which; /**< The joystick instance id */
    Uint8 button;       /**< The joystick button index */
    Uint8 state;        /**< ::SDL_PRESSED or ::SDL_RELEASED */
    Uint8 padding1;
    Uint8 padding2;
} SDL_JoyButtonEvent;
typedef struct SDL_JoyDeviceEvent
{
    Uint32 type;        /**< ::SDL_JOYDEVICEADDED or ::SDL_JOYDEVICEREMOVED */
    Uint32 timestamp;
    Sint32 which;       /**< The joystick device index for the ADDED event, instance id for the REMOVED event */
} SDL_JoyDeviceEvent;
typedef struct SDL_ControllerAxisEvent
{
    Uint32 type;        /**< ::SDL_CONTROLLERAXISMOTION */
    Uint32 timestamp;
    SDL_JoystickID which; /**< The joystick instance id */
    Uint8 axis;         /**< The controller axis (SDL_GameControllerAxis) */
    Uint8 padding1;
    Uint8 padding2;
    Uint8 padding3;
    Sint16 value;       /**< The axis value (range: -32768 to 32767) */
    Uint16 padding4;
} SDL_ControllerAxisEvent;
typedef struct SDL_ControllerButtonEvent
{
    Uint32 type;        /**< ::SDL_CONTROLLERBUTTONDOWN or ::SDL_CONTROLLERBUTTONUP */
    Uint32 timestamp;
    SDL_JoystickID which; /**< The joystick instance id */
    Uint8 button;       /**< The controller button (SDL_GameControllerButton) */
    Uint8 state;        /**< ::SDL_PRESSED or ::SDL_RELEASED */
    Uint8 padding1;
    Uint8 padding2;
} SDL_ControllerButtonEvent;
typedef struct SDL_ControllerDeviceEvent
{
    Uint32 type;        /**< ::SDL_CONTROLLERDEVICEADDED, ::SDL_CONTROLLERDEVICEREMOVED, or ::SDL_CONTROLLERDEVICEREMAPPED */
    Uint32 timestamp;
    Sint32 which;       /**< The joystick device index for the ADDED event, instance id for the REMOVED or REMAPPED event */
} SDL_ControllerDeviceEvent;
typedef struct SDL_TouchFingerEvent
{
    Uint32 type;        /**< ::SDL_FINGERMOTION or ::SDL_FINGERDOWN or ::SDL_FINGERUP */
    Uint32 timestamp;
    SDL_TouchID touchId; /**< The touch device id */
    SDL_FingerID fingerId;
    float x;            /**< Normalized in the range 0...1 */
    float y;            /**< Normalized in the range 0...1 */
    float dx;           /**< Normalized in the range 0...1 */
    float dy;           /**< Normalized in the range 0...1 */
    float pressure;     /**< Normalized in the range 0...1 */
} SDL_TouchFingerEvent;
typedef struct SDL_MultiGestureEvent
{
    Uint32 type;        /**< ::SDL_MULTIGESTURE */
    Uint32 timestamp;
    SDL_TouchID touchId; /**< The touch device index */
    float dTheta;
    float dDist;
    float x;
    float y;
    Uint16 numFingers;
    Uint16 padding;
} SDL_MultiGestureEvent;
typedef struct SDL_DollarGestureEvent
{
    Uint32 type;        /**< ::SDL_DOLLARGESTURE */
    Uint32 timestamp;
    SDL_TouchID touchId; /**< The touch device id */
    SDL_GestureID gestureId;
    Uint32 numFingers;
    float error;
    float x;            /**< Normalized center of gesture */
    float y;            /**< Normalized center of gesture */
} SDL_DollarGestureEvent;
typedef struct SDL_DropEvent
{
    Uint32 type;        /**< ::SDL_DROPFILE */
    Uint32 timestamp;
    char *file;         /**< The file name, which should be freed with SDL_free() */
} SDL_DropEvent;
typedef struct SDL_QuitEvent
{
    Uint32 type;        /**< ::SDL_QUIT */
    Uint32 timestamp;
} SDL_QuitEvent;
typedef struct SDL_OSEvent
{
    Uint32 type;        /**< ::SDL_QUIT */
    Uint32 timestamp;
} SDL_OSEvent;
typedef struct SDL_UserEvent
{
    Uint32 type;        /**< ::SDL_USEREVENT through ::SDL_LASTEVENT-1 */
    Uint32 timestamp;
    Uint32 windowID;    /**< The associated window if any */
    Sint32 code;        /**< User defined event code */
    void *data1;        /**< User defined data pointer */
    void *data2;        /**< User defined data pointer */
} SDL_UserEvent;
struct SDL_SysWMmsg;
typedef struct SDL_SysWMmsg SDL_SysWMmsg;
typedef struct SDL_SysWMEvent
{
    Uint32 type;        /**< ::SDL_SYSWMEVENT */
    Uint32 timestamp;
    SDL_SysWMmsg *msg;  /**< driver dependent data, defined in SDL_syswm.h */
} SDL_SysWMEvent;
typedef union SDL_Event
{
    Uint32 type;                    /**< Event type, shared with all events */
    SDL_CommonEvent common;         /**< Common event data */
    SDL_WindowEvent window;         /**< Window event data */
    SDL_KeyboardEvent key;          /**< Keyboard event data */
    SDL_TextEditingEvent edit;      /**< Text editing event data */
    SDL_TextInputEvent text;        /**< Text input event data */
    SDL_MouseMotionEvent motion;    /**< Mouse motion event data */
    SDL_MouseButtonEvent button;    /**< Mouse button event data */
    SDL_MouseWheelEvent wheel;      /**< Mouse wheel event data */
    SDL_JoyAxisEvent jaxis;         /**< Joystick axis event data */
    SDL_JoyBallEvent jball;         /**< Joystick ball event data */
    SDL_JoyHatEvent jhat;           /**< Joystick hat event data */
    SDL_JoyButtonEvent jbutton;     /**< Joystick button event data */
    SDL_JoyDeviceEvent jdevice;     /**< Joystick device change event data */
    SDL_ControllerAxisEvent caxis;      /**< Game Controller axis event data */
    SDL_ControllerButtonEvent cbutton;  /**< Game Controller button event data */
    SDL_ControllerDeviceEvent cdevice;  /**< Game Controller device event data */
    SDL_QuitEvent quit;             /**< Quit request event data */
    SDL_UserEvent user;             /**< Custom event data */
    SDL_SysWMEvent syswm;           /**< System dependent window event data */
    SDL_TouchFingerEvent tfinger;   /**< Touch finger event data */
    SDL_MultiGestureEvent mgesture; /**< Gesture event data */
    SDL_DollarGestureEvent dgesture; /**< Gesture event data */
    SDL_DropEvent drop;             /**< Drag and drop event data */
    Uint8 padding[56];
} SDL_Event;
void SDL_PumpEvents(void);
typedef enum
{
    SDL_ADDEVENT,
    SDL_PEEKEVENT,
    SDL_GETEVENT
} SDL_eventaction;
int SDL_PeepEvents(SDL_Event * events, int numevents, SDL_eventaction action, Uint32 minType, Uint32 maxType);
SDL_bool SDL_HasEvent(Uint32 type);
SDL_bool SDL_HasEvents(Uint32 minType, Uint32 maxType);
void SDL_FlushEvent(Uint32 type);
void SDL_FlushEvents(Uint32 minType, Uint32 maxType);
int SDL_PollEvent(SDL_Event * event);
int SDL_WaitEvent(SDL_Event * event);
int SDL_WaitEventTimeout(SDL_Event * event, int timeout);
int SDL_PushEvent(SDL_Event * event);
typedef int (* SDL_EventFilter) (void *userdata, SDL_Event * event);
void SDL_SetEventFilter(SDL_EventFilter filter, void *userdata);
SDL_bool SDL_GetEventFilter(SDL_EventFilter * filter, void **userdata);
void SDL_AddEventWatch(SDL_EventFilter filter, void *userdata);
void SDL_DelEventWatch(SDL_EventFilter filter, void *userdata);
void SDL_FilterEvents(SDL_EventFilter filter, void *userdata);
#define SDL_QUERY   -1
#define SDL_IGNORE   0
#define SDL_DISABLE  0
#define SDL_ENABLE   1
Uint8 SDL_EventState(Uint32 type, int state);
#define SDL_GetEventState(type) SDL_EventState(type, SDL_QUERY)
Uint32 SDL_RegisterEvents(int numevents);

// SDL_filesystem.h

char *SDL_GetBasePath(void);
char *SDL_GetPrefPath(const char *org, const char *app);

// SDL_haptic.h

struct _SDL_Haptic;
typedef struct _SDL_Haptic SDL_Haptic;
#define SDL_HAPTIC_CONSTANT   (1<<0)
#define SDL_HAPTIC_SINE       (1<<1)
#define SDL_HAPTIC_LEFTRIGHT     (1<<2)
#define SDL_HAPTIC_TRIANGLE   (1<<3)
#define SDL_HAPTIC_SAWTOOTHUP (1<<4)
#define SDL_HAPTIC_SAWTOOTHDOWN (1<<5)
#define SDL_HAPTIC_RAMP       (1<<6)
#define SDL_HAPTIC_SPRING     (1<<7)
#define SDL_HAPTIC_DAMPER     (1<<8)
#define SDL_HAPTIC_INERTIA    (1<<9)
#define SDL_HAPTIC_FRICTION   (1<<10)
#define SDL_HAPTIC_CUSTOM     (1<<11)
#define SDL_HAPTIC_GAIN       (1<<12)
#define SDL_HAPTIC_AUTOCENTER (1<<13)
#define SDL_HAPTIC_STATUS     (1<<14)
#define SDL_HAPTIC_PAUSE      (1<<15)
#define SDL_HAPTIC_POLAR      0
#define SDL_HAPTIC_CARTESIAN  1
#define SDL_HAPTIC_SPHERICAL  2
#define SDL_HAPTIC_INFINITY   4294967295U
typedef struct SDL_HapticDirection
{
    Uint8 type;         /**< The type of encoding. */
    Sint32 dir[3];      /**< The encoded direction. */
} SDL_HapticDirection;
typedef struct SDL_HapticConstant
{
    /* Header */
    Uint16 type;            /**< ::SDL_HAPTIC_CONSTANT */
    SDL_HapticDirection direction;  /**< Direction of the effect. */
    /* Replay */
    Uint32 length;          /**< Duration of the effect. */
    Uint16 delay;           /**< Delay before starting the effect. */
    /* Trigger */
    Uint16 button;          /**< Button that triggers the effect. */
    Uint16 interval;        /**< How soon it can be triggered again after button. */
    /* Constant */
    Sint16 level;           /**< Strength of the constant effect. */
    /* Envelope */
    Uint16 attack_length;   /**< Duration of the attack. */
    Uint16 attack_level;    /**< Level at the start of the attack. */
    Uint16 fade_length;     /**< Duration of the fade. */
    Uint16 fade_level;      /**< Level at the end of the fade. */
} SDL_HapticConstant;
typedef struct SDL_HapticPeriodic
{
    /* Header */
    Uint16 type;        /**< ::SDL_HAPTIC_SINE, ::SDL_HAPTIC_LEFTRIGHT,
                             ::SDL_HAPTIC_TRIANGLE, ::SDL_HAPTIC_SAWTOOTHUP or
                             ::SDL_HAPTIC_SAWTOOTHDOWN */
    SDL_HapticDirection direction;  /**< Direction of the effect. */
    /* Replay */
    Uint32 length;      /**< Duration of the effect. */
    Uint16 delay;       /**< Delay before starting the effect. */
    /* Trigger */
    Uint16 button;      /**< Button that triggers the effect. */
    Uint16 interval;    /**< How soon it can be triggered again after button. */
    /* Periodic */
    Uint16 period;      /**< Period of the wave. */
    Sint16 magnitude;   /**< Peak value. */
    Sint16 offset;      /**< Mean value of the wave. */
    Uint16 phase;       /**< Horizontal shift given by hundredth of a cycle. */
    /* Envelope */
    Uint16 attack_length;   /**< Duration of the attack. */
    Uint16 attack_level;    /**< Level at the start of the attack. */
    Uint16 fade_length; /**< Duration of the fade. */
    Uint16 fade_level;  /**< Level at the end of the fade. */
} SDL_HapticPeriodic;
typedef struct SDL_HapticCondition
{
    /* Header */
    Uint16 type;            /**< ::SDL_HAPTIC_SPRING, ::SDL_HAPTIC_DAMPER,
                                 ::SDL_HAPTIC_INERTIA or ::SDL_HAPTIC_FRICTION */
    SDL_HapticDirection direction;  /**< Direction of the effect - Not used ATM. */
    /* Replay */
    Uint32 length;          /**< Duration of the effect. */
    Uint16 delay;           /**< Delay before starting the effect. */
    /* Trigger */
    Uint16 button;          /**< Button that triggers the effect. */
    Uint16 interval;        /**< How soon it can be triggered again after button. */
    /* Condition */
    Uint16 right_sat[3];    /**< Level when joystick is to the positive side. */
    Uint16 left_sat[3];     /**< Level when joystick is to the negative side. */
    Sint16 right_coeff[3];  /**< How fast to increase the force towards the positive side. */
    Sint16 left_coeff[3];   /**< How fast to increase the force towards the negative side. */
    Uint16 deadband[3];     /**< Size of the dead zone. */
    Sint16 center[3];       /**< Position of the dead zone. */
} SDL_HapticCondition;
typedef struct SDL_HapticRamp
{
    /* Header */
    Uint16 type;            /**< ::SDL_HAPTIC_RAMP */
    SDL_HapticDirection direction;  /**< Direction of the effect. */
    /* Replay */
    Uint32 length;          /**< Duration of the effect. */
    Uint16 delay;           /**< Delay before starting the effect. */
    /* Trigger */
    Uint16 button;          /**< Button that triggers the effect. */
    Uint16 interval;        /**< How soon it can be triggered again after button. */
    /* Ramp */
    Sint16 start;           /**< Beginning strength level. */
    Sint16 end;             /**< Ending strength level. */
    /* Envelope */
    Uint16 attack_length;   /**< Duration of the attack. */
    Uint16 attack_level;    /**< Level at the start of the attack. */
    Uint16 fade_length;     /**< Duration of the fade. */
    Uint16 fade_level;      /**< Level at the end of the fade. */
} SDL_HapticRamp;
typedef struct SDL_HapticLeftRight
{
    /* Header */
    Uint16 type;            /**< ::SDL_HAPTIC_LEFTRIGHT */
    /* Replay */
    Uint32 length;          /**< Duration of the effect. */
    /* Rumble */
    Uint16 large_magnitude; /**< Control of the large controller motor. */
    Uint16 small_magnitude; /**< Control of the small controller motor. */
} SDL_HapticLeftRight;
typedef struct SDL_HapticCustom
{
    /* Header */
    Uint16 type;            /**< ::SDL_HAPTIC_CUSTOM */
    SDL_HapticDirection direction;  /**< Direction of the effect. */
    /* Replay */
    Uint32 length;          /**< Duration of the effect. */
    Uint16 delay;           /**< Delay before starting the effect. */
    /* Trigger */
    Uint16 button;          /**< Button that triggers the effect. */
    Uint16 interval;        /**< How soon it can be triggered again after button. */
    /* Custom */
    Uint8 channels;         /**< Axes to use, minimum of one. */
    Uint16 period;          /**< Sample periods. */
    Uint16 samples;         /**< Amount of samples. */
    Uint16 *data;           /**< Should contain channels*samples items. */
    /* Envelope */
    Uint16 attack_length;   /**< Duration of the attack. */
    Uint16 attack_level;    /**< Level at the start of the attack. */
    Uint16 fade_length;     /**< Duration of the fade. */
    Uint16 fade_level;      /**< Level at the end of the fade. */
} SDL_HapticCustom;
typedef union SDL_HapticEffect
{
    /* Common for all force feedback effects */
    Uint16 type;                    /**< Effect type. */
    SDL_HapticConstant constant;    /**< Constant effect. */
    SDL_HapticPeriodic periodic;    /**< Periodic effect. */
    SDL_HapticCondition condition;  /**< Condition effect. */
    SDL_HapticRamp ramp;            /**< Ramp effect. */
    SDL_HapticLeftRight leftright;  /**< Left/Right effect. */
    SDL_HapticCustom custom;        /**< Custom effect. */
} SDL_HapticEffect;
int SDL_NumHaptics(void);
const char *SDL_HapticName(int device_index);
SDL_Haptic *SDL_HapticOpen(int device_index);
int SDL_HapticOpened(int device_index);
int SDL_HapticIndex(SDL_Haptic * haptic);
int SDL_MouseIsHaptic(void);
SDL_Haptic *SDL_HapticOpenFromMouse(void);
int SDL_JoystickIsHaptic(SDL_Joystick * joystick);
SDL_Haptic *SDL_HapticOpenFromJoystick(SDL_Joystick * joystick);
void SDL_HapticClose(SDL_Haptic * haptic);
int SDL_HapticNumEffects(SDL_Haptic * haptic);
int SDL_HapticNumEffectsPlaying(SDL_Haptic * haptic);
unsigned int SDL_HapticQuery(SDL_Haptic * haptic);
int SDL_HapticNumAxes(SDL_Haptic * haptic);
int SDL_HapticEffectSupported(SDL_Haptic * haptic, SDL_HapticEffect * effect);
int SDL_HapticNewEffect(SDL_Haptic * haptic, SDL_HapticEffect * effect);
int SDL_HapticUpdateEffect(SDL_Haptic * haptic, int effect, SDL_HapticEffect * data);
int SDL_HapticRunEffect(SDL_Haptic * haptic, int effect, Uint32 iterations);
int SDL_HapticStopEffect(SDL_Haptic * haptic, int effect);
void SDL_HapticDestroyEffect(SDL_Haptic * haptic, int effect);
int SDL_HapticGetEffectStatus(SDL_Haptic * haptic, int effect);
int SDL_HapticSetGain(SDL_Haptic * haptic, int gain);
int SDL_HapticSetAutocenter(SDL_Haptic * haptic, int autocenter);
int SDL_HapticPause(SDL_Haptic * haptic);
int SDL_HapticUnpause(SDL_Haptic * haptic);
int SDL_HapticStopAll(SDL_Haptic * haptic);
int SDL_HapticRumbleSupported(SDL_Haptic * haptic);
int SDL_HapticRumbleInit(SDL_Haptic * haptic);
int SDL_HapticRumblePlay(SDL_Haptic * haptic, float strength, Uint32 length );
int SDL_HapticRumbleStop(SDL_Haptic * haptic);

// SDL_hints.h

#define SDL_HINT_FRAMEBUFFER_ACCELERATION   "SDL_FRAMEBUFFER_ACCELERATION"
#define SDL_HINT_RENDER_DRIVER              "SDL_RENDER_DRIVER"
#define SDL_HINT_RENDER_OPENGL_SHADERS      "SDL_RENDER_OPENGL_SHADERS"
#define SDL_HINT_RENDER_DIRECT3D_THREADSAFE "SDL_RENDER_DIRECT3D_THREADSAFE"
#define SDL_HINT_RENDER_DIRECT3D11_DEBUG    "SDL_HINT_RENDER_DIRECT3D11_DEBUG"
#define SDL_HINT_RENDER_SCALE_QUALITY       "SDL_RENDER_SCALE_QUALITY"
#define SDL_HINT_RENDER_VSYNC               "SDL_RENDER_VSYNC"
#define SDL_HINT_VIDEO_ALLOW_SCREENSAVER    "SDL_VIDEO_ALLOW_SCREENSAVER"
#define SDL_HINT_VIDEO_X11_XVIDMODE         "SDL_VIDEO_X11_XVIDMODE"
#define SDL_HINT_VIDEO_X11_XINERAMA         "SDL_VIDEO_X11_XINERAMA"
#define SDL_HINT_VIDEO_X11_XRANDR           "SDL_VIDEO_X11_XRANDR"
#define SDL_HINT_GRAB_KEYBOARD              "SDL_GRAB_KEYBOARD"
#define SDL_HINT_MOUSE_RELATIVE_MODE_WARP    "SDL_MOUSE_RELATIVE_MODE_WARP"
#define SDL_HINT_VIDEO_MINIMIZE_ON_FOCUS_LOSS   "SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS"
#define SDL_HINT_IDLE_TIMER_DISABLED "SDL_IOS_IDLE_TIMER_DISABLED"
#define SDL_HINT_ORIENTATIONS "SDL_IOS_ORIENTATIONS"
#define SDL_HINT_ACCELEROMETER_AS_JOYSTICK "SDL_ACCELEROMETER_AS_JOYSTICK"
#define SDL_HINT_XINPUT_ENABLED "SDL_XINPUT_ENABLED"
#define SDL_HINT_GAMECONTROLLERCONFIG "SDL_GAMECONTROLLERCONFIG"
#define SDL_HINT_JOYSTICK_ALLOW_BACKGROUND_EVENTS "SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"
#define SDL_HINT_ALLOW_TOPMOST "SDL_ALLOW_TOPMOST"
#define SDL_HINT_TIMER_RESOLUTION "SDL_TIMER_RESOLUTION"
#define SDL_HINT_VIDEO_HIGHDPI_DISABLED "SDL_VIDEO_HIGHDPI_DISABLED"
#define SDL_HINT_MAC_CTRL_CLICK_EMULATE_RIGHT_CLICK "SDL_MAC_CTRL_CLICK_EMULATE_RIGHT_CLICK"
#define SDL_HINT_VIDEO_WIN_D3DCOMPILER              "SDL_VIDEO_WIN_D3DCOMPILER"
#define SDL_HINT_VIDEO_WINDOW_SHARE_PIXEL_FORMAT    "SDL_VIDEO_WINDOW_SHARE_PIXEL_FORMAT"
#define SDL_HINT_WINRT_PRIVACY_POLICY_URL "SDL_HINT_WINRT_PRIVACY_POLICY_URL"
#define SDL_HINT_WINRT_PRIVACY_POLICY_LABEL "SDL_HINT_WINRT_PRIVACY_POLICY_LABEL"
#define SDL_HINT_WINRT_HANDLE_BACK_BUTTON "SDL_HINT_WINRT_HANDLE_BACK_BUTTON"
#define SDL_HINT_VIDEO_MAC_FULLSCREEN_SPACES    "SDL_VIDEO_MAC_FULLSCREEN_SPACES"
typedef enum
{
    SDL_HINT_DEFAULT,
    SDL_HINT_NORMAL,
    SDL_HINT_OVERRIDE
} SDL_HintPriority;
SDL_bool SDL_SetHintWithPriority(const char *name, const char *value, SDL_HintPriority priority);
SDL_bool SDL_SetHint(const char *name, const char *value);
const char * SDL_GetHint(const char *name);
typedef void (*SDL_HintCallback)(void *userdata, const char *name, const char *oldValue, const char *newValue);
void SDL_AddHintCallback(const char *name, SDL_HintCallback callback, void *userdata);
void SDL_DelHintCallback(const char *name, SDL_HintCallback callback, void *userdata);
void SDL_ClearHints(void);

// SDL_loadso.h

void *SDL_LoadObject(const char *sofile);
void *SDL_LoadFunction(void *handle, const char *name);
void SDL_UnloadObject(void *handle);

// SDL_log.h

#define SDL_MAX_LOG_MESSAGE 4096
enum
{
    SDL_LOG_CATEGORY_APPLICATION,
    SDL_LOG_CATEGORY_ERROR,
    SDL_LOG_CATEGORY_ASSERT,
    SDL_LOG_CATEGORY_SYSTEM,
    SDL_LOG_CATEGORY_AUDIO,
    SDL_LOG_CATEGORY_VIDEO,
    SDL_LOG_CATEGORY_RENDER,
    SDL_LOG_CATEGORY_INPUT,
    SDL_LOG_CATEGORY_TEST,

    /* Reserved for future SDL library use */
    SDL_LOG_CATEGORY_RESERVED1,
    SDL_LOG_CATEGORY_RESERVED2,
    SDL_LOG_CATEGORY_RESERVED3,
    SDL_LOG_CATEGORY_RESERVED4,
    SDL_LOG_CATEGORY_RESERVED5,
    SDL_LOG_CATEGORY_RESERVED6,
    SDL_LOG_CATEGORY_RESERVED7,
    SDL_LOG_CATEGORY_RESERVED8,
    SDL_LOG_CATEGORY_RESERVED9,
    SDL_LOG_CATEGORY_RESERVED10,

    /* Beyond this point is reserved for application use, e.g.
       enum {
           MYAPP_CATEGORY_AWESOME1 = SDL_LOG_CATEGORY_CUSTOM,
           MYAPP_CATEGORY_AWESOME2,
           MYAPP_CATEGORY_AWESOME3,
           ...
       };
     */
    SDL_LOG_CATEGORY_CUSTOM
};
typedef enum
{
    SDL_LOG_PRIORITY_VERBOSE = 1,
    SDL_LOG_PRIORITY_DEBUG,
    SDL_LOG_PRIORITY_INFO,
    SDL_LOG_PRIORITY_WARN,
    SDL_LOG_PRIORITY_ERROR,
    SDL_LOG_PRIORITY_CRITICAL,
    SDL_NUM_LOG_PRIORITIES
} SDL_LogPriority;
void SDL_LogSetAllPriority(SDL_LogPriority priority);
void SDL_LogSetPriority(int category, SDL_LogPriority priority);
SDL_LogPriority SDL_LogGetPriority(int category);
void SDL_LogResetPriorities(void);
void SDL_Log(const char *fmt, ...);
void SDL_LogVerbose(int category, const char *fmt, ...);
void SDL_LogDebug(int category, const char *fmt, ...);
void SDL_LogInfo(int category, const char *fmt, ...);
void SDL_LogWarn(int category, const char *fmt, ...);
void SDL_LogError(int category, const char *fmt, ...);
void SDL_LogCritical(int category, const char *fmt, ...);
void SDL_LogMessage(int category, SDL_LogPriority priority, const char *fmt, ...);
void SDL_LogMessageV(int category, SDL_LogPriority priority, const char *fmt, va_list ap);
typedef void (*SDL_LogOutputFunction)(void *userdata, int category, SDL_LogPriority priority, const char *message);
void SDL_LogGetOutputFunction(SDL_LogOutputFunction *callback, void **userdata);
void SDL_LogSetOutputFunction(SDL_LogOutputFunction callback, void *userdata);

// SDL_messagebox.h

typedef enum
{
    SDL_MESSAGEBOX_ERROR        = 0x00000010,   /**< error dialog */
    SDL_MESSAGEBOX_WARNING      = 0x00000020,   /**< warning dialog */
    SDL_MESSAGEBOX_INFORMATION  = 0x00000040    /**< informational dialog */
} SDL_MessageBoxFlags;
typedef enum
{
    SDL_MESSAGEBOX_BUTTON_RETURNKEY_DEFAULT = 0x00000001,  /**< Marks the default button when return is hit */
    SDL_MESSAGEBOX_BUTTON_ESCAPEKEY_DEFAULT = 0x00000002   /**< Marks the default button when escape is hit */
} SDL_MessageBoxButtonFlags;
typedef struct
{
    Uint32 flags;       /**< ::SDL_MessageBoxButtonFlags */
    int buttonid;       /**< User defined button id (value returned via SDL_ShowMessageBox) */
    const char * text;  /**< The UTF-8 button text */
} SDL_MessageBoxButtonData;
typedef struct
{
    Uint8 r, g, b;
} SDL_MessageBoxColor;
typedef enum
{
    SDL_MESSAGEBOX_COLOR_BACKGROUND,
    SDL_MESSAGEBOX_COLOR_TEXT,
    SDL_MESSAGEBOX_COLOR_BUTTON_BORDER,
    SDL_MESSAGEBOX_COLOR_BUTTON_BACKGROUND,
    SDL_MESSAGEBOX_COLOR_BUTTON_SELECTED,
    SDL_MESSAGEBOX_COLOR_MAX
} SDL_MessageBoxColorType;
typedef struct
{
    SDL_MessageBoxColor colors[SDL_MESSAGEBOX_COLOR_MAX];
} SDL_MessageBoxColorScheme;
typedef struct
{
    Uint32 flags;                       /**< ::SDL_MessageBoxFlags */
    SDL_Window *window;                 /**< Parent window, can be NULL */
    const char *title;                  /**< UTF-8 title */
    const char *message;                /**< UTF-8 message text */
    int numbuttons;
    const SDL_MessageBoxButtonData *buttons;
    const SDL_MessageBoxColorScheme *colorScheme;   /**< ::SDL_MessageBoxColorScheme, can be NULL to use system settings */
} SDL_MessageBoxData;
int SDL_ShowMessageBox(const SDL_MessageBoxData *messageboxdata, int *buttonid);
int SDL_ShowSimpleMessageBox(Uint32 flags, const char *title, const char *message, SDL_Window *window);

// SDL_power.h

typedef enum
{
    SDL_POWERSTATE_UNKNOWN,      /**< cannot determine power status */
    SDL_POWERSTATE_ON_BATTERY,   /**< Not plugged in, running on the battery */
    SDL_POWERSTATE_NO_BATTERY,   /**< Plugged in, no battery available */
    SDL_POWERSTATE_CHARGING,     /**< Plugged in, charging battery */
    SDL_POWERSTATE_CHARGED       /**< Plugged in, battery charged */
} SDL_PowerState;
SDL_PowerState SDL_GetPowerInfo(int *secs, int *pct);

// SDL_render.h

typedef enum
{
    SDL_RENDERER_SOFTWARE = 0x00000001,         /**< The renderer is a software fallback */
    SDL_RENDERER_ACCELERATED = 0x00000002,      /**< The renderer uses hardware acceleration */
    SDL_RENDERER_PRESENTVSYNC = 0x00000004,     /**< Present is synchronized with the refresh rate */
    SDL_RENDERER_TARGETTEXTURE = 0x00000008     /**< The renderer supports rendering to texture */
} SDL_RendererFlags;
typedef struct SDL_RendererInfo
{
    const char *name;           /**< The name of the renderer */
    Uint32 flags;               /**< Supported ::SDL_RendererFlags */
    Uint32 num_texture_formats; /**< The number of available texture formats */
    Uint32 texture_formats[16]; /**< The available texture formats */
    int max_texture_width;      /**< The maximimum texture width */
    int max_texture_height;     /**< The maximimum texture height */
} SDL_RendererInfo;
typedef enum
{
    SDL_TEXTUREACCESS_STATIC,    /**< Changes rarely, not lockable */
    SDL_TEXTUREACCESS_STREAMING, /**< Changes frequently, lockable */
    SDL_TEXTUREACCESS_TARGET     /**< Texture can be used as a render target */
} SDL_TextureAccess;
typedef enum
{
    SDL_TEXTUREMODULATE_NONE = 0x00000000,     /**< No modulation */
    SDL_TEXTUREMODULATE_COLOR = 0x00000001,    /**< srcC = srcC * color */
    SDL_TEXTUREMODULATE_ALPHA = 0x00000002     /**< srcA = srcA * alpha */
} SDL_TextureModulate;
typedef enum
{
    SDL_FLIP_NONE = 0x00000000,     /**< Do not flip */
    SDL_FLIP_HORIZONTAL = 0x00000001,    /**< flip horizontally */
    SDL_FLIP_VERTICAL = 0x00000002     /**< flip vertically */
} SDL_RendererFlip;
struct SDL_Renderer;
typedef struct SDL_Renderer SDL_Renderer;
struct SDL_Texture;
typedef struct SDL_Texture SDL_Texture;
int SDL_GetNumRenderDrivers(void);
int SDL_GetRenderDriverInfo(int index, SDL_RendererInfo * info);
int SDL_CreateWindowAndRenderer(int width, int height, Uint32 window_flags, SDL_Window **window, SDL_Renderer **renderer);
SDL_Renderer * SDL_CreateRenderer(SDL_Window * window, int index, Uint32 flags);
SDL_Renderer * SDL_CreateSoftwareRenderer(SDL_Surface * surface);
SDL_Renderer * SDL_GetRenderer(SDL_Window * window);
int SDL_GetRendererInfo(SDL_Renderer * renderer, SDL_RendererInfo * info);
int SDL_GetRendererOutputSize(SDL_Renderer * renderer, int *w, int *h);
SDL_Texture * SDL_CreateTexture(SDL_Renderer * renderer, Uint32 format, int access, int w, int h);
SDL_Texture * SDL_CreateTextureFromSurface(SDL_Renderer * renderer, SDL_Surface * surface);
int SDL_QueryTexture(SDL_Texture * texture, Uint32 * format, int *access, int *w, int *h);
int SDL_SetTextureColorMod(SDL_Texture * texture, Uint8 r, Uint8 g, Uint8 b);
int SDL_GetTextureColorMod(SDL_Texture * texture, Uint8 * r, Uint8 * g, Uint8 * b);
int SDL_SetTextureAlphaMod(SDL_Texture * texture, Uint8 alpha);
int SDL_GetTextureAlphaMod(SDL_Texture * texture, Uint8 * alpha);
int SDL_SetTextureBlendMode(SDL_Texture * texture, SDL_BlendMode blendMode);
int SDL_GetTextureBlendMode(SDL_Texture * texture, SDL_BlendMode *blendMode);
int SDL_UpdateTexture(SDL_Texture * texture, const SDL_Rect * rect, const void *pixels, int pitch);
int SDL_UpdateYUVTexture(SDL_Texture * texture, const SDL_Rect * rect, const Uint8 *Yplane, int Ypitch, const Uint8 *Uplane, int Upitch, const Uint8 *Vplane, int Vpitch);
int SDL_LockTexture(SDL_Texture * texture, const SDL_Rect * rect, void **pixels, int *pitch);
void SDL_UnlockTexture(SDL_Texture * texture);
SDL_bool SDL_RenderTargetSupported(SDL_Renderer *renderer);
int SDL_SetRenderTarget(SDL_Renderer *renderer, SDL_Texture *texture);
SDL_Texture * SDL_GetRenderTarget(SDL_Renderer *renderer);
int SDL_RenderSetLogicalSize(SDL_Renderer * renderer, int w, int h);
void SDL_RenderGetLogicalSize(SDL_Renderer * renderer, int *w, int *h);
int SDL_RenderSetViewport(SDL_Renderer * renderer, const SDL_Rect * rect);
void SDL_RenderGetViewport(SDL_Renderer * renderer, SDL_Rect * rect);
int SDL_RenderSetClipRect(SDL_Renderer * renderer, const SDL_Rect * rect);
void SDL_RenderGetClipRect(SDL_Renderer * renderer, SDL_Rect * rect);
int SDL_RenderSetScale(SDL_Renderer * renderer, float scaleX, float scaleY);
void SDL_RenderGetScale(SDL_Renderer * renderer, float *scaleX, float *scaleY);
int SDL_SetRenderDrawColor(SDL_Renderer * renderer, Uint8 r, Uint8 g, Uint8 b, Uint8 a);
int SDL_GetRenderDrawColor(SDL_Renderer * renderer, Uint8 * r, Uint8 * g, Uint8 * b, Uint8 * a);
int SDL_SetRenderDrawBlendMode(SDL_Renderer * renderer, SDL_BlendMode blendMode);
int SDL_GetRenderDrawBlendMode(SDL_Renderer * renderer, SDL_BlendMode *blendMode);
int SDL_RenderClear(SDL_Renderer * renderer);
int SDL_RenderDrawPoint(SDL_Renderer * renderer, int x, int y);
int SDL_RenderDrawPoints(SDL_Renderer * renderer, const SDL_Point * points, int count);
int SDL_RenderDrawLine(SDL_Renderer * renderer, int x1, int y1, int x2, int y2);
int SDL_RenderDrawLines(SDL_Renderer * renderer, const SDL_Point * points, int count);
int SDL_RenderDrawRect(SDL_Renderer * renderer, const SDL_Rect * rect);
int SDL_RenderDrawRects(SDL_Renderer * renderer, const SDL_Rect * rects, int count);
int SDL_RenderFillRect(SDL_Renderer * renderer, const SDL_Rect * rect);
int SDL_RenderFillRects(SDL_Renderer * renderer, const SDL_Rect * rects, int count);
int SDL_RenderCopy(SDL_Renderer * renderer, SDL_Texture * texture, const SDL_Rect * srcrect, const SDL_Rect * dstrect);
int SDL_RenderCopyEx(SDL_Renderer * renderer, SDL_Texture * texture, const SDL_Rect * srcrect, const SDL_Rect * dstrect, const double angle, const SDL_Point *center, const SDL_RendererFlip flip);
int SDL_RenderReadPixels(SDL_Renderer * renderer, const SDL_Rect * rect, Uint32 format, void *pixels, int pitch);
void SDL_RenderPresent(SDL_Renderer * renderer);
void SDL_DestroyTexture(SDL_Texture * texture);
void SDL_DestroyRenderer(SDL_Renderer * renderer);
int SDL_GL_BindTexture(SDL_Texture *texture, float *texw, float *texh);
int SDL_GL_UnbindTexture(SDL_Texture *texture);

// SDL_system.h

int SDL_Direct3D9GetAdapterIndex( int displayIndex );
typedef struct IDirect3DDevice9 IDirect3DDevice9;
IDirect3DDevice9* SDL_RenderGetD3D9Device(SDL_Renderer * renderer);
void SDL_DXGIGetOutputInfo( int displayIndex, int *adapterIndex, int *outputIndex );
int SDL_iPhoneSetAnimationCallback(SDL_Window * window, int interval, void (*callback)(void*), void *callbackParam);
void SDL_iPhoneSetEventPump(SDL_bool enabled);
void * SDL_AndroidGetJNIEnv();
void * SDL_AndroidGetActivity();
#define SDL_ANDROID_EXTERNAL_STORAGE_READ   0x01
#define SDL_ANDROID_EXTERNAL_STORAGE_WRITE  0x02
const char * SDL_AndroidGetInternalStoragePath();
int SDL_AndroidGetExternalStorageState();
const char * SDL_AndroidGetExternalStoragePath();
typedef enum
{
    /** \brief The installed app's root directory.
        Files here are likely to be read-only. */
    SDL_WINRT_PATH_INSTALLED_LOCATION,
    /** \brief The app's local data store.  Files may be written here */
    SDL_WINRT_PATH_LOCAL_FOLDER,
    /** \brief The app's roaming data store.  Unsupported on Windows Phone.
        Files written here may be copied to other machines via a network
        connection.
    */
    SDL_WINRT_PATH_ROAMING_FOLDER,
    /** \brief The app's temporary data store.  Unsupported on Windows Phone.
        Files written here may be deleted at any time. */
    SDL_WINRT_PATH_TEMP_FOLDER
} SDL_WinRT_Path;
const wchar_t * SDL_WinRTGetFSPathUNICODE(SDL_WinRT_Path pathType);
const char * SDL_WinRTGetFSPathUTF8(SDL_WinRT_Path pathType);

// SDL_timer.h

Uint32 SDL_GetTicks(void);
#define SDL_TICKS_PASSED(A, B)  ((Sint32)((B) - (A)) <= 0)
Uint64 SDL_GetPerformanceCounter(void);
Uint64 SDL_GetPerformanceFrequency(void);
void SDL_Delay(Uint32 ms);
typedef Uint32 (* SDL_TimerCallback) (Uint32 interval, void *param);
typedef int SDL_TimerID;
SDL_TimerID SDL_AddTimer(Uint32 interval, SDL_TimerCallback callback, void *param);
SDL_bool SDL_RemoveTimer(SDL_TimerID id);

// SDL_version.h

typedef struct SDL_version
{
    Uint8 major;        /**< major version */
    Uint8 minor;        /**< minor version */
    Uint8 patch;        /**< update version */
} SDL_version;
#define SDL_MAJOR_VERSION   2
#define SDL_MINOR_VERSION   0
#define SDL_PATCHLEVEL      3
#define SDL_VERSION(x) { (x)->major = SDL_MAJOR_VERSION; (x)->minor = SDL_MINOR_VERSION; (x)->patch = SDL_PATCHLEVEL; }
#define SDL_VERSIONNUM(X, Y, Z)  ((X)*1000 + (Y)*100 + (Z))
#define SDL_COMPILEDVERSION  SDL_VERSIONNUM(SDL_MAJOR_VERSION, SDL_MINOR_VERSION, SDL_PATCHLEVEL)
#define SDL_VERSION_ATLEAST(X, Y, Z)  (SDL_COMPILEDVERSION >= SDL_VERSIONNUM(X, Y, Z))
void SDL_GetVersion(SDL_version * ver);
const char *SDL_GetRevision(void);
int SDL_GetRevisionNumber(void);

// SDL.h

#define SDL_INIT_TIMER          0x00000001
#define SDL_INIT_AUDIO          0x00000010
#define SDL_INIT_VIDEO          0x00000020  /**< SDL_INIT_VIDEO implies SDL_INIT_EVENTS */
#define SDL_INIT_JOYSTICK       0x00000200  /**< SDL_INIT_JOYSTICK implies SDL_INIT_EVENTS */
#define SDL_INIT_HAPTIC         0x00001000
#define SDL_INIT_GAMECONTROLLER 0x00002000  /**< SDL_INIT_GAMECONTROLLER implies SDL_INIT_JOYSTICK */
#define SDL_INIT_EVENTS         0x00004000
#define SDL_INIT_NOPARACHUTE    0x00100000  /**< Don't catch fatal signals */
#define SDL_INIT_EVERYTHING (SDL_INIT_TIMER | SDL_INIT_AUDIO | SDL_INIT_VIDEO | SDL_INIT_EVENTS | SDL_INIT_JOYSTICK | SDL_INIT_HAPTIC | SDL_INIT_GAMECONTROLLER)
int SDL_Init(Uint32 flags);
int SDL_InitSubSystem(Uint32 flags);
void SDL_QuitSubSystem(Uint32 flags);
Uint32 SDL_WasInit(Uint32 flags);
void SDL_Quit(void);

"""


get_cdefs(ffi)
