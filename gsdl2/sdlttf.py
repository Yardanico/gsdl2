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
const SDL_version * TTF_Linked_Version(void);
void TTF_ByteSwappedUNICODE(int swapped);
typedef struct _TTF_Font TTF_Font;
int TTF_Init(void);
TTF_Font * TTF_OpenFont(const char *file, int ptsize);
TTF_Font * TTF_OpenFontIndex(const char *file, int ptsize, long index);
TTF_Font * TTF_OpenFontRW(SDL_RWops *src, int freesrc, int ptsize);
TTF_Font * TTF_OpenFontIndexRW(SDL_RWops *src, int freesrc, int ptsize, long index);
int TTF_GetFontStyle(const TTF_Font *font);
void TTF_SetFontStyle(TTF_Font *font, int style);
int TTF_GetFontOutline(const TTF_Font *font);
void TTF_SetFontOutline(TTF_Font *font, int outline);
int TTF_GetFontHinting(const TTF_Font *font);
void TTF_SetFontHinting(TTF_Font *font, int hinting);
int TTF_FontHeight(const TTF_Font *font);
int TTF_FontAscent(const TTF_Font *font);
int TTF_FontDescent(const TTF_Font *font);
int TTF_FontLineSkip(const TTF_Font *font);
int TTF_GetFontKerning(const TTF_Font *font);
void TTF_SetFontKerning(TTF_Font *font, int allowed);
long TTF_FontFaces(const TTF_Font *font);
int TTF_FontFaceIsFixedWidth(const TTF_Font *font);
char * TTF_FontFaceFamilyName(const TTF_Font *font);
char * TTF_FontFaceStyleName(const TTF_Font *font);
int TTF_GlyphIsProvided(const TTF_Font *font, Uint16 ch);
int TTF_GlyphMetrics(TTF_Font *font, Uint16 ch, int *minx, int *maxx, int *miny, int *maxy, int *advance);
int TTF_SizeText(TTF_Font *font, const char *text, int *w, int *h);
int TTF_SizeUTF8(TTF_Font *font, const char *text, int *w, int *h);
int TTF_SizeUNICODE(TTF_Font *font, const Uint16 *text, int *w, int *h);
SDL_Surface * TTF_RenderText_Solid(TTF_Font *font, const char *text, SDL_Color fg);
SDL_Surface * TTF_RenderUTF8_Solid(TTF_Font *font, const char *text, SDL_Color fg);
SDL_Surface * TTF_RenderUNICODE_Solid(TTF_Font *font, const Uint16 *text, SDL_Color fg);
SDL_Surface * TTF_RenderGlyph_Solid(TTF_Font *font, Uint16 ch, SDL_Color fg);
SDL_Surface * TTF_RenderText_Shaded(TTF_Font *font, const char *text, SDL_Color fg, SDL_Color bg);
SDL_Surface * TTF_RenderUTF8_Shaded(TTF_Font *font, const char *text, SDL_Color fg, SDL_Color bg);
SDL_Surface * TTF_RenderUNICODE_Shaded(TTF_Font *font, const Uint16 *text, SDL_Color fg, SDL_Color bg);
SDL_Surface * TTF_RenderGlyph_Shaded(TTF_Font *font, Uint16 ch, SDL_Color fg, SDL_Color bg);
SDL_Surface * TTF_RenderText_Blended(TTF_Font *font, const char *text, SDL_Color fg);
SDL_Surface * TTF_RenderUTF8_Blended(TTF_Font *font, const char *text, SDL_Color fg);
SDL_Surface * TTF_RenderUNICODE_Blended(TTF_Font *font, const Uint16 *text, SDL_Color fg);
SDL_Surface * TTF_RenderText_Blended_Wrapped(TTF_Font *font, const char *text, SDL_Color fg, Uint32 wrapLength);
SDL_Surface * TTF_RenderUTF8_Blended_Wrapped(TTF_Font *font, const char *text, SDL_Color fg, Uint32 wrapLength);
SDL_Surface * TTF_RenderUNICODE_Blended_Wrapped(TTF_Font *font, const Uint16 *text, SDL_Color fg, Uint32 wrapLength);
SDL_Surface * TTF_RenderGlyph_Blended(TTF_Font *font, Uint16 ch, SDL_Color fg);
void TTF_CloseFont(TTF_Font *font);
void TTF_Quit(void);
int TTF_WasInit(void);
int TTF_GetFontKerningSize(TTF_Font *font, int prev_index, int index);
"""


get_cdefs(ffi)
