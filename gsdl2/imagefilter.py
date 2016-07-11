from . import gfx_lib


def mmx_detect():
    return gfx_lib.SDL_imageFilterMMXdetect()


def mmx_off():
    gfx_lib.SDL_imageFilterMMXoff()


def mmx_on():
    gfx_lib.SDL_imageFilterMMXon()

# All routines return:
#   0   OK
#  -1   Error (internal error, parameter error)


#  SDL_imageFilterAdd: D = saturation255(S1 + S2)
def add(src1, src2, dest, length):
    return gfx_lib.SDL_imageFilterAdd(src1, src2, dest, length)


#  SDL_imageFilterMean: D = S1/2 + S2/2
def mean(src1, src2, dest, length):
    return gfx_lib.SDL_imageFilterMean(src1, src2, dest, length)


#  SDL_imageFilterSub: D = saturation0(S1 - S2)
def sub(src1, src2, dest, length):
    return gfx_lib.SDL_imageFilterSub(src1, src2, dest, length)


#  SDL_imageFilterAbsDiff: D = | S1 - S2 |
def abs_diff(src1, src2, dest, length):
    return gfx_lib.SDL_imageFilterAbsDiff(src1, src2, dest, length)


#  SDL_imageFilterMult: D = saturation(S1 * S2)
def mult(src1, src2, dest, length):
    return gfx_lib.SDL_imageFilterMult(src1, src2, dest, length)


#  SDL_imageFilterMultNor: D = S1 * S2   (non-MMX)
def mult_nor(src1, src2, dest, length):
    return gfx_lib.SDL_imageFilterMultNor(src1, src2, dest, length)


#  SDL_imageFilterMultDivby2: D = saturation255(S1/2 * S2)
def mult_div_by_2(src1, src2, dest, length):
    return gfx_lib.SDL_imageFilterMultDivby2(src1, src2, dest, length)


#  SDL_imageFilterMultDivby4: D = saturation255(S1/2 * S2/2)
def mult_div_by_4(src1, src2, dest, length):
    return gfx_lib.SDL_imageFilterMultDivby4(src1, src2, dest, length)


#  SDL_imageFilterBitAnd: D = S1 & S2
def bit_and(src1, src2, dest, length):
    return gfx_lib.SDL_imageFilterBitAnd(src1, src2, dest, length)


#  SDL_imageFilterBitOr: D = S1 | S2
def bit_or(src1, src2, dest, length):
    return gfx_lib.SDL_imageFilterBitOr(src1, src2, dest, length)


#  SDL_imageFilterDiv: D = S1 / S2   (non-MMX)
def div(src1, src2, dest, length):
    return gfx_lib.SDL_imageFilterDiv(src1, src2, dest, length)


#  SDL_imageFilterBitNegation: D = !S
def bit_negation(src1, dest, length):
    return gfx_lib.SDL_imageFilterBitNegation(src1, dest, length)


#  SDL_imageFilterAddByte: D = saturation255(S + C)
def add_byte(src1, dest, length, c):
    return gfx_lib.SDL_imageFilterAddByte(src1, dest, length, c)


#  SDL_imageFilterAddUint: D = saturation255(S + (uint)C)
def add_uint(src1, dest, length, c):
    return gfx_lib.SDL_imageFilterAddUint(src1, dest, length, c)


#  SDL_imageFilterAddByteToHalf: D = saturation255(S/2 + C)
def add_byte_to_half(src1, dest, length, c):
    return gfx_lib.SDL_imageFilterAddByteToHalf(src1, dest, length, c)


#  SDL_imageFilterSubByte: D = saturation0(S - C)
def sub_byte(src1, dest, length, c):
    return gfx_lib.SDL_imageFilterSubByte(src1, dest, length, c)


#  SDL_imageFilterSubUint: D = saturation0(S - (uint)C)
def sub_uint(src1, dest, length, c):
    return gfx_lib.SDL_imageFilterSubUint(src1, dest, length, c)


#  SDL_imageFilterShiftRight: D = saturation0(S >> N)
def shift_right(src1, dest, length, n):
    return gfx_lib.SDL_imageFilterShiftRight(src1, dest, length, n)


#  SDL_imageFilterShiftRightUint: D = saturation0((uint)S >> N)
def shift_right_uint(src1, dest, length, n):
    return gfx_lib.SDL_imageFilterShiftRightUint(src1, dest, length, n)


#  SDL_imageFilterMultByByte: D = saturation255(S * C)
def mult_by_byte(src1, dest, length, c):
    return gfx_lib.SDL_imageFilterMultByByte(src1, dest, length, c)


#  SDL_imageFilterShiftRightAndMultByByte: D = saturation255((S >> N) * C)
def shift_right_and_mult_by_byte(src1, dest, length, n, c):
    return gfx_lib.SDL_imageFilterShiftRightAndMultByByte(src1, dest, length, n, c)


#  SDL_imageFilterShiftLeftByte: D = (S << N)
def shift_left_byte(src1, dest, length, n):
    return gfx_lib.SDL_imageFilterShiftLeftByte(src1, dest, length, n)


#  SDL_imageFilterShiftLeftUint: D = ((uint)S << N)
def shift_left_uint(src1, dest, length, n):
    return gfx_lib.SDL_imageFilterShiftLeftUint(src1, dest, length, n)


#  SDL_imageFilterShiftLeft: D = saturation255(S << N)
def shift_left(src1, dest, length, n):
    return gfx_lib.SDL_imageFilterShiftLeft(src1, dest, length, n)


#  SDL_imageFilterBinarizeUsingThreshold: D = S >= T ? 255:0
def binerize_using_threshold(src1, dest, length, t):
    return gfx_lib.SDL_imageFilterBinarizeUsingThreshold(src1, dest, length, t)


#  SDL_imageFilterClipToRange: D = (S >= Tmin) & (S <= Tmax) 255:0
def clip_to_range(src1, dest, length, tmin, tmax):
    return gfx_lib.SDL_imageFilterClipToRange(src1, dest, length, tmin, tmax)


#  SDL_imageFilterNormalizeLinear: D = saturation255((Nmax - Nmin)/(Cmax - Cmin)*(S - Cmin) + Nmin)
def normalize_linear(src, dest, length, cmin, cmax, nmin, nmax):
    return gfx_lib.SDL_imageFilterNormalizeLinear(src, dest, length, cmin, cmax, nmin, nmax)
