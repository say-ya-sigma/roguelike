import random

RootRoom = ((0,0),(160,200))

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

def divide_room(ParentRoom, DivideLine):
    LeftChildRoomStart = ParentRoom[0]
    RightChildRoomEnd = ParentRoom[1]

    if DivideLine[1] == 'X':
        LeftChildRoomEnd = (DivideLine[0], ParentRoom[1][1])
        RightChildRoomStart = (DivideLine[0], ParentRoom[0][1])
    elif DivideLine[1] == 'Y':
        LeftChildRoomEnd = (ParentRoom[1][0], DivideLine[0])
        RightChildRoomStart = (ParentRoom[0][0], DivideLine[0])
    
    LeftChildRoom = (LeftChildRoomStart, LeftChildRoomEnd)
    RightChildRoom = (RightChildRoomStart, RightChildRoomEnd)
    return [LeftChildRoom, RightChildRoom]

print(divide_room(RootRoom, define_divide_line(determine_long_side(RootRoom))))
