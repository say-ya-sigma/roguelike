RootRoom = ((0,0),(200,200))

def determine_long_side(Room):
    XLen = Room[1][0] - Room[0][0]
    YLen = Room[1][1] - Room[0][1]

    if XLen >= YLen:
        return XLen, 'X'
    else:
        return YLen, 'Y'

print(determine_long_side(RootRoom))
