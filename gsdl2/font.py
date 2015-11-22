__all__ = ['Font', 'SysFont']


import logging
import os

from .sdllibs import *
from .sdlffi import sdl_ffi, ttf_ffi
from .sdlconstants import (
    TTF_STYLE_NORMAL,
    TTF_STYLE_BOLD,
    TTF_STYLE_ITALIC,
    TTF_STYLE_UNDERLINE,
    TTF_STYLE_STRIKETHROUGH,
    TTF_HINTING_NORMAL,
    TTF_HINTING_LIGHT,
    TTF_HINTING_MONO,
    TTF_HINTING_NONE,
)
from .locals import utf8


log = logging.getLogger(__name__)


class Font(object):

    def __init__(self, filename, pointsize):
        self.__filename = filename
        self.__pointsize = pointsize
        assert os.access(filename, os.F_OK)

        self.__sdl_font = ttf_lib.TTF_OpenFont(utf8(filename), pointsize)
        if self.__sdl_font == sdl_ffi.NULL:
            log.critical(sdl_ffi.string(sdl_lib.SDL_GetError()).decode('utf-8'))
            raise SDLError()

    def render(self, text, color, background=None, encoding='utf-8', wrap_length=0, palette=False):
        """render text, returning a Surface

        If palette is True: the TTF_RenderSolid* routines are used.
        If wrap_length > 0: the TTF_RenderBlendedWrapped* routines are used.
        If background is not None: the TTF_RenderShaded* routined are used.
        Else: the TTF_RenderBlended* routines (not wrapped) are used.

        :param text: string; the text to render
        :param color: color.Color; foreground color
        :param background: color.Color; (optional) background colod
        :param encoding: one of: 'utf-8', 'ascii', 'unicode', 'glyph'
        :param wrap_length: pixel width to wrap text; 0 (zero) means no wrapping
        :param palette: use 8-bit palette rendering
        :return:
        """
        if background:
            sdl_surf = self._render_shaded(text, color, background, encoding)
        elif wrap_length:
            if encoding == 'glyph':
                sdl_surf = self._render_blended(text, color, encoding)
            else:
                sdl_surf = self._render_blended_wrapped(text, color, encoding, wrap_length)
        elif palette:
            sdl_surf = self._render_solid(text, color, encoding)
        else:
            sdl_surf = self._render_blended(text, color, encoding)

        if sdl_surf == sdl_ffi.NULL:
            raise SDLError()

        return Surface((sdl_surf.w, sdl_surf.h), surface=sdl_surf)

    def _render_shaded(self, text, color, background, encoding):
        """
        SDL_Surface * TTF_RenderUTF8_Shaded(TTF_Font *font, const char *text, SDL_Color fg, SDL_Color bg);
        SDL_Surface * TTF_RenderText_Shaded(TTF_Font *font, const char *text, SDL_Color fg, SDL_Color bg);
        SDL_Surface * TTF_RenderUNICODE_Shaded(TTF_Font *font, const Uint16 *text, SDL_Color fg, SDL_Color bg);
        SDL_Surface * TTF_RenderGlyph_Shaded(TTF_Font *font, Uint16 ch, SDL_Color fg, SDL_Color bg);
        """
        if encoding == 'utf-8':
            sdl_surf = ttf_lib.TTF_RenderUTF8_Shaded(
                self.__sdl_font, utf8(text), color.sdl_color[0], background.sdl_color[0])
        elif encoding == 'ascii':
            sdl_surf = ttf_lib.TTF_RenderText_Shaded(
                self.__sdl_font, text, color.sdl_color[0], background.sdl_color[0])
        elif encoding == 'unicode':
            sdl_surf = ttf_lib.TTF_RenderUNICODE_Shaded(
                self.__sdl_font, text, color.sdl_color[0], background.sdl_color[0])
        elif encoding == 'glyph':
            sdl_surf = ttf_lib.TTF_RenderGlyph_Shaded(
                self.__sdl_font, text, color.sdl_color[0], background.sdl_color[0])
        else:
            raise Exception('valid encodings are {}, not {}'.format('utf-8', 'ascii', 'unicode', 'glyph'))
        return sdl_surf

    def _render_solid(self, text, color, encoding):
        """
        SDL_Surface * TTF_RenderUTF8_Solid(TTF_Font *font, const char *text, SDL_Color fg);
        SDL_Surface * TTF_RenderText_Solid(TTF_Font *font, const char *text, SDL_Color fg);
        SDL_Surface * TTF_RenderUNICODE_Solid(TTF_Font *font, const Uint16 *text, SDL_Color fg);
        SDL_Surface * TTF_RenderGlyph_Solid(TTF_Font *font, Uint16 ch, SDL_Color fg);
        """
        if encoding == 'utf-8':
            sdl_surf = ttf_lib.TTF_RenderUTF8_Solid(self.__sdl_font, utf8(text), color.sdl_color[0])
        elif encoding == 'ascii':
            sdl_surf = ttf_lib.TTF_RenderText_Solid(self.__sdl_font, text, color.sdl_color[0])
        elif encoding == 'unicode':
            sdl_surf = ttf_lib.TTF_RenderUNICODE_Solid(self.__sdl_font, text, color.sdl_color[0])
        elif encoding == 'glyph':
            sdl_surf = ttf_lib.TTF_RenderGlyph_Solid(self.__sdl_font, text, color.sdl_color[0])
        else:
            raise Exception('valid encodings are {}, not {}'.format('utf-8', 'ascii', 'unicode', 'glyph'))
        return sdl_surf

    def _render_blended_wrapped(self, text, color, encoding, wrap_length):
        """
        SDL_Surface * TTF_RenderUTF8_Blended_Wrapped(TTF_Font *font, const char *text, SDL_Color fg, Uint32 wrapLength);
        SDL_Surface * TTF_RenderText_Blended_Wrapped(TTF_Font *font, const char *text, SDL_Color fg, Uint32 wrapLength);
        SDL_Surface * TTF_RenderUNICODE_Blended_Wrapped(TTF_Font *font, const Uint16 *text, SDL_Color fg, Uint32 wrapLength);
        """
        if encoding == 'utf-8':
            sdl_surf = ttf_lib.TTF_RenderUTF8_Blended_Wrapped(
                self.__sdl_font, utf8(text), color.sdl_color[0], wrap_length)
        elif encoding == 'ascii':
            sdl_surf = ttf_lib.TTF_RenderText_Blended_Wrapped(self.__sdl_font, text, color.sdl_color[0], wrap_length)
        elif encoding == 'unicode':
            sdl_surf = ttf_lib.TTF_RenderUNICODE_Blended_Wrapped(self.__sdl_font, text, color.sdl_color[0], wrap_length)
        elif encoding == 'glyph':
            sdl_surf = self._render_blended(text, color, encoding)
        else:
            raise Exception('valid encodings are {}, not {}'.format('utf-8', 'ascii', 'unicode', 'glyph'))
        return sdl_surf

    def _render_blended(self, text, color, encoding):
        """
        SDL_Surface * TTF_RenderUTF8_Blended(TTF_Font *font, const char *text, SDL_Color fg);
        SDL_Surface * TTF_RenderText_Blended(TTF_Font *font, const char *text, SDL_Color fg);
        SDL_Surface * TTF_RenderUNICODE_Blended(TTF_Font *font, const Uint16 *text, SDL_Color fg);
        SDL_Surface * TTF_RenderGlyph_Blended(TTF_Font *font, Uint16 ch, SDL_Color fg);
        """
        if encoding == 'utf-8':
            sdl_surf = ttf_lib.TTF_RenderUTF8_Blended(self.__sdl_font, utf8(text), color.sdl_color[0])
        elif encoding == 'ascii':
            sdl_surf = ttf_lib.TTF_RenderText_Blended(self.__sdl_font, text, color.sdl_color[0])
        elif encoding == 'unicode':
            sdl_surf = ttf_lib.TTF_RenderUNICODE_Blended(self.__sdl_font, text, color.sdl_color[0])
        elif encoding == 'glyph':
            sdl_surf = ttf_lib.TTF_RenderGlyph_Blended(self.__sdl_font, text, color.sdl_color[0])
        else:
            raise Exception('valid encodings are {}, not {}'.format('utf-8', 'ascii', 'unicode', 'glyph'))
        return sdl_surf

    def size(self, text, encoding='utf-8'):
        """
        TTF_SizeText(TTF_Font *font, const char *text, int *w, int *h)
        TTF_SizeUTF8(TTF_Font *font, const char *text, int *w, int *h)
        TTF_SizeUNICODE(TTF_Font *font, const Uint16 *text, int *w, int *h)
        """
        cdef_w = ttf_ffi.new('int *')
        cdef_h = ttf_ffi.new('int *')
        if encoding == 'utf-8':
            ttf_lib.TTF_SizeUTF8(self.__sdl_font, utf8(text), cdef_w, cdef_h)
        elif encoding == 'ascii':
            ttf_lib.TTF_SizeText(self.__sdl_font, text, cdef_w, cdef_h)
        elif encoding == 'unicode':
            ttf_lib.TTF_SizeUNICODE(self.__sdl_font, text, cdef_w, cdef_h)
        else:
            raise NotImplemented

        return cdef_w[0], cdef_h[0]

    def set_hinting(self, hinting):
        """
        TTF_HINTING_NORMAL = 0
        TTF_HINTING_LIGHT = 1
        TTF_HINTING_MONO = 2
        TTF_HINTING_NONE = 3
        """
        ttf_lib.TTF_SetFontHinting(self.__sdl_font, hinting)

    def get_hinting(self):
        return ttf_lib.TTF_GetFontHinting()

    def set_style(self, style):
        """
        TTF_STYLE_NORMAL        = 0x00
        TTF_STYLE_BOLD          = 0x01
        TTF_STYLE_ITALIC        = 0x02
        TTF_STYLE_UNDERLINE     = 0x04
        TTF_STYLE_STRIKETHROUGH = 0x08
        """
        ttf_lib.TTF_SetFontStyle(self.__sdl_font, style)

    def get_style(self):
        return ttf_lib.TTF_GetFontStyle(self.__sdl_font)

    def set_outline(self, boolean):
        """
        """
        # TODO: uses same color?
        ttf_lib.TTF_SetFontOutline(self.__sdl_font, boolean)

    def get_outline(self):
        return ttf_lib.TTF_GetFontOutline(self.__sdl_font) == 1

    def _mask_style_flags(self, boolean, mod_flags):
        flags = self.get_style()
        if boolean:
            flags |= mod_flags
        else:
            flags ^= mod_flags
        return flags

    def set_underline(self, boolean):
        self.set_style(self._mask_style_flags(boolean, TTF_STYLE_UNDERLINE))

    def get_underline(self):
        return self.get_style() & TTF_STYLE_UNDERLINE

    def set_bold(self, boolean):
        self.set_style(self._mask_style_flags(boolean, TTF_STYLE_BOLD))

    def get_bold(self):
        return self.get_style() & TTF_STYLE_BOLD

    def set_italic(self, boolean):
        self.set_style(self._mask_style_flags(boolean, TTF_STYLE_ITALIC))

    def get_italic(self):
        return self.get_style() & TTF_STYLE_ITALIC

    def set_strikethrough(self, boolean):
        self.set_style(self._mask_style_flags(boolean, TTF_STYLE_STRIKETHROUGH))

    def get_strikethrough(self):
        return self.get_style() & TTF_STYLE_STRIKETHROUGH

    def set_normal(self):
        self.set_style(TTF_STYLE_NORMAL)

    def get_normal(self):
        return self.get_style() == TTF_STYLE_NORMAL

    def get_linesize(self):
        return self.get_height() + self.get_ascent() + self.get_descent()

    def get_height(self):
        return ttf_lib.TTF_FontHeight(self.__sdl_font)

    def get_ascent(self):
        return ttf_lib.TTF_FontAscent(self.__sdl_font)

    def get_descent(self):
        return ttf_lib.TTF_FontDescent(self.__sdl_font)

    def get_line_skip(self):
        return ttf_lib.TTF_FontLineSkip(self.__sdl_font)

    def get_kerning(self):
        return ttf_lib.TTF_GetFontKerning()

    def set_kerning(self, allowed):
        ttf_lib.TTF_SetFontKerning(self.__sdl_font, allowed)

    def get_kerning_size(self, prev_index, index):
        """
        int TTF_GetFontKerningSize(TTF_Font *font, int prev_index, int index)
        """
        return ttf_lib.TTF_GetFontKerningSize(self.__sdl_font, prev_index, index)

    def get_faces(self):
        return ttf_lib.TTF_FontFaces(self.__sdl_font)

    def is_fixed_width(self):
        return ttf_lib.TTF_FontFaceIsFixedWidth(self.__sdl_font)

    def family_name(self):
        name = ttf_lib.TTF_FontFaceFamilyName(self.__sdl_font)
        return ttf_ffi.string(name).decode('utf-8')

    def style_name(self):
        name = ttf_lib.TTF_FontFaceStyleName(self.__sdl_font)
        return ttf_ffi.string(name).decode('utf-8')

    def glyph_is_provided(self, ch):
        """
        int TTF_GlyphIsProvided(const TTF_Font *font, Uint16 ch)
        """
        return ttf_lib.TTF_GlyphIsProvided(self.__sdl_font, ch)

    def metrics(self, ch):
        """get the metrics (dimensions) of a glyph

        To understand what these metrics mean, here is a useful link:
        http://freetype.sourceforge.net/freetype2/docs/tutorial/step2.html
        TTF_GlyphMetrics(TTF_Font *font, Uint16 ch, int *minx, int *maxx, int *miny, int *maxy, int *advance)

        ;return; tuple of int; minx, maxx, miny, maxy, advance
        """
        minx = sdl_ffi.new('int *')
        maxx = sdl_ffi.new('int *')
        miny = sdl_ffi.new('int *')
        maxy = sdl_ffi.new('int *')
        advance = sdl_ffi.new('int *')
        ttf_lib.TTF_GlyphMetrics(self.__sdl_font, ch, minx, maxx, miny, maxy, advance)
        return minx[0], max[0], miny[0], maxy[0], advance[0]

    def filename(self):
        return self.__filename

    def pointsize(self):
        return self.__pointsize

    def close(self):
        if self.__sdl_font:
            ttf_lib.TTF_CloseFont(self.__sdl_font)
            self.__sdl_font = None

    def __getsdlfont(self):
        return self.__sdl_font
    sdl_font = property(__getsdlfont)

    def __del__(self):
        self.close()

    def __str__(self):
        return '<{}({}, {}>'.format(self.__class__.__name__, self.__filename, self.__size)


def SysFont(object):

    def __init__(self, name, size, bold=False, italic=False):
        raise NotImplemented


from .surface import Surface
