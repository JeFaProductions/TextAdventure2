import tead.event
import pyfiglet

class Command:
    
    def __init__(self, callback, helpText):
        self.callback = callback
        self.help = helpText

class CommandParser:

    def __init__(self, eventSystem, gui):
        self._eventSystem = eventSystem
        self._gui = gui
        
        # command mapping
        self._commands = {
            'start' : Command(self._cmdStart, 'start the game'),
            'help'  : Command(self._cmdHelp, 'show help text')
        }
        
        self._eventSystem.registerEventHander(tead.event.TEXT_ENTERED,
                                              self._onTextEntered)
        
    def _cmdStart(self, args):
        figlet = pyfiglet.Figlet("starwars")
        self._gui.output(figlet.renderText("nope"))
        self._gui.output("\r\n")

    def _cmdHelp(self, args):
        lines = ['',
                 'Controls:',
                 '',
                 '<escape>  -- quit game',
                 '<tab>     -- switch between inventory and command line',
                 '<return>  -- enter command',
                 '',
                 'Commands:',
                 '']
        
        for key, value in self._commands.items():
            lines.append(key.ljust(10) + '-- ' + value.help)
        
        lines.append('')
        self._gui.output('\n'.join(lines)) 
                   
        
    def _onTextEntered(self, event):
        if len(event.userParam['args']) == 0:
            return
        
        cmd = event.userParam['args'][0]
        
        if event.userParam['args'][0] not in self._commands:
            self._gui.output('Unknown command "' +
                             ' '.join(event.userParam['args']) + '"\n')
            return
        
        self._commands[cmd].callback(event.userParam['args'])