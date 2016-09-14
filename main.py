import tead.event as evt
import tead.gui as gui
import tead.command as cmd
import tead.game as game

EVENT_SYSTEM = None
GUI = None
CMD_PARSER = None
WORLD = None

def processInput(text):
    args = text.rstrip().lstrip().split()

    CMD_PARSER.parse(args)

    EVENT_SYSTEM.processEvents()

if __name__ == '__main__':
    EVENT_SYSTEM = evt.EventSystem()

    GUI = gui.MainWindow()
    GUI.setOnReturn(processInput)

    WORLD = game.World(EVENT_SYSTEM, GUI)

    CMD_PARSER = cmd.CommandParser(WORLD, GUI)

    GUI.mainloop()
