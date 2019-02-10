import random
import pprint

RootRoom = ((0,0),(1920,1080))

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
    Offset = round(
            LongSide[0] * random.uniform(0.4,0.6))
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
        LeftChildRoomEnd = (
                DivideLine[0],
                ParentRoom[1][1])
        RightChildRoomStart = (
                DivideLine[0],
                ParentRoom[0][1])
    elif DivideLine[1] == 'Y':
        LeftChildRoomEnd = (
                ParentRoom[1][0],
                DivideLine[0])
        RightChildRoomStart = (
                ParentRoom[0][0],
                DivideLine[0])
    
    CorridorStraight = (
            RightChildRoomStart,
            LeftChildRoomEnd)
    LeftChildRoom = (
            LeftChildRoomStart,
            LeftChildRoomEnd)
    RightChildRoom = (
            RightChildRoomStart,
            RightChildRoomEnd)
    return ([LeftChildRoom,
            RightChildRoom],
            CorridorStraight)

def gen_room_hierarchy(
        RootRoom,
        RoomFrameData,
        RoomSize=5000,
        Tier=0,
        BrosID=0):
    Tier += 1
    if get_area(RootRoom) <= RoomSize:
        ID = len(RoomFrameData["BinaryRoomTree"])
        RoomFrameData["BinaryRoomTree"][str(ID)] = {
            "Tier":Tier,
            "Room":RootRoom,
            "Area":get_area(RootRoom),
            "BrosID":BrosID}
        RoomFrameData["TerminateRooms"].append({
            "ID":ID,
            "Room":RootRoom})
        return ID
    else:
        ChildRooms, CorridorStraight = divide_room(
                RootRoom,
                define_divide_line(
                    RootRoom,
                    determine_long_side(
                        RootRoom)))
        RightChildID = gen_room_hierarchy(
                ChildRooms[1],
                RoomFrameData,
                RoomSize,
                Tier)
        LeftChildID = gen_room_hierarchy(
                ChildRooms[0],
                RoomFrameData,
                RoomSize,
                Tier,
                RightChildID)
    ID = len(RoomFrameData["BinaryRoomTree"])
    RoomFrameData["BinaryRoomTree"][str(ID)] = {
        "Tier":Tier,
        "Room":RootRoom,
        "Area":get_area(RootRoom),
        "ChildID":(LeftChildID, RightChildID),
        "BrosID":BrosID}
    RoomFrameData["CorridorStraights"].append({
        "ID":ID,
        "Start":CorridorStraight[0],
        "End": CorridorStraight[1]})
    return ID

def to_level_form(CorridorStraight):
    Start = CorridorStraight["Start"]
    End = CorridorStraight["End"]
    if Start[0] == End[0]:
        Level = 'X',Start[0]
        Range = Start[1],End[1]
    elif Start[1] == End[1]:
        Level = 'Y',Start[1]
        Range = Start[0],End[0]

    return Level, Range

def neighbor_room(Level, Range, Room):
    OnLevel = False
    OutOfRange = True
    for Point in Room["Room"]:
        if Level[0] == 'X':
            Cross = Point[0]
            Straight = Point[1]
        elif Level[0] == 'Y':
            Cross = Point[1]
            Straight = Point[0]

        if Cross == Level[1]:
            OnLevel = True
        if Range[0] <= Straight <= Range[1]:
            OutOfRange = False

    return OnLevel and not OutOfRange

def associate_neighbor_room(CorridorStraight, TerminateRooms):
    Level, Range = to_level_form(CorridorStraight)
    return {
        "ID":CorridorStraight["ID"],
        "RoomList":list(
            filter(
                lambda Room:neighbor_room(
                    Level,
                    Range,
                    Room),
                TerminateRooms
            )
        )
    }

def listup_vaild_child(BinaryRoomTree, Parent):
    pass

def associate_neighbor_room_brt(CorridorStraight,  BinaryRoomTree):
    Level, Range = to_level_form(CorridorStraight)
    VaildParents = CorridorStraight["ID"]
    while(True):
        VaildChildren = listup_vaild_child(
            BinaryRoomTree,
            VaildParents)
        VaildParents = list(
            filter(
                lambda Adult:'ChildID' in Adult,
                list(filter(
                    lambda Room:neighbor_room(
                            Level,
                            Range,
                            Room),
                    VaildChildren
                ))
            )
        )
        if len(VaildParents) == 0:
            break

RoomFrameData = {
    "BinaryRoomTree":{},
    "TerminateRooms":[],
    "CorridorStraights":[]
}
gen_room_hierarchy(RootRoom, RoomFrameData)

pprint.pprint(
    RoomFrameData["BinaryRoomTree"],
    width=50)

pprint.pprint(
    RoomFrameData["TerminateRooms"],
    width=50)
print(len(RoomFrameData["TerminateRooms"]))
pprint.pprint(
    RoomFrameData["CorridorStraights"],
    width=50)

pprint.pprint(
    list(
        map(
            lambda x:associate_neighbor_room(
                x,
                TerminateRooms=RoomFrameData[
                    "TerminateRooms"]),
            RoomFrameData["CorridorStraights"])),
    width=50)

# print(neighbor_room(('Y', 80), (0, 110), {"ID":11, "Room":((0, 0), (60, 80))}))
