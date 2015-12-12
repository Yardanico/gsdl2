#!/usr/bin/env python

__all__ = ['ffi', 'parse_headers']


import re

import cffi

from . import sdl


ffi = cffi.FFI()
ffi.include(sdl.ffi)


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
const SDL_version * IMG_Linked_Version(void);
typedef enum
{
    IMG_INIT_JPG = 0x00000001,
    IMG_INIT_PNG = 0x00000002,
    IMG_INIT_TIF = 0x00000004,
    IMG_INIT_WEBP = 0x00000008
} IMG_InitFlags;
int IMG_Init(int flags);
void IMG_Quit(void);
SDL_Surface * IMG_LoadTyped_RW(SDL_RWops *src, int freesrc, const char *type);
SDL_Surface * IMG_Load(const char *file);
SDL_Surface * IMG_Load_RW(SDL_RWops *src, int freesrc);
SDL_Texture * IMG_LoadTexture(SDL_Renderer *renderer, const char *file);
SDL_Texture * IMG_LoadTexture_RW(SDL_Renderer *renderer, SDL_RWops *src, int freesrc);
SDL_Texture * IMG_LoadTextureTyped_RW(SDL_Renderer *renderer, SDL_RWops *src, int freesrc, const char *type);
int IMG_isICO(SDL_RWops *src);
int IMG_isCUR(SDL_RWops *src);
int IMG_isBMP(SDL_RWops *src);
int IMG_isGIF(SDL_RWops *src);
int IMG_isJPG(SDL_RWops *src);
int IMG_isLBM(SDL_RWops *src);
int IMG_isPCX(SDL_RWops *src);
int IMG_isPNG(SDL_RWops *src);
int IMG_isPNM(SDL_RWops *src);
int IMG_isTIF(SDL_RWops *src);
int IMG_isXCF(SDL_RWops *src);
int IMG_isXPM(SDL_RWops *src);
int IMG_isXV(SDL_RWops *src);
int IMG_isWEBP(SDL_RWops *src);
SDL_Surface * IMG_LoadICO_RW(SDL_RWops *src);
SDL_Surface * IMG_LoadCUR_RW(SDL_RWops *src);
SDL_Surface * IMG_LoadBMP_RW(SDL_RWops *src);
SDL_Surface * IMG_LoadGIF_RW(SDL_RWops *src);
SDL_Surface * IMG_LoadJPG_RW(SDL_RWops *src);
SDL_Surface * IMG_LoadLBM_RW(SDL_RWops *src);
SDL_Surface * IMG_LoadPCX_RW(SDL_RWops *src);
SDL_Surface * IMG_LoadPNG_RW(SDL_RWops *src);
SDL_Surface * IMG_LoadPNM_RW(SDL_RWops *src);
SDL_Surface * IMG_LoadTGA_RW(SDL_RWops *src);
SDL_Surface * IMG_LoadTIF_RW(SDL_RWops *src);
SDL_Surface * IMG_LoadXCF_RW(SDL_RWops *src);
SDL_Surface * IMG_LoadXPM_RW(SDL_RWops *src);
SDL_Surface * IMG_LoadXV_RW(SDL_RWops *src);
SDL_Surface * IMG_LoadWEBP_RW(SDL_RWops *src);
SDL_Surface * IMG_ReadXPMFromArray(char **xpm);
int IMG_SavePNG(SDL_Surface *surface, const char *file);
int IMG_SavePNG_RW(SDL_Surface *surface, SDL_RWops *dst, int freedst);
"""


get_cdefs(ffi)

