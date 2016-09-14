class ActionBuilder:

    def __init__(self, world, gui):

        self._gui = gui
        self._world = world

        self._actions = {
            'createItem'  : self._createItem,
            'destroyItem' : self._destroyItem,
            'openDoor'    : self._openDoor,
            'closeDoor'   : self._closeDoor,
            'printText'   : self._printText
        }

        self._conditions = {
                'usedItem' : self._usedItem
        }

    def _clear(self):
        self._builtActions = []
        self._builtConditions = []

    def _createItem(self, param):
        pass

    def _destroyItem(self, param):
        pass

    def _openDoor(self, param):
        assert('direction' in param)
        direction = param['direction']
        self._world.doors[direction].locked = False

    def _closeDoor(self, param):
        assert('direction' in param)
        direction = param['direction']
        self._world.doors[direction].locked = True

    def _printText(self, param):
        assert('text' in param)
        self._gui.outputln(param['text'])

    def createAction(self, action, param=dict()):
        ''' Creates a lambda function with the given action and parameters.

        :param action, string that specifies the type of action that will be created.
        :param param, a dictionary that specifies parameters for the action that
          will be created.

        :return a function which executes the action.
        '''
        if not action in self._actions:
            return

        self._builtActions.append(lambda : self._actions[action](param))
        return self

    def _usedItem(self, param):
        assert('items' in param and 'itemName' in param)
        for i in param['items']:
            if i == param['itemName']:
                return True
        return False

    def createCondition(self, condition, param=dict()):
        ''' Creates a lambda function with the given condition and parameters.

        :param condition, string that specifies the type of condition that will be created.
        :param param, a dictionary that specifies parameters for the action that
          will be created.

        :return a function which checks the condition.
        '''
        if not condition in self._conditions:
            return

        self._builtConditions.append(lambda : self._actions[condition](param))
        return self

    def build(self):
        conds = self._builtConditions
        acts = self._builtActions

        def actionCB(event):
            for cond in conds:
                if not cond():
                    return

            for act in acts:
                act()

        self._clear()
        return actionCB

