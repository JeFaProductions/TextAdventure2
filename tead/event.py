import queue

ROOM_ENTERED = 'roomEntered'

class Event:

    def __init__(self, eventType='', userParam=dict()):
        self.type = eventType
        self.userParam = userParam

class EventSystem:

    def __init__(self):
        self._eventQueue = queue.Queue()
        self._eventHandlers = dict()

    def registerEventHander(self, eventType, callback):
        ''' Register a handler to be called on the given event type.

        eventType specifies the type of event the handler should process.
        callback specifies the function that should be called on the event.
          Its function header should look like "def myCallback(event):"

        Returns the ID of the handler.
        '''
        if not eventType in self._eventHandlers:
            self._eventHandlers[eventType] = []

        handlerID = len(self._eventHandlers[eventType])
        self._eventHandlers[eventType].append(callback)

        return handlerID

    def unregisterEventHandler(self, eventType, handlerID):
        ''' Unregister a handler, so it won't be called on the specified event.

        eventType specifies the type of event the handler should process.
        handlerID specifies the ID of the handler, which should be unregistered.
          The ID was returned by the corresponding register-function.

        Returns True on success, else False.
        '''
        if not eventType in self._eventHandlers:
            return False

        if handlerID >= len(self._eventHandlers[eventType]):
            return False

        self._eventHandlers[eventType].pop(handlerID)

        return True

    def createEvent(self, event):
        self._eventQueue.put_nowait(event)

    def processEvents(self):
        while not self._eventQueue.empty():
            event = self._eventQueue.get_nowait()

            # check if eventhandler wants to process event
            if not event.type in self._eventHandlers:
                continue

            for cb in self._eventHandlers[event.type]:
                cb(event)
