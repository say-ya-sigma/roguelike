import random
import pprint
from functools import reduce

RootRoom = ((0,0),(480,320))

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
    
    Partition = (
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
            Partition)

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
            "ID":ID,
            "Tier":Tier,
            "Room":RootRoom,
            "Area":get_area(RootRoom),
            "BrosID":BrosID}
        RoomFrameData["TerminateRooms"][str(ID)] = {
            "ID":ID,
            "Room":RootRoom,
            "Wall":tuple([random.randint(2, round(min(RootRoom[1][0]-RootRoom[0][0],RootRoom[1][1]-RootRoom[0][1])*0.15)) for i in range(4)])}
        return ID
    else:
        ChildRooms, Partition = divide_room(
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
        "ID":ID,
        "Tier":Tier,
        "Room":RootRoom,
        "Area":get_area(RootRoom),
        "ChildID":{LeftChildID, RightChildID},
        "BrosID":BrosID}
    RoomFrameData["Partitions"].append({
        "ID":ID,
        "Start":Partition[0],
        "End":Partition[1]})
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
                TerminateRooms.values()
            )
        )
    }

def vaild_child(BinaryRoomTree, Parents):
    return list(map(
        lambda ChildID:BinaryRoomTree[str(ChildID)]
        ,reduce(lambda x,y:x.union(y),map(
            lambda ID:BinaryRoomTree[str(ID)]['ChildID'],
            Parents
        ))
    ))

def associate_neighbor_room_brt(CorridorStraight, BinaryRoomTree):
    Level, Range = to_level_form(CorridorStraight)
    VaildParents = {CorridorStraight['ID']}
    NeighborRoom = set()
    while len(VaildParents) != 0:
        VaildChildren = vaild_child(
            BinaryRoomTree,
            VaildParents)
        Neighbors = set(map(
            lambda Neighbor:Neighbor['ID'],
            filter(
                lambda Room:neighbor_room(
                    Level,
                    Range,
                    Room),
                VaildChildren
            )
        ))
        Parents = set(map(
            lambda Parent:Parent['ID'],
            filter(
                lambda Adult:'ChildID' in Adult,
                VaildChildren
            )
        ))
        VaildParents = Neighbors & Parents
        VaildTerminates = Neighbors - VaildParents

        NeighborRoom = NeighborRoom.union(VaildTerminates)
    return {'ID':CorridorStraight['ID'],
            'Rooms':NeighborRoom}

def right_side(Level, Room):
    return Room[0][0] == Level or Room[0][1] == Level

def align_rooms(CorridorStraight, Rooms):
    Level, Range = to_level_form(Corridor)

def generate_path(RoomsOnStraight,Straights,BRT):
    return RoomsOnStraight

RoomFrameData = {
    'BinaryRoomTree':{},
    'TerminateRooms':{},
    'Partitions':[]
}
gen_room_hierarchy(RootRoom, RoomFrameData)

Corridor = {
    'Straights':{},
    'RoomsOnStraights':[],
    'Paths':[]
}

Corridor['Straights'] = RoomFrameData["Partitions"]


Corridor['RoomsOnStraights'] = list(map(
    lambda x:associate_neighbor_room_brt(
        x,
        BinaryRoomTree=RoomFrameData[
            "BinaryRoomTree"]),
    Corridor['Straights']
))

Corridor['Paths'] = list(map(
    lambda x:generate_path(
        x,
        Straights = Corridor['Straights'],
        BRT = RoomFrameData['BinaryRoomTree']),
    Corridor['RoomsOnStraights']
))


pprint.pprint(
    RoomFrameData["BinaryRoomTree"],
    width=50)

pprint.pprint(
    RoomFrameData["TerminateRooms"],
    width=50)
print(len(RoomFrameData["TerminateRooms"]))
pprint.pprint(
    RoomFrameData["Partitions"],
    width=50)

pprint.pprint(Corridor['RoomsOnStraights'],width=50)

print(neighbor_room(('Y', 80), (0, 110), {"ID":11, "Room":((0, 0), (60, 80))}))
