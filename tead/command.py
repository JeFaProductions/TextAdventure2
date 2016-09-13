import os
import tead.event
import pyfiglet

class Command:

    def __init__(self, callback, helpText):
        self.callback = callback
        self.help = helpText

class CommandParser:

    def __init__(self, eventSystem, world, gui):
        self._eventSystem = eventSystem
        self._world = world
        self._gui = gui

        # command mapping
        self._commands = {
            'start' : Command(self._cmdStart, 'start the game'),
            'help'  : Command(self._cmdHelp, 'show help text'),
            'goto'  : Command(self._cmdGoto, 'go to a direction: NORTH, SOUTH, EAST, WEST')
        }

        self._eventSystem.registerEventHander(tead.event.TEXT_ENTERED,
                                              self._onTextEntered)

    def _cmdStart(self, args):
        figlet = pyfiglet.Figlet("starwars")
        self._gui.output(figlet.renderText("nope"))
        self._gui.output(os.linesep)

    def _cmdHelp(self, args):
        ljustLen = 10
        lines = ['',
                 'Controls:',
                 '',
                 '<escape>'.ljust(ljustLen) + '-- quit game',
                 '<tab>'.ljust(ljustLen) + '-- switch between inventory and command line',
                 '<return>'.ljust(ljustLen) + '-- enter command',
                 '<arrows>'.ljust(ljustLen) + '-- navigate inventory',
                 '',
                 'Commands:',
                 '']

        for key, value in self._commands.items():
            lines.append(key.ljust(ljustLen) + '-- ' + value.help)

        lines.append('')
        self._gui.output(os.linesep.join(lines))

    def _cmdGoto(self, args):
        if len(args) < 2:
            self._gui.outputln('Missing direction.')

        self._world.gotoDirectionStr(args[1])

    def _onTextEntered(self, event):
        if len(event.userParam['args']) == 0:
            return

        cmd = event.userParam['args'][0]

        if event.userParam['args'][0] not in self._commands:
            self._gui.output('Unknown command "' +
                             ' '.join(event.userParam['args']) + '"' + os.linesep)
            return

        self._commands[cmd].callback(event.userParam['args'])
