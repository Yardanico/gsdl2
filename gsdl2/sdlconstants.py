import sys

SDL_LIL_ENDIAN = 1234
SDL_BIG_ENDIAN = 4321

if sys.platform == 'linux':
    # include <endian.h>
    # define SDL_BYTEORDER  __BYTE_ORDER
    SDL_BYTEORDER = SDL_LIL_ENDIAN
    pass
elif sys.platform in ('hppa', 'm68k', 'mc68000', 'M_M68K', 'MIPS', 'MISPEB', 'ppc', 'POWERPC', 'M_PPC', 'sparc'):
    SDL_BYTEORDER = SDL_BIG_ENDIAN
else:
    SDL_BYTEORDER = SDL_LIL_ENDIAN
