class ActionManager:

    def __init__(self):

        self._actions = {
            'createItem'  : self._createItem,
            'destroyItem' : self._destroyItem,
            'openDoor'    : self._openDoor,
            'closeDoor'   : self._closeDoor,
            'printText'   : self._printText
        }

    def _createItem(self, param):
        pass

    def _destroyItem(self, param):
        pass

    def _openDoor(self, param):
        pass

    def _closeDoor(self, param):
        pass

    def _printText(self, param):
        pass

    def createAction(self, action, param=dict()):
        ''' Creates a lambda function with the given action and parameters.

        action specifies the type of action that will be created.
        param is a dictionary that specifies parameters for the action that
          will be created.

        Returns a function which executes the action.
        '''
        if not action in self._actions:
            return None

        return lambda : self._actions[action](param)
