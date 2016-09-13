import tkinter as tk
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

    # create Event that text was entered on console
    EVENT_SYSTEM.createEvent(
        evt.Event(evt.TEXT_ENTERED, {'args': args}))

    EVENT_SYSTEM.processEvents()


if __name__ == '__main__':
    EVENT_SYSTEM = evt.EventSystem()

    GUI = gui.MainWindow()
    GUI.setOnReturn(processInput)

    WORLD = game.World(EVENT_SYSTEM)

    CMD_PARSER = cmd.CommandParser(EVENT_SYSTEM, WORLD, GUI)

    GUI.mainloop()
