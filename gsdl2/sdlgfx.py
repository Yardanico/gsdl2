#!/usr/bin/env python

import re

# unlike other ffi modules, this one depends on previously loaded sdl.ffi
from .basesdl import ffi


__all__ = ['ffi', 'parse_headers']


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

//
// SDL2_gfxPrimitives.h
//


#define M_PI	3.1415926535897932384626433832795
#define SDL2_GFXPRIMITIVES_MAJOR	1
#define SDL2_GFXPRIMITIVES_MINOR	0
#define SDL2_GFXPRIMITIVES_MICRO	1

// Note: all ___Color routines expect the color to be in format 0xRRGGBBAA

// Pixel
int pixelColor(SDL_Renderer * renderer, Sint16 x, Sint16 y, Uint32 color);
int pixelRGBA(SDL_Renderer * renderer, Sint16 x, Sint16 y, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Horizontal line
int hlineColor(SDL_Renderer * renderer, Sint16 x1, Sint16 x2, Sint16 y, Uint32 color);
int hlineRGBA(SDL_Renderer * renderer, Sint16 x1, Sint16 x2, Sint16 y, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Vertical line
int vlineColor(SDL_Renderer * renderer, Sint16 x, Sint16 y1, Sint16 y2, Uint32 color);
int vlineRGBA(SDL_Renderer * renderer, Sint16 x, Sint16 y1, Sint16 y2, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Rectangle
int rectangleColor(SDL_Renderer * renderer, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Uint32 color);
int rectangleRGBA(SDL_Renderer * renderer, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Rounded-Corner Rectangle
int roundedRectangleColor(SDL_Renderer * renderer, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Sint16 rad, Uint32 color);
int roundedRectangleRGBA(SDL_Renderer * renderer, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Sint16 rad, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Filled rectangle (Box)
int boxColor(SDL_Renderer * renderer, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Uint32 color);
int boxRGBA(SDL_Renderer * renderer, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Rounded-Corner Filled rectangle (Box)
int roundedBoxColor(SDL_Renderer * renderer, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Sint16 rad, Uint32 color);
int roundedBoxRGBA(SDL_Renderer * renderer, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Sint16 rad, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Line
int lineColor(SDL_Renderer * renderer, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Uint32 color);
int lineRGBA(SDL_Renderer * renderer, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// AA Line
int aalineColor(SDL_Renderer * renderer, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Uint32 color);
int aalineRGBA(SDL_Renderer * renderer, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Thick Line
int thickLineColor(SDL_Renderer * renderer, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Uint8 width, Uint32 color);
int thickLineRGBA(SDL_Renderer * renderer, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Uint8 width, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Circle
int circleColor(SDL_Renderer * renderer, Sint16 x, Sint16 y, Sint16 rad, Uint32 color);
int circleRGBA(SDL_Renderer * renderer, Sint16 x, Sint16 y, Sint16 rad, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Arc
int arcColor(SDL_Renderer * renderer, Sint16 x, Sint16 y, Sint16 rad, Sint16 start, Sint16 end, Uint32 color);
int arcRGBA(SDL_Renderer * renderer, Sint16 x, Sint16 y, Sint16 rad, Sint16 start, Sint16 end, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// AA Circle
int aacircleColor(SDL_Renderer * renderer, Sint16 x, Sint16 y, Sint16 rad, Uint32 color);
int aacircleRGBA(SDL_Renderer * renderer, Sint16 x, Sint16 y, Sint16 rad, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Filled Circle
int filledCircleColor(SDL_Renderer * renderer, Sint16 x, Sint16 y, Sint16 r, Uint32 color);
int filledCircleRGBA(SDL_Renderer * renderer, Sint16 x, Sint16 y, Sint16 rad, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Ellipse
int ellipseColor(SDL_Renderer * renderer, Sint16 x, Sint16 y, Sint16 rx, Sint16 ry, Uint32 color);
int ellipseRGBA(SDL_Renderer * renderer, Sint16 x, Sint16 y, Sint16 rx, Sint16 ry, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// AA Ellipse
int aaellipseColor(SDL_Renderer * renderer, Sint16 x, Sint16 y, Sint16 rx, Sint16 ry, Uint32 color);
int aaellipseRGBA(SDL_Renderer * renderer, Sint16 x, Sint16 y, Sint16 rx, Sint16 ry, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Filled Ellipse
int filledEllipseColor(SDL_Renderer * renderer, Sint16 x, Sint16 y, Sint16 rx, Sint16 ry, Uint32 color);
int filledEllipseRGBA(SDL_Renderer * renderer, Sint16 x, Sint16 y, Sint16 rx, Sint16 ry, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Pie
int pieColor(SDL_Renderer * renderer, Sint16 x, Sint16 y, Sint16 rad, Sint16 start, Sint16 end, Uint32 color);
int pieRGBA(SDL_Renderer * renderer, Sint16 x, Sint16 y, Sint16 rad, Sint16 start, Sint16 end, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Filled Pie
int filledPieColor(SDL_Renderer * renderer, Sint16 x, Sint16 y, Sint16 rad, Sint16 start, Sint16 end, Uint32 color);
int filledPieRGBA(SDL_Renderer * renderer, Sint16 x, Sint16 y, Sint16 rad, Sint16 start, Sint16 end, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Trigon
int trigonColor(SDL_Renderer * renderer, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Sint16 x3, Sint16 y3, Uint32 color);
int trigonRGBA(SDL_Renderer * renderer, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Sint16 x3, Sint16 y3, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// AA-Trigon
int aatrigonColor(SDL_Renderer * renderer, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Sint16 x3, Sint16 y3, Uint32 color);
int aatrigonRGBA(SDL_Renderer * renderer,  Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Sint16 x3, Sint16 y3, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Filled Trigon
int filledTrigonColor(SDL_Renderer * renderer, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Sint16 x3, Sint16 y3, Uint32 color);
int filledTrigonRGBA(SDL_Renderer * renderer, Sint16 x1, Sint16 y1, Sint16 x2, Sint16 y2, Sint16 x3, Sint16 y3, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Polygon
int polygonColor(SDL_Renderer * renderer, const Sint16 * vx, const Sint16 * vy, int n, Uint32 color);
int polygonRGBA(SDL_Renderer * renderer, const Sint16 * vx, const Sint16 * vy, int n, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// AA-Polygon
int aapolygonColor(SDL_Renderer * renderer, const Sint16 * vx, const Sint16 * vy, int n, Uint32 color);
int aapolygonRGBA(SDL_Renderer * renderer, const Sint16 * vx, const Sint16 * vy, int n, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Filled Polygon
int filledPolygonColor(SDL_Renderer * renderer, const Sint16 * vx, const Sint16 * vy, int n, Uint32 color);
int filledPolygonRGBA(SDL_Renderer * renderer, const Sint16 * vx, const Sint16 * vy, int n, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Textured Polygon
int texturedPolygon(SDL_Renderer * renderer, const Sint16 * vx, const Sint16 * vy, int n, SDL_Surface * texture,int texture_dx,int texture_dy);

// Bezier
int bezierColor(SDL_Renderer * renderer, const Sint16 * vx, const Sint16 * vy, int n, int s, Uint32 color);
int bezierRGBA(SDL_Renderer * renderer, const Sint16 * vx, const Sint16 * vy, int n, int s, Uint8 r, Uint8 g, Uint8 b, Uint8 a);

// Characters/Strings
void gfxPrimitivesSetFont(const void *fontdata, Uint32 cw, Uint32 ch);
void gfxPrimitivesSetFontRotation(Uint32 rotation);
int characterColor(SDL_Renderer * renderer, Sint16 x, Sint16 y, char c, Uint32 color);
int characterRGBA(SDL_Renderer * renderer, Sint16 x, Sint16 y, char c, Uint8 r, Uint8 g, Uint8 b, Uint8 a);
int stringColor(SDL_Renderer * renderer, Sint16 x, Sint16 y, const char *s, Uint32 color);
int stringRGBA(SDL_Renderer * renderer, Sint16 x, Sint16 y, const char *s, Uint8 r, Uint8 g, Uint8 b, Uint8 a);


//
// SDL2_imageFilter.h
//


// Comments:
//  1.) MMX functions work best if all data blocks are aligned on a 32 bytes boundary.
//  2.) Data that is not within an 8 byte boundary is processed using the C routine.
//  3.) Convolution routines do not have C routines at this time.

// Detect MMX capability in CPU
int SDL_imageFilterMMXdetect(void);

// Force use of MMX off (or turn possible use back on)
void SDL_imageFilterMMXoff(void);
void SDL_imageFilterMMXon(void);

// All routines return:
//   0   OK
//  -1   Error (internal error, parameter error)

//  SDL_imageFilterAdd: D = saturation255(S1 + S2)
int SDL_imageFilterAdd(unsigned char *Src1, unsigned char *Src2, unsigned char *Dest, unsigned int length);

//  SDL_imageFilterMean: D = S1/2 + S2/2
int SDL_imageFilterMean(unsigned char *Src1, unsigned char *Src2, unsigned char *Dest, unsigned int length);

//  SDL_imageFilterSub: D = saturation0(S1 - S2)
int SDL_imageFilterSub(unsigned char *Src1, unsigned char *Src2, unsigned char *Dest, unsigned int length);

//  SDL_imageFilterAbsDiff: D = | S1 - S2 |
int SDL_imageFilterAbsDiff(unsigned char *Src1, unsigned char *Src2, unsigned char *Dest, unsigned int length);

//  SDL_imageFilterMult: D = saturation(S1 * S2)
int SDL_imageFilterMult(unsigned char *Src1, unsigned char *Src2, unsigned char *Dest, unsigned int length);

//  SDL_imageFilterMultNor: D = S1 * S2   (non-MMX)
int SDL_imageFilterMultNor(unsigned char *Src1, unsigned char *Src2, unsigned char *Dest, unsigned int length);

//  SDL_imageFilterMultDivby2: D = saturation255(S1/2 * S2)
int SDL_imageFilterMultDivby2(unsigned char *Src1, unsigned char *Src2, unsigned char *Dest, unsigned int length);

//  SDL_imageFilterMultDivby4: D = saturation255(S1/2 * S2/2)
int SDL_imageFilterMultDivby4(unsigned char *Src1, unsigned char *Src2, unsigned char *Dest, unsigned int length);

//  SDL_imageFilterBitAnd: D = S1 & S2
int SDL_imageFilterBitAnd(unsigned char *Src1, unsigned char *Src2, unsigned char *Dest, unsigned int length);

//  SDL_imageFilterBitOr: D = S1 | S2
int SDL_imageFilterBitOr(unsigned char *Src1, unsigned char *Src2, unsigned char *Dest, unsigned int length);

//  SDL_imageFilterDiv: D = S1 / S2   (non-MMX)
int SDL_imageFilterDiv(unsigned char *Src1, unsigned char *Src2, unsigned char *Dest, unsigned int length);

//  SDL_imageFilterBitNegation: D = !S
int SDL_imageFilterBitNegation(unsigned char *Src1, unsigned char *Dest, unsigned int length);

//  SDL_imageFilterAddByte: D = saturation255(S + C)
int SDL_imageFilterAddByte(unsigned char *Src1, unsigned char *Dest, unsigned int length, unsigned char C);

//  SDL_imageFilterAddUint: D = saturation255(S + (uint)C)
int SDL_imageFilterAddUint(unsigned char *Src1, unsigned char *Dest, unsigned int length, unsigned int C);

//  SDL_imageFilterAddByteToHalf: D = saturation255(S/2 + C)
int SDL_imageFilterAddByteToHalf(unsigned char *Src1, unsigned char *Dest, unsigned int length, unsigned char C);

//  SDL_imageFilterSubByte: D = saturation0(S - C)
int SDL_imageFilterSubByte(unsigned char *Src1, unsigned char *Dest, unsigned int length, unsigned char C);

//  SDL_imageFilterSubUint: D = saturation0(S - (uint)C)
int SDL_imageFilterSubUint(unsigned char *Src1, unsigned char *Dest, unsigned int length, unsigned int C);

//  SDL_imageFilterShiftRight: D = saturation0(S >> N)
int SDL_imageFilterShiftRight(unsigned char *Src1, unsigned char *Dest, unsigned int length, unsigned char N);

//  SDL_imageFilterShiftRightUint: D = saturation0((uint)S >> N)
int SDL_imageFilterShiftRightUint(unsigned char *Src1, unsigned char *Dest, unsigned int length, unsigned char N);

//  SDL_imageFilterMultByByte: D = saturation255(S * C)
int SDL_imageFilterMultByByte(unsigned char *Src1, unsigned char *Dest, unsigned int length, unsigned char C);

//  SDL_imageFilterShiftRightAndMultByByte: D = saturation255((S >> N) * C)
int SDL_imageFilterShiftRightAndMultByByte(unsigned char *Src1, unsigned char *Dest, unsigned int length, unsigned char N, unsigned char C);

//  SDL_imageFilterShiftLeftByte: D = (S << N)
int SDL_imageFilterShiftLeftByte(unsigned char *Src1, unsigned char *Dest, unsigned int length, unsigned char N);

//  SDL_imageFilterShiftLeftUint: D = ((uint)S << N)
int SDL_imageFilterShiftLeftUint(unsigned char *Src1, unsigned char *Dest, unsigned int length, unsigned char N);

//  SDL_imageFilterShiftLeft: D = saturation255(S << N)
int SDL_imageFilterShiftLeft(unsigned char *Src1, unsigned char *Dest, unsigned int length, unsigned char N);

//  SDL_imageFilterBinarizeUsingThreshold: D = S >= T ? 255:0
int SDL_imageFilterBinarizeUsingThreshold(unsigned char *Src1, unsigned char *Dest, unsigned int length, unsigned char T);

//  SDL_imageFilterClipToRange: D = (S >= Tmin) & (S <= Tmax) 255:0
int SDL_imageFilterClipToRange(unsigned char *Src1, unsigned char *Dest, unsigned int length, unsigned char Tmin, unsigned char Tmax);

//  SDL_imageFilterNormalizeLinear: D = saturation255((Nmax - Nmin)/(Cmax - Cmin)*(S - Cmin) + Nmin)
int SDL_imageFilterNormalizeLinear(unsigned char *Src, unsigned char *Dest, unsigned int length, int Cmin, int Cmax, int Nmin, int Nmax);


//
// SDL2_rotozoom.h
//


// Disable anti-aliasing (no smoothing).
#define SMOOTHING_OFF		0

// Enable anti-aliasing (smoothing).
#define SMOOTHING_ON		1

// Rotozoom functions
SDL_Surface *rotozoomSurface(SDL_Surface * src, double angle, double zoom, int smooth);
SDL_Surface *rotozoomSurfaceXY(SDL_Surface * src, double angle, double zoomx, double zoomy, int smooth);
void rotozoomSurfaceSize(int width, int height, double angle, double zoom, int *dstwidth, int *dstheight);
void rotozoomSurfaceSizeXY(int width, int height, double angle, double zoomx, double zoomy, int *dstwidth, int *dstheight);

// Zooming functions
SDL_Surface *zoomSurface(SDL_Surface * src, double zoomx, double zoomy, int smooth);
void zoomSurfaceSize(int width, int height, double zoomx, double zoomy, int *dstwidth, int *dstheight);

// Shrinking functions
SDL_Surface *shrinkSurface(SDL_Surface * src, int factorx, int factory);

// Specialized rotation functions
SDL_Surface* rotateSurface90Degrees(SDL_Surface* src, int numClockwiseTurns);


//
// SDL2_gfxPrimitives_font.h
//


#define GFX_FONTDATAMAX (8*256)

//static unsigned char gfxPrimitivesFontdata[GFX_FONTDATAMAX] = {
static unsigned char gfxPrimitivesFontdata[2048] = {

    // 0 0x00 '^@'
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 1 0x01 '^A'
    0x7e,         // 01111110
    0x81,         // 10000001
    0xa5,         // 10100101
    0x81,         // 10000001
    0xbd,         // 10111101
    0x99,         // 10011001
    0x81,         // 10000001
    0x7e,         // 01111110
    // 2 0x02 '^B'
    0x7e,         // 01111110
    0xff,         // 11111111
    0xdb,         // 11011011
    0xff,         // 11111111
    0xc3,         // 11000011
    0xe7,         // 11100111
    0xff,         // 11111111
    0x7e,         // 01111110
    // 3 0x03 '^C'
    0x6c,         // 01101100
    0xfe,         // 11111110
    0xfe,         // 11111110
    0xfe,         // 11111110
    0x7c,         // 01111100
    0x38,         // 00111000
    0x10,         // 00010000
    0x00,         // 00000000
    // 4 0x04 '^D'
    0x10,         // 00010000
    0x38,         // 00111000
    0x7c,         // 01111100
    0xfe,         // 11111110
    0x7c,         // 01111100
    0x38,         // 00111000
    0x10,         // 00010000
    0x00,         // 00000000
    // 5 0x05 '^E'
    0x38,         // 00111000
    0x7c,         // 01111100
    0x38,         // 00111000
    0xfe,         // 11111110
    0xfe,         // 11111110
    0xd6,         // 11010110
    0x10,         // 00010000
    0x38,         // 00111000
    // 6 0x06 '^F'
    0x10,         // 00010000
    0x38,         // 00111000
    0x7c,         // 01111100
    0xfe,         // 11111110
    0xfe,         // 11111110
    0x7c,         // 01111100
    0x10,         // 00010000
    0x38,         // 00111000
    // 7 0x07 '^G'
    0x00,         // 00000000
    0x00,         // 00000000
    0x18,         // 00011000
    0x3c,         // 00111100
    0x3c,         // 00111100
    0x18,         // 00011000
    0x00,         // 00000000
    0x00,         // 00000000
    // 8 0x08 '^H'
    0xff,         // 11111111
    0xff,         // 11111111
    0xe7,         // 11100111
    0xc3,         // 11000011
    0xc3,         // 11000011
    0xe7,         // 11100111
    0xff,         // 11111111
    0xff,         // 11111111
    // 9 0x09 '   '
    0x00,         // 00000000
    0x3c,         // 00111100
    0x66,         // 01100110
    0x42,         // 01000010
    0x42,         // 01000010
    0x66,         // 01100110
    0x3c,         // 00111100
    0x00,         // 00000000
    // 10 0x0a '^J'
    0xff,         // 11111111
    0xc3,         // 11000011
    0x99,         // 10011001
    0xbd,         // 10111101
    0xbd,         // 10111101
    0x99,         // 10011001
    0xc3,         // 11000011
    0xff,         // 11111111
    // 11 0x0b '^K'
    0x0f,         // 00001111
    0x07,         // 00000111
    0x0f,         // 00001111
    0x7d,         // 01111101
    0xcc,         // 11001100
    0xcc,         // 11001100
    0xcc,         // 11001100
    0x78,         // 01111000
    // 12 0x0c '^L'
    0x3c,         // 00111100
    0x66,         // 01100110
    0x66,         // 01100110
    0x66,         // 01100110
    0x3c,         // 00111100
    0x18,         // 00011000
    0x7e,         // 01111110
    0x18,         // 00011000
    // 13 0x0d '^M'
    0x3f,         // 00111111
    0x33,         // 00110011
    0x3f,         // 00111111
    0x30,         // 00110000
    0x30,         // 00110000
    0x70,         // 01110000
    0xf0,         // 11110000
    0xe0,         // 11100000
    // 14 0x0e '^N'
    0x7f,         // 01111111
    0x63,         // 01100011
    0x7f,         // 01111111
    0x63,         // 01100011
    0x63,         // 01100011
    0x67,         // 01100111
    0xe6,         // 11100110
    0xc0,         // 11000000
    // 15 0x0f '^O'
    0x18,         // 00011000
    0xdb,         // 11011011
    0x3c,         // 00111100
    0xe7,         // 11100111
    0xe7,         // 11100111
    0x3c,         // 00111100
    0xdb,         // 11011011
    0x18,         // 00011000
    // 16 0x10 '^P'
    0x80,         // 10000000
    0xe0,         // 11100000
    0xf8,         // 11111000
    0xfe,         // 11111110
    0xf8,         // 11111000
    0xe0,         // 11100000
    0x80,         // 10000000
    0x00,         // 00000000
    // 17 0x11 '^Q'
    0x02,         // 00000010
    0x0e,         // 00001110
    0x3e,         // 00111110
    0xfe,         // 11111110
    0x3e,         // 00111110
    0x0e,         // 00001110
    0x02,         // 00000010
    0x00,         // 00000000
    // 18 0x12 '^R'
    0x18,         // 00011000
    0x3c,         // 00111100
    0x7e,         // 01111110
    0x18,         // 00011000
    0x18,         // 00011000
    0x7e,         // 01111110
    0x3c,         // 00111100
    0x18,         // 00011000
    // 19 0x13 '^S'
    0x66,         // 01100110
    0x66,         // 01100110
    0x66,         // 01100110
    0x66,         // 01100110
    0x66,         // 01100110
    0x00,         // 00000000
    0x66,         // 01100110
    0x00,         // 00000000
    // 20 0x14 '^T'
    0x7f,         // 01111111
    0xdb,         // 11011011
    0xdb,         // 11011011
    0x7b,         // 01111011
    0x1b,         // 00011011
    0x1b,         // 00011011
    0x1b,         // 00011011
    0x00,         // 00000000
    // 21 0x15 '^U'
    0x3e,         // 00111110
    0x61,         // 01100001
    0x3c,         // 00111100
    0x66,         // 01100110
    0x66,         // 01100110
    0x3c,         // 00111100
    0x86,         // 10000110
    0x7c,         // 01111100
    // 22 0x16 '^V'
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x7e,         // 01111110
    0x7e,         // 01111110
    0x7e,         // 01111110
    0x00,         // 00000000
    // 23 0x17 '^W'
    0x18,         // 00011000
    0x3c,         // 00111100
    0x7e,         // 01111110
    0x18,         // 00011000
    0x7e,         // 01111110
    0x3c,         // 00111100
    0x18,         // 00011000
    0xff,         // 11111111
    // 24 0x18 '^X'
    0x18,         // 00011000
    0x3c,         // 00111100
    0x7e,         // 01111110
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x00,         // 00000000
    // 25 0x19 '^Y'
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x7e,         // 01111110
    0x3c,         // 00111100
    0x18,         // 00011000
    0x00,         // 00000000
    // 26 0x1a '^Z'
    0x00,         // 00000000
    0x18,         // 00011000
    0x0c,         // 00001100
    0xfe,         // 11111110
    0x0c,         // 00001100
    0x18,         // 00011000
    0x00,         // 00000000
    0x00,         // 00000000
    // 27 0x1b '^['
    0x00,         // 00000000
    0x30,         // 00110000
    0x60,         // 01100000
    0xfe,         // 11111110
    0x60,         // 01100000
    0x30,         // 00110000
    0x00,         // 00000000
    0x00,         // 00000000
    // 28 0x1c '^\'
    0x00,         // 00000000
    0x00,         // 00000000
    0xc0,         // 11000000
    0xc0,         // 11000000
    0xc0,         // 11000000
    0xfe,         // 11111110
    0x00,         // 00000000
    0x00,         // 00000000
    // 29 0x1d '^]'
    0x00,         // 00000000
    0x24,         // 00100100
    0x66,         // 01100110
    0xff,         // 11111111
    0x66,         // 01100110
    0x24,         // 00100100
    0x00,         // 00000000
    0x00,         // 00000000
    // 30 0x1e '^^'
    0x00,         // 00000000
    0x18,         // 00011000
    0x3c,         // 00111100
    0x7e,         // 01111110
    0xff,         // 11111111
    0xff,         // 11111111
    0x00,         // 00000000
    0x00,         // 00000000
    // 31 0x1f '^_'
    0x00,         // 00000000
    0xff,         // 11111111
    0xff,         // 11111111
    0x7e,         // 01111110
    0x3c,         // 00111100
    0x18,         // 00011000
    0x00,         // 00000000
    0x00,         // 00000000
    // 32 0x20 ' '
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 33 0x21 '!'
    0x18,         // 00011000
    0x3c,         // 00111100
    0x3c,         // 00111100
    0x18,         // 00011000
    0x18,         // 00011000
    0x00,         // 00000000
    0x18,         // 00011000
    0x00,         // 00000000
    // 34 0x22 '"'
    0x66,         // 01100110
    0x66,         // 01100110
    0x24,         // 00100100
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 35 0x23 '#'
    0x6c,         // 01101100
    0x6c,         // 01101100
    0xfe,         // 11111110
    0x6c,         // 01101100
    0xfe,         // 11111110
    0x6c,         // 01101100
    0x6c,         // 01101100
    0x00,         // 00000000
    // 36 0x24 '$'
    0x18,         // 00011000
    0x3e,         // 00111110
    0x60,         // 01100000
    0x3c,         // 00111100
    0x06,         // 00000110
    0x7c,         // 01111100
    0x18,         // 00011000
    0x00,         // 00000000
    // 37 0x25 '%'
    0x00,         // 00000000
    0xc6,         // 11000110
    0xcc,         // 11001100
    0x18,         // 00011000
    0x30,         // 00110000
    0x66,         // 01100110
    0xc6,         // 11000110
    0x00,         // 00000000
    // 38 0x26 '&'
    0x38,         // 00111000
    0x6c,         // 01101100
    0x38,         // 00111000
    0x76,         // 01110110
    0xdc,         // 11011100
    0xcc,         // 11001100
    0x76,         // 01110110
    0x00,         // 00000000
    // 39 0x27 '''
    0x18,         // 00011000
    0x18,         // 00011000
    0x30,         // 00110000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 40 0x28 '('
    0x0c,         // 00001100
    0x18,         // 00011000
    0x30,         // 00110000
    0x30,         // 00110000
    0x30,         // 00110000
    0x18,         // 00011000
    0x0c,         // 00001100
    0x00,         // 00000000
    // 41 0x29 ')'
    0x30,         // 00110000
    0x18,         // 00011000
    0x0c,         // 00001100
    0x0c,         // 00001100
    0x0c,         // 00001100
    0x18,         // 00011000
    0x30,         // 00110000
    0x00,         // 00000000
    // 42 0x2a '*'
    0x00,         // 00000000
    0x66,         // 01100110
    0x3c,         // 00111100
    0xff,         // 11111111
    0x3c,         // 00111100
    0x66,         // 01100110
    0x00,         // 00000000
    0x00,         // 00000000
    // 43 0x2b '+'
    0x00,         // 00000000
    0x18,         // 00011000
    0x18,         // 00011000
    0x7e,         // 01111110
    0x18,         // 00011000
    0x18,         // 00011000
    0x00,         // 00000000
    0x00,         // 00000000
    // 44 0x2c ','
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x18,         // 00011000
    0x18,         // 00011000
    0x30,         // 00110000
    // 45 0x2d '-'
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x7e,         // 01111110
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 46 0x2e '.'
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x18,         // 00011000
    0x18,         // 00011000
    0x00,         // 00000000
    // 47 0x2f '/'
    0x06,         // 00000110
    0x0c,         // 00001100
    0x18,         // 00011000
    0x30,         // 00110000
    0x60,         // 01100000
    0xc0,         // 11000000
    0x80,         // 10000000
    0x00,         // 00000000
    // 48 0x30 '0'
    0x38,         // 00111000
    0x6c,         // 01101100
    0xc6,         // 11000110
    0xd6,         // 11010110
    0xc6,         // 11000110
    0x6c,         // 01101100
    0x38,         // 00111000
    0x00,         // 00000000
    // 49 0x31 '1'
    0x18,         // 00011000
    0x38,         // 00111000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x7e,         // 01111110
    0x00,         // 00000000
    // 50 0x32 '2'
    0x7c,         // 01111100
    0xc6,         // 11000110
    0x06,         // 00000110
    0x1c,         // 00011100
    0x30,         // 00110000
    0x66,         // 01100110
    0xfe,         // 11111110
    0x00,         // 00000000
    // 51 0x33 '3'
    0x7c,         // 01111100
    0xc6,         // 11000110
    0x06,         // 00000110
    0x3c,         // 00111100
    0x06,         // 00000110
    0xc6,         // 11000110
    0x7c,         // 01111100
    0x00,         // 00000000
    // 52 0x34 '4'
    0x1c,         // 00011100
    0x3c,         // 00111100
    0x6c,         // 01101100
    0xcc,         // 11001100
    0xfe,         // 11111110
    0x0c,         // 00001100
    0x1e,         // 00011110
    0x00,         // 00000000
    // 53 0x35 '5'
    0xfe,         // 11111110
    0xc0,         // 11000000
    0xc0,         // 11000000
    0xfc,         // 11111100
    0x06,         // 00000110
    0xc6,         // 11000110
    0x7c,         // 01111100
    0x00,         // 00000000
    // 54 0x36 '6'
    0x38,         // 00111000
    0x60,         // 01100000
    0xc0,         // 11000000
    0xfc,         // 11111100
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x7c,         // 01111100
    0x00,         // 00000000
    // 55 0x37 '7'
    0xfe,         // 11111110
    0xc6,         // 11000110
    0x0c,         // 00001100
    0x18,         // 00011000
    0x30,         // 00110000
    0x30,         // 00110000
    0x30,         // 00110000
    0x00,         // 00000000
    // 56 0x38 '8'
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x7c,         // 01111100
    0x00,         // 00000000
    // 57 0x39 '9'
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x7e,         // 01111110
    0x06,         // 00000110
    0x0c,         // 00001100
    0x78,         // 01111000
    0x00,         // 00000000
    // 58 0x3a ':'
    0x00,         // 00000000
    0x18,         // 00011000
    0x18,         // 00011000
    0x00,         // 00000000
    0x00,         // 00000000
    0x18,         // 00011000
    0x18,         // 00011000
    0x00,         // 00000000
    // 59 0x3b ';'
    0x00,         // 00000000
    0x18,         // 00011000
    0x18,         // 00011000
    0x00,         // 00000000
    0x00,         // 00000000
    0x18,         // 00011000
    0x18,         // 00011000
    0x30,         // 00110000
    // 60 0x3c '<'
    0x06,         // 00000110
    0x0c,         // 00001100
    0x18,         // 00011000
    0x30,         // 00110000
    0x18,         // 00011000
    0x0c,         // 00001100
    0x06,         // 00000110
    0x00,         // 00000000
    // 61 0x3d '='
    0x00,         // 00000000
    0x00,         // 00000000
    0x7e,         // 01111110
    0x00,         // 00000000
    0x00,         // 00000000
    0x7e,         // 01111110
    0x00,         // 00000000
    0x00,         // 00000000
    // 62 0x3e '>'
    0x60,         // 01100000
    0x30,         // 00110000
    0x18,         // 00011000
    0x0c,         // 00001100
    0x18,         // 00011000
    0x30,         // 00110000
    0x60,         // 01100000
    0x00,         // 00000000
    // 63 0x3f '?'
    0x7c,         // 01111100
    0xc6,         // 11000110
    0x0c,         // 00001100
    0x18,         // 00011000
    0x18,         // 00011000
    0x00,         // 00000000
    0x18,         // 00011000
    0x00,         // 00000000
    // 64 0x40 '@'
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xde,         // 11011110
    0xde,         // 11011110
    0xde,         // 11011110
    0xc0,         // 11000000
    0x78,         // 01111000
    0x00,         // 00000000
    // 65 0x41 'A'
    0x38,         // 00111000
    0x6c,         // 01101100
    0xc6,         // 11000110
    0xfe,         // 11111110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x00,         // 00000000
    // 66 0x42 'B'
    0xfc,         // 11111100
    0x66,         // 01100110
    0x66,         // 01100110
    0x7c,         // 01111100
    0x66,         // 01100110
    0x66,         // 01100110
    0xfc,         // 11111100
    0x00,         // 00000000
    // 67 0x43 'C'
    0x3c,         // 00111100
    0x66,         // 01100110
    0xc0,         // 11000000
    0xc0,         // 11000000
    0xc0,         // 11000000
    0x66,         // 01100110
    0x3c,         // 00111100
    0x00,         // 00000000
    // 68 0x44 'D'
    0xf8,         // 11111000
    0x6c,         // 01101100
    0x66,         // 01100110
    0x66,         // 01100110
    0x66,         // 01100110
    0x6c,         // 01101100
    0xf8,         // 11111000
    0x00,         // 00000000
    // 69 0x45 'E'
    0xfe,         // 11111110
    0x62,         // 01100010
    0x68,         // 01101000
    0x78,         // 01111000
    0x68,         // 01101000
    0x62,         // 01100010
    0xfe,         // 11111110
    0x00,         // 00000000
    // 70 0x46 'F'
    0xfe,         // 11111110
    0x62,         // 01100010
    0x68,         // 01101000
    0x78,         // 01111000
    0x68,         // 01101000
    0x60,         // 01100000
    0xf0,         // 11110000
    0x00,         // 00000000
    // 71 0x47 'G'
    0x3c,         // 00111100
    0x66,         // 01100110
    0xc0,         // 11000000
    0xc0,         // 11000000
    0xce,         // 11001110
    0x66,         // 01100110
    0x3a,         // 00111010
    0x00,         // 00000000
    // 72 0x48 'H'
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xfe,         // 11111110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x00,         // 00000000
    // 73 0x49 'I'
    0x3c,         // 00111100
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x3c,         // 00111100
    0x00,         // 00000000
    // 74 0x4a 'J'
    0x1e,         // 00011110
    0x0c,         // 00001100
    0x0c,         // 00001100
    0x0c,         // 00001100
    0xcc,         // 11001100
    0xcc,         // 11001100
    0x78,         // 01111000
    0x00,         // 00000000
    // 75 0x4b 'K'
    0xe6,         // 11100110
    0x66,         // 01100110
    0x6c,         // 01101100
    0x78,         // 01111000
    0x6c,         // 01101100
    0x66,         // 01100110
    0xe6,         // 11100110
    0x00,         // 00000000
    // 76 0x4c 'L'
    0xf0,         // 11110000
    0x60,         // 01100000
    0x60,         // 01100000
    0x60,         // 01100000
    0x62,         // 01100010
    0x66,         // 01100110
    0xfe,         // 11111110
    0x00,         // 00000000
    // 77 0x4d 'M'
    0xc6,         // 11000110
    0xee,         // 11101110
    0xfe,         // 11111110
    0xfe,         // 11111110
    0xd6,         // 11010110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x00,         // 00000000
    // 78 0x4e 'N'
    0xc6,         // 11000110
    0xe6,         // 11100110
    0xf6,         // 11110110
    0xde,         // 11011110
    0xce,         // 11001110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x00,         // 00000000
    // 79 0x4f 'O'
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x7c,         // 01111100
    0x00,         // 00000000
    // 80 0x50 'P'
    0xfc,         // 11111100
    0x66,         // 01100110
    0x66,         // 01100110
    0x7c,         // 01111100
    0x60,         // 01100000
    0x60,         // 01100000
    0xf0,         // 11110000
    0x00,         // 00000000
    // 81 0x51 'Q'
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xce,         // 11001110
    0x7c,         // 01111100
    0x0e,         // 00001110
    // 82 0x52 'R'
    0xfc,         // 11111100
    0x66,         // 01100110
    0x66,         // 01100110
    0x7c,         // 01111100
    0x6c,         // 01101100
    0x66,         // 01100110
    0xe6,         // 11100110
    0x00,         // 00000000
    // 83 0x53 'S'
    0x3c,         // 00111100
    0x66,         // 01100110
    0x30,         // 00110000
    0x18,         // 00011000
    0x0c,         // 00001100
    0x66,         // 01100110
    0x3c,         // 00111100
    0x00,         // 00000000
    // 84 0x54 'T'
    0x7e,         // 01111110
    0x7e,         // 01111110
    0x5a,         // 01011010
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x3c,         // 00111100
    0x00,         // 00000000
    // 85 0x55 'U'
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x7c,         // 01111100
    0x00,         // 00000000
    // 86 0x56 'V'
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x6c,         // 01101100
    0x38,         // 00111000
    0x00,         // 00000000
    // 87 0x57 'W'
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xd6,         // 11010110
    0xd6,         // 11010110
    0xfe,         // 11111110
    0x6c,         // 01101100
    0x00,         // 00000000
    // 88 0x58 'X'
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x6c,         // 01101100
    0x38,         // 00111000
    0x6c,         // 01101100
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x00,         // 00000000
    // 89 0x59 'Y'
    0x66,         // 01100110
    0x66,         // 01100110
    0x66,         // 01100110
    0x3c,         // 00111100
    0x18,         // 00011000
    0x18,         // 00011000
    0x3c,         // 00111100
    0x00,         // 00000000
    // 90 0x5a 'Z'
    0xfe,         // 11111110
    0xc6,         // 11000110
    0x8c,         // 10001100
    0x18,         // 00011000
    0x32,         // 00110010
    0x66,         // 01100110
    0xfe,         // 11111110
    0x00,         // 00000000
    // 91 0x5b '['
    0x3c,         // 00111100
    0x30,         // 00110000
    0x30,         // 00110000
    0x30,         // 00110000
    0x30,         // 00110000
    0x30,         // 00110000
    0x3c,         // 00111100
    0x00,         // 00000000
    // 92 0x5c '\'
    0xc0,         // 11000000
    0x60,         // 01100000
    0x30,         // 00110000
    0x18,         // 00011000
    0x0c,         // 00001100
    0x06,         // 00000110
    0x02,         // 00000010
    0x00,         // 00000000
    // 93 0x5d ']'
    0x3c,         // 00111100
    0x0c,         // 00001100
    0x0c,         // 00001100
    0x0c,         // 00001100
    0x0c,         // 00001100
    0x0c,         // 00001100
    0x3c,         // 00111100
    0x00,         // 00000000
    // 94 0x5e '^'
    0x10,         // 00010000
    0x38,         // 00111000
    0x6c,         // 01101100
    0xc6,         // 11000110
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 95 0x5f '_'
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0xff,         // 11111111
    // 96 0x60 '`'
    0x30,         // 00110000
    0x18,         // 00011000
    0x0c,         // 00001100
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 97 0x61 'a'
    0x00,         // 00000000
    0x00,         // 00000000
    0x78,         // 01111000
    0x0c,         // 00001100
    0x7c,         // 01111100
    0xcc,         // 11001100
    0x76,         // 01110110
    0x00,         // 00000000
    // 98 0x62 'b'
    0xe0,         // 11100000
    0x60,         // 01100000
    0x7c,         // 01111100
    0x66,         // 01100110
    0x66,         // 01100110
    0x66,         // 01100110
    0xdc,         // 11011100
    0x00,         // 00000000
    // 99 0x63 'c'
    0x00,         // 00000000
    0x00,         // 00000000
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xc0,         // 11000000
    0xc6,         // 11000110
    0x7c,         // 01111100
    0x00,         // 00000000
    // 100 0x64 'd'
    0x1c,         // 00011100
    0x0c,         // 00001100
    0x7c,         // 01111100
    0xcc,         // 11001100
    0xcc,         // 11001100
    0xcc,         // 11001100
    0x76,         // 01110110
    0x00,         // 00000000
    // 101 0x65 'e'
    0x00,         // 00000000
    0x00,         // 00000000
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xfe,         // 11111110
    0xc0,         // 11000000
    0x7c,         // 01111100
    0x00,         // 00000000
    // 102 0x66 'f'
    0x3c,         // 00111100
    0x66,         // 01100110
    0x60,         // 01100000
    0xf8,         // 11111000
    0x60,         // 01100000
    0x60,         // 01100000
    0xf0,         // 11110000
    0x00,         // 00000000
    // 103 0x67 'g'
    0x00,         // 00000000
    0x00,         // 00000000
    0x76,         // 01110110
    0xcc,         // 11001100
    0xcc,         // 11001100
    0x7c,         // 01111100
    0x0c,         // 00001100
    0xf8,         // 11111000
    // 104 0x68 'h'
    0xe0,         // 11100000
    0x60,         // 01100000
    0x6c,         // 01101100
    0x76,         // 01110110
    0x66,         // 01100110
    0x66,         // 01100110
    0xe6,         // 11100110
    0x00,         // 00000000
    // 105 0x69 'i'
    0x18,         // 00011000
    0x00,         // 00000000
    0x38,         // 00111000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x3c,         // 00111100
    0x00,         // 00000000
    // 106 0x6a 'j'
    0x06,         // 00000110
    0x00,         // 00000000
    0x06,         // 00000110
    0x06,         // 00000110
    0x06,         // 00000110
    0x66,         // 01100110
    0x66,         // 01100110
    0x3c,         // 00111100
    // 107 0x6b 'k'
    0xe0,         // 11100000
    0x60,         // 01100000
    0x66,         // 01100110
    0x6c,         // 01101100
    0x78,         // 01111000
    0x6c,         // 01101100
    0xe6,         // 11100110
    0x00,         // 00000000
    // 108 0x6c 'l'
    0x38,         // 00111000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x3c,         // 00111100
    0x00,         // 00000000
    // 109 0x6d 'm'
    0x00,         // 00000000
    0x00,         // 00000000
    0xec,         // 11101100
    0xfe,         // 11111110
    0xd6,         // 11010110
    0xd6,         // 11010110
    0xd6,         // 11010110
    0x00,         // 00000000
    // 110 0x6e 'n'
    0x00,         // 00000000
    0x00,         // 00000000
    0xdc,         // 11011100
    0x66,         // 01100110
    0x66,         // 01100110
    0x66,         // 01100110
    0x66,         // 01100110
    0x00,         // 00000000
    // 111 0x6f 'o'
    0x00,         // 00000000
    0x00,         // 00000000
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x7c,         // 01111100
    0x00,         // 00000000
    // 112 0x70 'p'
    0x00,         // 00000000
    0x00,         // 00000000
    0xdc,         // 11011100
    0x66,         // 01100110
    0x66,         // 01100110
    0x7c,         // 01111100
    0x60,         // 01100000
    0xf0,         // 11110000
    // 113 0x71 'q'
    0x00,         // 00000000
    0x00,         // 00000000
    0x76,         // 01110110
    0xcc,         // 11001100
    0xcc,         // 11001100
    0x7c,         // 01111100
    0x0c,         // 00001100
    0x1e,         // 00011110
    // 114 0x72 'r'
    0x00,         // 00000000
    0x00,         // 00000000
    0xdc,         // 11011100
    0x76,         // 01110110
    0x60,         // 01100000
    0x60,         // 01100000
    0xf0,         // 11110000
    0x00,         // 00000000
    // 115 0x73 's'
    0x00,         // 00000000
    0x00,         // 00000000
    0x7e,         // 01111110
    0xc0,         // 11000000
    0x7c,         // 01111100
    0x06,         // 00000110
    0xfc,         // 11111100
    0x00,         // 00000000
    // 116 0x74 't'
    0x30,         // 00110000
    0x30,         // 00110000
    0xfc,         // 11111100
    0x30,         // 00110000
    0x30,         // 00110000
    0x36,         // 00110110
    0x1c,         // 00011100
    0x00,         // 00000000
    // 117 0x75 'u'
    0x00,         // 00000000
    0x00,         // 00000000
    0xcc,         // 11001100
    0xcc,         // 11001100
    0xcc,         // 11001100
    0xcc,         // 11001100
    0x76,         // 01110110
    0x00,         // 00000000
    // 118 0x76 'v'
    0x00,         // 00000000
    0x00,         // 00000000
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x6c,         // 01101100
    0x38,         // 00111000
    0x00,         // 00000000
    // 119 0x77 'w'
    0x00,         // 00000000
    0x00,         // 00000000
    0xc6,         // 11000110
    0xd6,         // 11010110
    0xd6,         // 11010110
    0xfe,         // 11111110
    0x6c,         // 01101100
    0x00,         // 00000000
    // 120 0x78 'x'
    0x00,         // 00000000
    0x00,         // 00000000
    0xc6,         // 11000110
    0x6c,         // 01101100
    0x38,         // 00111000
    0x6c,         // 01101100
    0xc6,         // 11000110
    0x00,         // 00000000
    // 121 0x79 'y'
    0x00,         // 00000000
    0x00,         // 00000000
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x7e,         // 01111110
    0x06,         // 00000110
    0xfc,         // 11111100
    // 122 0x7a 'z'
    0x00,         // 00000000
    0x00,         // 00000000
    0x7e,         // 01111110
    0x4c,         // 01001100
    0x18,         // 00011000
    0x32,         // 00110010
    0x7e,         // 01111110
    0x00,         // 00000000
    // 123 0x7b '{'
    0x0e,         // 00001110
    0x18,         // 00011000
    0x18,         // 00011000
    0x70,         // 01110000
    0x18,         // 00011000
    0x18,         // 00011000
    0x0e,         // 00001110
    0x00,         // 00000000
    // 124 0x7c '|'
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x00,         // 00000000
    // 125 0x7d '}'
    0x70,         // 01110000
    0x18,         // 00011000
    0x18,         // 00011000
    0x0e,         // 00001110
    0x18,         // 00011000
    0x18,         // 00011000
    0x70,         // 01110000
    0x00,         // 00000000
    // 126 0x7e '~'
    0x76,         // 01110110
    0xdc,         // 11011100
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 127 0x7f '^?'
    0x00,         // 00000000
    0x10,         // 00010000
    0x38,         // 00111000
    0x6c,         // 01101100
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xfe,         // 11111110
    0x00,         // 00000000
    // 128 0x80 'M-^@'
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xc0,         // 11000000
    0xc0,         // 11000000
    0xc6,         // 11000110
    0x7c,         // 01111100
    0x0c,         // 00001100
    0x78,         // 01111000
    // 129 0x81 'M-^A'
    0xcc,         // 11001100
    0x00,         // 00000000
    0xcc,         // 11001100
    0xcc,         // 11001100
    0xcc,         // 11001100
    0xcc,         // 11001100
    0x76,         // 01110110
    0x00,         // 00000000
    // 130 0x82 'M-^B'
    0x0c,         // 00001100
    0x18,         // 00011000
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xfe,         // 11111110
    0xc0,         // 11000000
    0x7c,         // 01111100
    0x00,         // 00000000
    // 131 0x83 'M-^C'
    0x7c,         // 01111100
    0x82,         // 10000010
    0x78,         // 01111000
    0x0c,         // 00001100
    0x7c,         // 01111100
    0xcc,         // 11001100
    0x76,         // 01110110
    0x00,         // 00000000
    // 132 0x84 'M-^D'
    0xc6,         // 11000110
    0x00,         // 00000000
    0x78,         // 01111000
    0x0c,         // 00001100
    0x7c,         // 01111100
    0xcc,         // 11001100
    0x76,         // 01110110
    0x00,         // 00000000
    // 133 0x85 'M-^E'
    0x30,         // 00110000
    0x18,         // 00011000
    0x78,         // 01111000
    0x0c,         // 00001100
    0x7c,         // 01111100
    0xcc,         // 11001100
    0x76,         // 01110110
    0x00,         // 00000000
    // 134 0x86 'M-^F'
    0x30,         // 00110000
    0x30,         // 00110000
    0x78,         // 01111000
    0x0c,         // 00001100
    0x7c,         // 01111100
    0xcc,         // 11001100
    0x76,         // 01110110
    0x00,         // 00000000
    // 135 0x87 'M-^G'
    0x00,         // 00000000
    0x00,         // 00000000
    0x7e,         // 01111110
    0xc0,         // 11000000
    0xc0,         // 11000000
    0x7e,         // 01111110
    0x0c,         // 00001100
    0x38,         // 00111000
    // 136 0x88 'M-^H'
    0x7c,         // 01111100
    0x82,         // 10000010
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xfe,         // 11111110
    0xc0,         // 11000000
    0x7c,         // 01111100
    0x00,         // 00000000
    // 137 0x89 'M-   '
    0xc6,         // 11000110
    0x00,         // 00000000
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xfe,         // 11111110
    0xc0,         // 11000000
    0x7c,         // 01111100
    0x00,         // 00000000
    // 138 0x8a 'M-^J'
    0x30,         // 00110000
    0x18,         // 00011000
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xfe,         // 11111110
    0xc0,         // 11000000
    0x7c,         // 01111100
    0x00,         // 00000000
    // 139 0x8b 'M-^K'
    0x66,         // 01100110
    0x00,         // 00000000
    0x38,         // 00111000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x3c,         // 00111100
    0x00,         // 00000000
    // 140 0x8c 'M-^L'
    0x7c,         // 01111100
    0x82,         // 10000010
    0x38,         // 00111000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x3c,         // 00111100
    0x00,         // 00000000
    // 141 0x8d 'M-^M'
    0x30,         // 00110000
    0x18,         // 00011000
    0x00,         // 00000000
    0x38,         // 00111000
    0x18,         // 00011000
    0x18,         // 00011000
    0x3c,         // 00111100
    0x00,         // 00000000
    // 142 0x8e 'M-^N'
    0xc6,         // 11000110
    0x38,         // 00111000
    0x6c,         // 01101100
    0xc6,         // 11000110
    0xfe,         // 11111110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x00,         // 00000000
    // 143 0x8f 'M-^O'
    0x38,         // 00111000
    0x6c,         // 01101100
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xfe,         // 11111110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x00,         // 00000000
    // 144 0x90 'M-^P'
    0x18,         // 00011000
    0x30,         // 00110000
    0xfe,         // 11111110
    0xc0,         // 11000000
    0xf8,         // 11111000
    0xc0,         // 11000000
    0xfe,         // 11111110
    0x00,         // 00000000
    // 145 0x91 'M-^Q'
    0x00,         // 00000000
    0x00,         // 00000000
    0x7e,         // 01111110
    0x18,         // 00011000
    0x7e,         // 01111110
    0xd8,         // 11011000
    0x7e,         // 01111110
    0x00,         // 00000000
    // 146 0x92 'M-^R'
    0x3e,         // 00111110
    0x6c,         // 01101100
    0xcc,         // 11001100
    0xfe,         // 11111110
    0xcc,         // 11001100
    0xcc,         // 11001100
    0xce,         // 11001110
    0x00,         // 00000000
    // 147 0x93 'M-^S'
    0x7c,         // 01111100
    0x82,         // 10000010
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x7c,         // 01111100
    0x00,         // 00000000
    // 148 0x94 'M-^T'
    0xc6,         // 11000110
    0x00,         // 00000000
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x7c,         // 01111100
    0x00,         // 00000000
    // 149 0x95 'M-^U'
    0x30,         // 00110000
    0x18,         // 00011000
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x7c,         // 01111100
    0x00,         // 00000000
    // 150 0x96 'M-^V'
    0x78,         // 01111000
    0x84,         // 10000100
    0x00,         // 00000000
    0xcc,         // 11001100
    0xcc,         // 11001100
    0xcc,         // 11001100
    0x76,         // 01110110
    0x00,         // 00000000
    // 151 0x97 'M-^W'
    0x60,         // 01100000
    0x30,         // 00110000
    0xcc,         // 11001100
    0xcc,         // 11001100
    0xcc,         // 11001100
    0xcc,         // 11001100
    0x76,         // 01110110
    0x00,         // 00000000
    // 152 0x98 'M-^X'
    0xc6,         // 11000110
    0x00,         // 00000000
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x7e,         // 01111110
    0x06,         // 00000110
    0xfc,         // 11111100
    // 153 0x99 'M-^Y'
    0xc6,         // 11000110
    0x38,         // 00111000
    0x6c,         // 01101100
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x6c,         // 01101100
    0x38,         // 00111000
    0x00,         // 00000000
    // 154 0x9a 'M-^Z'
    0xc6,         // 11000110
    0x00,         // 00000000
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x7c,         // 01111100
    0x00,         // 00000000
    // 155 0x9b 'M-^['
    0x18,         // 00011000
    0x18,         // 00011000
    0x7e,         // 01111110
    0xc0,         // 11000000
    0xc0,         // 11000000
    0x7e,         // 01111110
    0x18,         // 00011000
    0x18,         // 00011000
    // 156 0x9c 'M-^\'
    0x38,         // 00111000
    0x6c,         // 01101100
    0x64,         // 01100100
    0xf0,         // 11110000
    0x60,         // 01100000
    0x66,         // 01100110
    0xfc,         // 11111100
    0x00,         // 00000000
    // 157 0x9d 'M-^]'
    0x66,         // 01100110
    0x66,         // 01100110
    0x3c,         // 00111100
    0x7e,         // 01111110
    0x18,         // 00011000
    0x7e,         // 01111110
    0x18,         // 00011000
    0x18,         // 00011000
    // 158 0x9e 'M-^^'
    0xf8,         // 11111000
    0xcc,         // 11001100
    0xcc,         // 11001100
    0xfa,         // 11111010
    0xc6,         // 11000110
    0xcf,         // 11001111
    0xc6,         // 11000110
    0xc7,         // 11000111
    // 159 0x9f 'M-^_'
    0x0e,         // 00001110
    0x1b,         // 00011011
    0x18,         // 00011000
    0x3c,         // 00111100
    0x18,         // 00011000
    0xd8,         // 11011000
    0x70,         // 01110000
    0x00,         // 00000000
    // 160 0xa0 'M- '
    0x18,         // 00011000
    0x30,         // 00110000
    0x78,         // 01111000
    0x0c,         // 00001100
    0x7c,         // 01111100
    0xcc,         // 11001100
    0x76,         // 01110110
    0x00,         // 00000000
    // 161 0xa1 'M-!'
    0x0c,         // 00001100
    0x18,         // 00011000
    0x00,         // 00000000
    0x38,         // 00111000
    0x18,         // 00011000
    0x18,         // 00011000
    0x3c,         // 00111100
    0x00,         // 00000000
    // 162 0xa2 'M-"'
    0x0c,         // 00001100
    0x18,         // 00011000
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x7c,         // 01111100
    0x00,         // 00000000
    // 163 0xa3 'M-#'
    0x18,         // 00011000
    0x30,         // 00110000
    0xcc,         // 11001100
    0xcc,         // 11001100
    0xcc,         // 11001100
    0xcc,         // 11001100
    0x76,         // 01110110
    0x00,         // 00000000
    // 164 0xa4 'M-$'
    0x76,         // 01110110
    0xdc,         // 11011100
    0x00,         // 00000000
    0xdc,         // 11011100
    0x66,         // 01100110
    0x66,         // 01100110
    0x66,         // 01100110
    0x00,         // 00000000
    // 165 0xa5 'M-%'
    0x76,         // 01110110
    0xdc,         // 11011100
    0x00,         // 00000000
    0xe6,         // 11100110
    0xf6,         // 11110110
    0xde,         // 11011110
    0xce,         // 11001110
    0x00,         // 00000000
    // 166 0xa6 'M-&'
    0x3c,         // 00111100
    0x6c,         // 01101100
    0x6c,         // 01101100
    0x3e,         // 00111110
    0x00,         // 00000000
    0x7e,         // 01111110
    0x00,         // 00000000
    0x00,         // 00000000
    // 167 0xa7 'M-''
    0x38,         // 00111000
    0x6c,         // 01101100
    0x6c,         // 01101100
    0x38,         // 00111000
    0x00,         // 00000000
    0x7c,         // 01111100
    0x00,         // 00000000
    0x00,         // 00000000
    // 168 0xa8 'M-('
    0x18,         // 00011000
    0x00,         // 00000000
    0x18,         // 00011000
    0x18,         // 00011000
    0x30,         // 00110000
    0x63,         // 01100011
    0x3e,         // 00111110
    0x00,         // 00000000
    // 169 0xa9 'M-)'
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0xfe,         // 11111110
    0xc0,         // 11000000
    0xc0,         // 11000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 170 0xaa 'M-*'
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0xfe,         // 11111110
    0x06,         // 00000110
    0x06,         // 00000110
    0x00,         // 00000000
    0x00,         // 00000000
    // 171 0xab 'M-+'
    0x63,         // 01100011
    0xe6,         // 11100110
    0x6c,         // 01101100
    0x7e,         // 01111110
    0x33,         // 00110011
    0x66,         // 01100110
    0xcc,         // 11001100
    0x0f,         // 00001111
    // 172 0xac 'M-,'
    0x63,         // 01100011
    0xe6,         // 11100110
    0x6c,         // 01101100
    0x7a,         // 01111010
    0x36,         // 00110110
    0x6a,         // 01101010
    0xdf,         // 11011111
    0x06,         // 00000110
    // 173 0xad 'M--'
    0x18,         // 00011000
    0x00,         // 00000000
    0x18,         // 00011000
    0x18,         // 00011000
    0x3c,         // 00111100
    0x3c,         // 00111100
    0x18,         // 00011000
    0x00,         // 00000000
    // 174 0xae 'M-.'
    0x00,         // 00000000
    0x33,         // 00110011
    0x66,         // 01100110
    0xcc,         // 11001100
    0x66,         // 01100110
    0x33,         // 00110011
    0x00,         // 00000000
    0x00,         // 00000000
    // 175 0xaf 'M-/'
    0x00,         // 00000000
    0xcc,         // 11001100
    0x66,         // 01100110
    0x33,         // 00110011
    0x66,         // 01100110
    0xcc,         // 11001100
    0x00,         // 00000000
    0x00,         // 00000000
    // 176 0xb0 'M-0'
    0x22,         // 00100010
    0x88,         // 10001000
    0x22,         // 00100010
    0x88,         // 10001000
    0x22,         // 00100010
    0x88,         // 10001000
    0x22,         // 00100010
    0x88,         // 10001000
    // 177 0xb1 'M-1'
    0x55,         // 01010101
    0xaa,         // 10101010
    0x55,         // 01010101
    0xaa,         // 10101010
    0x55,         // 01010101
    0xaa,         // 10101010
    0x55,         // 01010101
    0xaa,         // 10101010
    // 178 0xb2 'M-2'
    0x77,         // 01110111
    0xdd,         // 11011101
    0x77,         // 01110111
    0xdd,         // 11011101
    0x77,         // 01110111
    0xdd,         // 11011101
    0x77,         // 01110111
    0xdd,         // 11011101
    // 179 0xb3 'M-3'
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    // 180 0xb4 'M-4'
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0xf8,         // 11111000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    // 181 0xb5 'M-5'
    0x18,         // 00011000
    0x18,         // 00011000
    0xf8,         // 11111000
    0x18,         // 00011000
    0xf8,         // 11111000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    // 182 0xb6 'M-6'
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    0xf6,         // 11110110
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    // 183 0xb7 'M-7'
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0xfe,         // 11111110
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    // 184 0xb8 'M-8'
    0x00,         // 00000000
    0x00,         // 00000000
    0xf8,         // 11111000
    0x18,         // 00011000
    0xf8,         // 11111000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    // 185 0xb9 'M-9'
    0x36,         // 00110110
    0x36,         // 00110110
    0xf6,         // 11110110
    0x06,         // 00000110
    0xf6,         // 11110110
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    // 186 0xba 'M-:'
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    // 187 0xbb 'M-;'
    0x00,         // 00000000
    0x00,         // 00000000
    0xfe,         // 11111110
    0x06,         // 00000110
    0xf6,         // 11110110
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    // 188 0xbc 'M-<'
    0x36,         // 00110110
    0x36,         // 00110110
    0xf6,         // 11110110
    0x06,         // 00000110
    0xfe,         // 11111110
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 189 0xbd 'M-='
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    0xfe,         // 11111110
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 190 0xbe 'M->'
    0x18,         // 00011000
    0x18,         // 00011000
    0xf8,         // 11111000
    0x18,         // 00011000
    0xf8,         // 11111000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 191 0xbf 'M-?'
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0xf8,         // 11111000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    // 192 0xc0 'M-@'
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x1f,         // 00011111
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 193 0xc1 'M-A'
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0xff,         // 11111111
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 194 0xc2 'M-B'
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0xff,         // 11111111
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    // 195 0xc3 'M-C'
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x1f,         // 00011111
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    // 196 0xc4 'M-D'
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0xff,         // 11111111
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 197 0xc5 'M-E'
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0xff,         // 11111111
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    // 198 0xc6 'M-F'
    0x18,         // 00011000
    0x18,         // 00011000
    0x1f,         // 00011111
    0x18,         // 00011000
    0x1f,         // 00011111
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    // 199 0xc7 'M-G'
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    0x37,         // 00110111
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    // 200 0xc8 'M-H'
    0x36,         // 00110110
    0x36,         // 00110110
    0x37,         // 00110111
    0x30,         // 00110000
    0x3f,         // 00111111
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 201 0xc9 'M-I'
    0x00,         // 00000000
    0x00,         // 00000000
    0x3f,         // 00111111
    0x30,         // 00110000
    0x37,         // 00110111
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    // 202 0xca 'M-J'
    0x36,         // 00110110
    0x36,         // 00110110
    0xf7,         // 11110111
    0x00,         // 00000000
    0xff,         // 11111111
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 203 0xcb 'M-K'
    0x00,         // 00000000
    0x00,         // 00000000
    0xff,         // 11111111
    0x00,         // 00000000
    0xf7,         // 11110111
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    // 204 0xcc 'M-L'
    0x36,         // 00110110
    0x36,         // 00110110
    0x37,         // 00110111
    0x30,         // 00110000
    0x37,         // 00110111
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    // 205 0xcd 'M-M'
    0x00,         // 00000000
    0x00,         // 00000000
    0xff,         // 11111111
    0x00,         // 00000000
    0xff,         // 11111111
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 206 0xce 'M-N'
    0x36,         // 00110110
    0x36,         // 00110110
    0xf7,         // 11110111
    0x00,         // 00000000
    0xf7,         // 11110111
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    // 207 0xcf 'M-O'
    0x18,         // 00011000
    0x18,         // 00011000
    0xff,         // 11111111
    0x00,         // 00000000
    0xff,         // 11111111
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 208 0xd0 'M-P'
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    0xff,         // 11111111
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 209 0xd1 'M-Q'
    0x00,         // 00000000
    0x00,         // 00000000
    0xff,         // 11111111
    0x00,         // 00000000
    0xff,         // 11111111
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    // 210 0xd2 'M-R'
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0xff,         // 11111111
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    // 211 0xd3 'M-S'
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    0x3f,         // 00111111
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 212 0xd4 'M-T'
    0x18,         // 00011000
    0x18,         // 00011000
    0x1f,         // 00011111
    0x18,         // 00011000
    0x1f,         // 00011111
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 213 0xd5 'M-U'
    0x00,         // 00000000
    0x00,         // 00000000
    0x1f,         // 00011111
    0x18,         // 00011000
    0x1f,         // 00011111
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    // 214 0xd6 'M-V'
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x3f,         // 00111111
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    // 215 0xd7 'M-W'
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    0xff,         // 11111111
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    // 216 0xd8 'M-X'
    0x18,         // 00011000
    0x18,         // 00011000
    0xff,         // 11111111
    0x18,         // 00011000
    0xff,         // 11111111
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    // 217 0xd9 'M-Y'
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0xf8,         // 11111000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 218 0xda 'M-Z'
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x1f,         // 00011111
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    // 219 0xdb 'M-['
    0xff,         // 11111111
    0xff,         // 11111111
    0xff,         // 11111111
    0xff,         // 11111111
    0xff,         // 11111111
    0xff,         // 11111111
    0xff,         // 11111111
    0xff,         // 11111111
    // 220 0xdc 'M-\'
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0xff,         // 11111111
    0xff,         // 11111111
    0xff,         // 11111111
    0xff,         // 11111111
    // 221 0xdd 'M-]'
    0xf0,         // 11110000
    0xf0,         // 11110000
    0xf0,         // 11110000
    0xf0,         // 11110000
    0xf0,         // 11110000
    0xf0,         // 11110000
    0xf0,         // 11110000
    0xf0,         // 11110000
    // 222 0xde 'M-^'
    0x0f,         // 00001111
    0x0f,         // 00001111
    0x0f,         // 00001111
    0x0f,         // 00001111
    0x0f,         // 00001111
    0x0f,         // 00001111
    0x0f,         // 00001111
    0x0f,         // 00001111
    // 223 0xdf 'M-_'
    0xff,         // 11111111
    0xff,         // 11111111
    0xff,         // 11111111
    0xff,         // 11111111
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 224 0xe0 'M-`'
    0x00,         // 00000000
    0x00,         // 00000000
    0x76,         // 01110110
    0xdc,         // 11011100
    0xc8,         // 11001000
    0xdc,         // 11011100
    0x76,         // 01110110
    0x00,         // 00000000
    // 225 0xe1 'M-a'
    0x78,         // 01111000
    0xcc,         // 11001100
    0xcc,         // 11001100
    0xd8,         // 11011000
    0xcc,         // 11001100
    0xc6,         // 11000110
    0xcc,         // 11001100
    0x00,         // 00000000
    // 226 0xe2 'M-b'
    0xfe,         // 11111110
    0xc6,         // 11000110
    0xc0,         // 11000000
    0xc0,         // 11000000
    0xc0,         // 11000000
    0xc0,         // 11000000
    0xc0,         // 11000000
    0x00,         // 00000000
    // 227 0xe3 'M-c'
    0x00,         // 00000000
    0x00,         // 00000000
    0xfe,         // 11111110
    0x6c,         // 01101100
    0x6c,         // 01101100
    0x6c,         // 01101100
    0x6c,         // 01101100
    0x00,         // 00000000
    // 228 0xe4 'M-d'
    0xfe,         // 11111110
    0xc6,         // 11000110
    0x60,         // 01100000
    0x30,         // 00110000
    0x60,         // 01100000
    0xc6,         // 11000110
    0xfe,         // 11111110
    0x00,         // 00000000
    // 229 0xe5 'M-e'
    0x00,         // 00000000
    0x00,         // 00000000
    0x7e,         // 01111110
    0xd8,         // 11011000
    0xd8,         // 11011000
    0xd8,         // 11011000
    0x70,         // 01110000
    0x00,         // 00000000
    // 230 0xe6 'M-f'
    0x00,         // 00000000
    0x00,         // 00000000
    0x66,         // 01100110
    0x66,         // 01100110
    0x66,         // 01100110
    0x66,         // 01100110
    0x7c,         // 01111100
    0xc0,         // 11000000
    // 231 0xe7 'M-g'
    0x00,         // 00000000
    0x76,         // 01110110
    0xdc,         // 11011100
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x00,         // 00000000
    // 232 0xe8 'M-h'
    0x7e,         // 01111110
    0x18,         // 00011000
    0x3c,         // 00111100
    0x66,         // 01100110
    0x66,         // 01100110
    0x3c,         // 00111100
    0x18,         // 00011000
    0x7e,         // 01111110
    // 233 0xe9 'M-i'
    0x38,         // 00111000
    0x6c,         // 01101100
    0xc6,         // 11000110
    0xfe,         // 11111110
    0xc6,         // 11000110
    0x6c,         // 01101100
    0x38,         // 00111000
    0x00,         // 00000000
    // 234 0xea 'M-j'
    0x38,         // 00111000
    0x6c,         // 01101100
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x6c,         // 01101100
    0x6c,         // 01101100
    0xee,         // 11101110
    0x00,         // 00000000
    // 235 0xeb 'M-k'
    0x0e,         // 00001110
    0x18,         // 00011000
    0x0c,         // 00001100
    0x3e,         // 00111110
    0x66,         // 01100110
    0x66,         // 01100110
    0x3c,         // 00111100
    0x00,         // 00000000
    // 236 0xec 'M-l'
    0x00,         // 00000000
    0x00,         // 00000000
    0x7e,         // 01111110
    0xdb,         // 11011011
    0xdb,         // 11011011
    0x7e,         // 01111110
    0x00,         // 00000000
    0x00,         // 00000000
    // 237 0xed 'M-m'
    0x06,         // 00000110
    0x0c,         // 00001100
    0x7e,         // 01111110
    0xdb,         // 11011011
    0xdb,         // 11011011
    0x7e,         // 01111110
    0x60,         // 01100000
    0xc0,         // 11000000
    // 238 0xee 'M-n'
    0x1e,         // 00011110
    0x30,         // 00110000
    0x60,         // 01100000
    0x7e,         // 01111110
    0x60,         // 01100000
    0x30,         // 00110000
    0x1e,         // 00011110
    0x00,         // 00000000
    // 239 0xef 'M-o'
    0x00,         // 00000000
    0x7c,         // 01111100
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0xc6,         // 11000110
    0x00,         // 00000000
    // 240 0xf0 'M-p'
    0x00,         // 00000000
    0xfe,         // 11111110
    0x00,         // 00000000
    0xfe,         // 11111110
    0x00,         // 00000000
    0xfe,         // 11111110
    0x00,         // 00000000
    0x00,         // 00000000
    // 241 0xf1 'M-q'
    0x18,         // 00011000
    0x18,         // 00011000
    0x7e,         // 01111110
    0x18,         // 00011000
    0x18,         // 00011000
    0x00,         // 00000000
    0x7e,         // 01111110
    0x00,         // 00000000
    // 242 0xf2 'M-r'
    0x30,         // 00110000
    0x18,         // 00011000
    0x0c,         // 00001100
    0x18,         // 00011000
    0x30,         // 00110000
    0x00,         // 00000000
    0x7e,         // 01111110
    0x00,         // 00000000
    // 243 0xf3 'M-s'
    0x0c,         // 00001100
    0x18,         // 00011000
    0x30,         // 00110000
    0x18,         // 00011000
    0x0c,         // 00001100
    0x00,         // 00000000
    0x7e,         // 01111110
    0x00,         // 00000000
    // 244 0xf4 'M-t'
    0x0e,         // 00001110
    0x1b,         // 00011011
    0x1b,         // 00011011
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    // 245 0xf5 'M-u'
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0x18,         // 00011000
    0xd8,         // 11011000
    0xd8,         // 11011000
    0x70,         // 01110000
    // 246 0xf6 'M-v'
    0x00,         // 00000000
    0x18,         // 00011000
    0x00,         // 00000000
    0x7e,         // 01111110
    0x00,         // 00000000
    0x18,         // 00011000
    0x00,         // 00000000
    0x00,         // 00000000
    // 247 0xf7 'M-w'
    0x00,         // 00000000
    0x76,         // 01110110
    0xdc,         // 11011100
    0x00,         // 00000000
    0x76,         // 01110110
    0xdc,         // 11011100
    0x00,         // 00000000
    0x00,         // 00000000
    // 248 0xf8 'M-x'
    0x38,         // 00111000
    0x6c,         // 01101100
    0x6c,         // 01101100
    0x38,         // 00111000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 249 0xf9 'M-y'
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x18,         // 00011000
    0x18,         // 00011000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 250 0xfa 'M-z'
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x18,         // 00011000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 251 0xfb 'M-{'
    0x0f,         // 00001111
    0x0c,         // 00001100
    0x0c,         // 00001100
    0x0c,         // 00001100
    0xec,         // 11101100
    0x6c,         // 01101100
    0x3c,         // 00111100
    0x1c,         // 00011100
    // 252 0xfc 'M-|'
    0x6c,         // 01101100
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    0x36,         // 00110110
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 253 0xfd 'M-}'
    0x78,         // 01111000
    0x0c,         // 00001100
    0x18,         // 00011000
    0x30,         // 00110000
    0x7c,         // 01111100
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    // 254 0xfe 'M-~'
    0x00,         // 00000000
    0x00,         // 00000000
    0x3c,         // 00111100
    0x3c,         // 00111100
    0x3c,         // 00111100
    0x3c,         // 00111100
    0x00,         // 00000000
    0x00,         // 00000000
    // 255 0xff ' '
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000
    0x00,         // 00000000

};
"""


get_cdefs(ffi)
