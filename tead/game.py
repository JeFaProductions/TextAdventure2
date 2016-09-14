import enum
import tead.event as evt

_DIRECTION = enum.Enum(
    "_DIRECTION", "NORTH, SOUTH, EAST, WEST"
)


class Item:
    def __init__(self):
        self.id = None
        self.name = None


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
        self.nextRoom = None


class Room:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.doors = {
            _DIRECTION.NORTH: None,
            _DIRECTION.EAST: None,
            _DIRECTION.SOUTH: None,
            _DIRECTION.WEST: None
        }
        self.items = dict()
        self._eventListener = []

    def addItem(self, item):
        self.items[item.id] = item

    def removeItem(self, itemID):
        item = self.items[itemID]
        del self.items[itemID]
        return item

    def hasDoor(self, direction):
        return self.doors[direction] is not None

    def canPassDoor(self, direction):
        return self.hasDoor(direction) and not self.doors[direction].locked


class World:
    def __init__(self, eventSystem, gui):
        self.currentRoomID = None
        self.player = Player()
        self.rooms = dict()
        self._eventSystem = eventSystem
        self._gui = gui

    def addRoom(self, room):
        self.rooms[room.id] = room

    def gotoDirectionStr(self, directionStr):
        directionStr = directionStr.upper()
        if directionStr not in _DIRECTION.__members__:
            self._gui.outputln('Invalid direction.')
            return

        direction = _DIRECTION[directionStr]

        self.gotoDirection(direction)

    def gotoDirection(self, direction):
        assert(self.currentRoomID in self.rooms)

        currRoom = self.rooms[self.currentRoomID]

        if not currRoom.hasDoor(direction):
            self._gui.outputln('There is no door in this direction.')
            return

        if not currRoom.doors[direction].locked:
            self._gui.outputln('The door is locked.')
            return

        self.currentRoomID = currRoom.doors[direction].nextRoom
        self.eventSystem.createEvent(evt.Event(evt.ROOM_ENTERED,
                                               {'room': self.rooms[self.currentRoomID]}))
