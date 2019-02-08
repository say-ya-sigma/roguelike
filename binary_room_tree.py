import random

RootRoom = ((0,0),(200,200))

def determine_long_side(Room):
    XLen = Room[1][0] - Room[0][0]
    YLen = Room[1][1] - Room[0][1]

    if XLen >= YLen:
        LongSide = (XLen, 'X')
    else:
        LongSide = (YLen, 'Y')

    return LongSide

def define_divide_line(LongSide):
    Point = round(LongSide[0] * random.uniform(0.4,0.6))
    Axis = LongSide[1]
    return(Point, Axis)

print(define_divide_line(determine_long_side(RootRoom)))
