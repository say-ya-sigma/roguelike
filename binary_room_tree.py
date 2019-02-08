import random
import pprint

RootRoom = ((0,0),(200,200))

def get_area(Room):
    XLen = Room[1][0] - Room[0][0]
    YLen = Room[1][1] - Room[0][1]
    return XLen * YLen


def determine_long_side(Room):
    XLen = Room[1][0] - Room[0][0]
    YLen = Room[1][1] - Room[0][1]

    if XLen >= YLen:
        LongSide = (XLen, 'X')
    else:
        LongSide = (YLen, 'Y')

    return LongSide

def define_divide_line(RootRoom, LongSide):
    Offset = round(LongSide[0] * random.uniform(0.4,0.6))
    Axis = LongSide[1]
    if Axis == 'X':
        Point = RootRoom[0][0] + Offset
    elif Axis == 'Y':
        Point = RootRoom[0][1] + Offset
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

def gen_room_hierarchy(RootRoom, BinaryRoomTree, RoomSize=5000, Tier=1):
    BinaryRoomTree.append((Tier, RootRoom, get_area(RootRoom)))
    if get_area(RootRoom) <= RoomSize:
        return 
    else:
        Tier += 1
        ChildRooms = divide_room(RootRoom, define_divide_line(RootRoom, determine_long_side(RootRoom)))
        gen_room_hierarchy(ChildRooms[0], BinaryRoomTree, RoomSize, Tier)
        gen_room_hierarchy(ChildRooms[1], BinaryRoomTree, RoomSize, Tier)


BinaryRoomTree = []
gen_room_hierarchy(RootRoom, BinaryRoomTree)

pprint.pprint(sorted(BinaryRoomTree, key=lambda tup: tup[0]))
