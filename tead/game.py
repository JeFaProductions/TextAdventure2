import tead.event as evt

NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3

_DIR_TO_STR = ['NORTH', 'SOUTH', 'EAST', 'WEST']
_DIR_FROM_STR = {'NORTH' : 0, 'SOUTH' : 1, 'EAST': 2, 'WEST' : 3}

def dirToStr(direction):
    if direction < 0 or direction > 3:
        return None
    return _DIR_TO_STR[direction]

def dirFromStr(directionStr):
    upStr = directionStr.upper()
    if not upStr in _DIR_FROM_STR:
        return None
    return _DIR_FROM_STR[upStr]

class Item:

    def __init__(self):
        self.id = ''
        self.name = ''

class Player:

    def __init__(self):
        self.inventory = dict()

    def addItem(self, item):
        self.inventory[item.id] = item

    def removeItem(self, itemID):
        item = self.inventory[itemID]
        del self.inventory[itemID]
        return item


class Door:

    def __init__(self, locked=False):
        self.locked = locked
        self.nextRoom = ''

class Room:

    def __init__(self):
        self.id = ''
        self.name = ''
        self.doors = [None, None, None, None]
        self.items = dict()
        self._eventListener = []

    def addItem(self, item):
        self.items[item.id] = item

    def removeItem(self, itemID):
        item = self.items[itemID]
        del self.items[itemID]
        return item

    def hasDoor(self, direction):
        return direction >= 0 and direction < len(self.doors) and not self.doors[direction] is None

    def canPassDoor(self, direction):
        return self.hasDoor(direction) and not self.doors[direction].locked

class World:

    def __init__(self, eventSystem):
        self.currentRoomID = ''
        self.player = Player()
        self.rooms = dict()
        self._eventSystem = eventSystem

    def addRoom(self, room):
        self.rooms[room.id] = room

    def gotoDirectionStr(self, directionStr):
        direction = dirFromStr(directionStr)

        if direction is None:
            # TODO print 'invalid direction'
            return

        self.gotoDirection(direction)

    def gotoDirection(self, direction):
        assert(self.currentRoomID in self.rooms)

        currRoom = self.rooms[self.currentRoomID]

        if not currRoom.hasDoor(direction):
            # TODO print 'no door in this direction'
            return

        if not currRoom.doors[direction].locked:
            # TODO print 'door is locked'
            return

        self.currentRoomID = currRoom.doors[direction].nextRoom
        self.eventSystem.createEvent(evt.Event(evt.ROOM_ENTERED,
           {'room' : self.rooms[self.currentRoomID]}))
