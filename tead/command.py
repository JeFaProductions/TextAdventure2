import os
import pyfiglet

class Command:

    def __init__(self, callback, helpText):
        self.callback = callback
        self.help = helpText

class CommandParser:

    def __init__(self, world, gui):
        self._world = world
        self._gui = gui

        # command mapping
        self._commands = {
            'start' : Command(self._cmdStart, 'start the game'),
            'help'  : Command(self._cmdHelp, 'show help text'),
            'goto'  : Command(self._cmdGoto, 'go to a direction: NORTH, SOUTH, EAST, WEST')
        }

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
            return

        self._world.gotoDirectionStr(args[1])

    def parse(self, args):
        if len(args) == 0:
            return

        self._gui.outputln('> ' + ' '.join(args))

        cmd = args[0]

        if args[0] not in self._commands:
            self._gui.outputln('Unknown command "' +
                             ' '.join(args) + '"')
            return

        self._commands[cmd].callback(args)
